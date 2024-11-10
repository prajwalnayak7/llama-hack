from llama_stack_client import LlamaStackClient
from llama_stack_client.types import UserMessage

host = "localhost"
port = 5000
client = LlamaStackClient(
    base_url=f"http://{host}:{port}",
)

response = client.inference.chat_completion(
    messages=[
        UserMessage(
            content="hello world, write me a 2 sentence poem about the moon",
            role="user",
        ),
    ],
    model="Llama3.1-8B-Instruct",
    stream=False,
)
print(response)
