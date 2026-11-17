import os

import anthropic
from dotenv import load_dotenv

load_dotenv(".env.local")  # loads the file's variables into os.environ

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# The tools array tells Claude what's available:
# a name, a description, and a JSON schema for the inputs.
tools = [
    {
        "name": "get_weather",
        "description": "Get today's current weather for a city.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The city to check"}
            },
            "required": ["city"],
        },
    },
    {
        "name": "get_forecast",
        "description": "Get the weather forecast for the next few days for a city.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The city to check"}
            },
            "required": ["city"],
        },
    },
]


# run_tool is just a hardcoded lookup.
# In a real app, this would hit your database, an API, whatever.
def run_tool(name, tool_input):
    match name:
        case "get_weather":
            return f"Weather in {tool_input['city']}: 95F, sunny"
        case "get_forecast":
            return f"Forecast in {tool_input['city']}: 95F, sunny for the next 3 days"

    raise ValueError(f"Unknown tool: {name}")


messages = [
    {"role": "user", "content": "I'll spend the week in Austin, what should I pack?"}
]

# The agent loop. Each iteration sends messages to Claude
# and switches on the response's stop reason.
while True:
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )

    if response.stop_reason == "end_turn":
        # Claude is done. Print the final text and break.
        for block in response.content:
            if block.type == "text":
                print(block.text)
        break

    if response.stop_reason == "tool_use":
        messages.append({"role": "assistant", "content": response.content})
        # Find the tool use blocks in the response and run each one.
        tool_results = [
            {
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": run_tool(block.name, block.input),
            }
            for block in response.content
            if block.type == "tool_use"
        ]

        # Push the assistant's response and our tool results
        # back into messages, then loop again so Claude can answer.
        print("response content: %s" % response.content)
        print("Tool results: %s" % tool_results)
        print("----------------------")
        messages.append({"role": "user", "content": tool_results})
