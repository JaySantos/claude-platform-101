import os

import anthropic
from anthropic import beta_tool
from dotenv import load_dotenv

load_dotenv(".env.local")  # loads the file's variables into os.environ

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


@beta_tool
def get_weather(city: str) -> str:
    """Get today's current weather for a city."""
    print(f"get_weather called with city: {city}")
    return f"Weather in {city}: 95F, sunny"


@beta_tool
def get_forecast(city: str) -> str:
    """Get the weather forecast for the next few days for a city."""
    print(f"get_forecast called with city: {city}")
    return f"Forecast for {city}: Sunny for 3 days"


# The tool runner automatically handles the loop
response = client.beta.messages.tool_runner(
    model="claude-opus-5-5",
    max_tokens=1024,
    tools=[get_weather, get_forecast],  # Pass all tools here
    messages=[
        {
            "role": "user",
            "content": "What should I wear in Austin today? What about on Wednesday?",
        }
    ],
).until_done()

for block in response.content:
    if block.type == "text":
        print(block.text)
