import os
from together import Together
from dotenv import load_dotenv
load_dotenv("../.env")

client = Together()

stream = client.chat.completions.create(
  model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
  messages=[{"role": "user", "content": "What are some fun things to do in New York?"}],
  stream=True,
)

for chunk in stream:
  print(chunk.choices[0].delta.content or "", end="", flush=True)
