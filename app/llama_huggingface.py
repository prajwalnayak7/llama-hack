import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import List, Optional
import logging

class LLMInference:
    def __init__(
        self,
        model_name: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        device: str = "cuda",
        low_memory: bool = True
    ):
        """
        Initialize LLM model and tokenizer
        Args:
            model_name: Name of the model on HuggingFace
            device: Device to run inference on ("cuda" or "cpu")
            low_memory: Whether to use low memory optimizations
        """
        self.device = "cuda" if torch.cuda.is_available() and device == "cuda" else "cpu"
        logging.info(f"Using device: {self.device}")
        
        try:
            logging.info(f"Loading model from HuggingFace: {model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            # Model loading configuration based on memory constraints
            if low_memory:
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    low_cpu_mem_usage=True
                )
                self.model.to(self.device)
            else:
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
                )
                self.model.to(self.device)
            
            # Set padding token if not set
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            self.model.eval()
            logging.info("Model loaded successfully")
            
        except Exception as e:
            raise Exception(f"Error loading model: {str(e)}") from e

    def format_prompt(self, prompt: str) -> str:
        """
        Format prompt for the model
        Args:
            prompt: Raw input prompt
        Returns:
            Formatted prompt
        """
        return f"<|system|>You are a helpful AI assistant.</s><|user|>{prompt}</s><|assistant|>"

    def generate_response(
        self,
        prompt: str,
        max_length: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.95,
        top_k: int = 50,
        num_return_sequences: int = 1,
        stop_words: Optional[List[str]] = None
    ) -> List[str]:
        """
        Generate responses from the model
        Args:
            prompt: Input text prompt
            max_length: Maximum length of generated sequence
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            top_k: Top-k sampling parameter
            num_return_sequences: Number of responses to generate
            stop_words: List of words to stop generation when encountered
        Returns:
            List of generated responses
        """
        try:
            formatted_prompt = self.format_prompt(prompt)
            inputs = self.tokenizer(formatted_prompt, return_tensors="pt", padding=True)
            inputs = inputs.to(self.device)

            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    temperature=temperature,
                    top_p=top_p,
                    top_k=top_k,
                    num_return_sequences=num_return_sequences,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    do_sample=True
                )

            responses = []
            for output in outputs:
                decoded = self.tokenizer.decode(output, skip_special_tokens=True)
                
                # Remove the prompt from the response
                if formatted_prompt in decoded:
                    decoded = decoded.split("<|assistant|>")[-1].strip()
                
                # Handle stop words if provided
                if stop_words:
                    for stop_word in stop_words:
                        if stop_word in decoded:
                            decoded = decoded[:decoded.index(stop_word)]
                
                responses.append(decoded)

            return responses
            
        except Exception as e:
            logging.error(f"Error during generation: {str(e)}")
            raise

    def batch_generate(
        self,
        prompts: List[str],
        **kwargs
    ) -> List[List[str]]:
        """
        Generate responses for multiple prompts
        Args:
            prompts: List of input prompts
            **kwargs: Additional arguments passed to generate_response
        Returns:
            List of lists containing generated responses for each prompt
        """
        responses = []
        for prompt in prompts:
            responses.append(self.generate_response(prompt, **kwargs))
        return responses

# Example usage:
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize the model
    llm = LLMInference(low_memory=True)

    # Test with a single prompt
    prompt = "Explain what is machine learning in simple terms:"
    responses = llm.generate_response(
        prompt,
        max_length=256,
        temperature=0.8,
        num_return_sequences=1
    )
    print(f"\nPrompt: {prompt}")
    print(f"Response: {responses[0]}")

    # Test batch generation
    prompts = [
        "Write a haiku about spring:",
        "Give me a fun fact about space:"
    ]
    batch_responses = llm.batch_generate(prompts, max_length=128)
    for prompt, response_list in zip(prompts, batch_responses):
        print(f"\nPrompt: {prompt}")
        print(f"Response: {response_list[0]}")

    # Close the model
    llm.close()
    logging.info("Model closed")
    