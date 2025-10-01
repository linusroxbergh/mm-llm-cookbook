from openai import OpenAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import pydantic_function_tool
import json
import csv

load_dotenv()

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    return client

client = get_openai_client()

dice_mcp = {
            "type": "mcp",
            "server_label": "dmcp",
            "server_description": "A Dungeons and Dragons MCP server to assist with dice rolling.",
            "server_url": "https://dmcp-server.deno.dev/sse",
            "require_approval": "never",
        }

resp = client.responses.create(
    model="gpt-5",
    tools=[
        dice_mcp,
    ],
    input="Roll 2d4+1",
)

print(resp.output_text)

# https://mcpservers.org/