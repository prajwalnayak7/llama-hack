from openai import OpenAI
from dotenv import load_dotenv
load_dotenv("../.env")

client = OpenAI(
  base_url="https://api.featherless.ai/v1",
  api_key="rc_0ce91e40e1afbac92573f81b90993136698d308130b17dd054b9093b88992dca",
)

response = client.chat.completions.create(
  model='meta-llama/Meta-Llama-3-8B-Instruct',
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ],
)
print(response.model_dump()['choices'][0]['message']['content'])