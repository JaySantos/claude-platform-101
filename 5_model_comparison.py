import os

import anthropic
from dotenv import load_dotenv

load_dotenv(".env.local")  # loads the file's variables into os.environ

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

models = ["claude-haiku-4-5", "claude-sonnet-5", "claude-opus-5-5"]

prompt = "Explain prompt caching in two sentences"

for model in models:
    response = client.messages.create(
        model=model,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    print("Model: %s" % model)
    print(" %s --- %s" % (response.usage.input_tokens, response.usage.output_tokens))
    if model == "claude-opus-5-5":
        print(response.content[1].text)
    else:
        print(response.content[0].text)
