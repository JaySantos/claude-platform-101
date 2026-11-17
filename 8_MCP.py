import json
import os

import anthropic
from dotenv import load_dotenv

load_dotenv(".env.local")  # loads the file's variables into os.environ

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

response = client.beta.messages.create(
    model="claude-opus-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "What tools do you have available?"}],
    mcp_servers=[
        {
            "type": "url",
            "url": "https://mcpplaygroundonline.com/mcp-complex-server",
            "name": "mcp-playground-online",
        }
    ],
    tools=[
        {
            "type": "mcp_toolset",
            "mcp_server_name": "mcp-playground-online",
        }
    ],
    betas=["mcp-client-2025-11-20"],
)

print(json.dumps(response.model_dump(), indent=2))

# messages = [{"role": "user", "content": "What is Anthropic latest model release?"}]

# # The agent loop. Each iteration sends messages to Claude
# # and switches on the response's stop reason.

# search_response = client.messages.create(
#     model="claude-opus-5",
#     max_tokens=1024,
#     tools=[{"type": "web_search_20260209", "name": "web_search"}],
#     messages=messages,
# )

# for block in search_response.content:
#     if block.type == "server_tool_use":
#         print(f"Tool call: {block.name} — {block.input}")
#     elif block.type == "text":
#         print(block.text)

# # Call 2: code execution — Claude writes and runs Python in a sandbox
# code_response = client.messages.create(
#     model="claude-opus-5",
#     max_tokens=1024,
#     tools=[{"type": "code_execution_20260120", "name": "code_execution"}],
#     messages=[
#         {
#             "role": "user",
#             "content": "Calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]",
#         }
#     ],
# )

# for block in code_response.content:
#     if block.type == "server_tool_use":
#         print(f"Tool call: {block.name} — {block.input}")
#     elif block.type == "bash_code_execution_tool_result":
#         print(f"stdout: {block.content.stdout}")
#     elif block.type == "text":
#         print(block.text)
