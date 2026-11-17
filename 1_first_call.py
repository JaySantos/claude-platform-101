import os

import anthropic
from dotenv import load_dotenv

load_dotenv(".env.local")  # loads the file's variables into os.environ

buggyCode = "function add(a, b) {return a - b;}"

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=2048,
    system="You are a terse senior code reviewer. Give feedback in one paragraph.",
    messages=[{"role": "user", "content": f"Review this code:\n{buggyCode}"}],
)
for block in message.content:
    print(block.text)
