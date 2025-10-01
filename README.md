# mm-llm-cookbook

Simple LLM examples

## Setup
1. Copy `.env-example`and rename it `.env`. Replace my-open-ai-api-key with your API key
2. In the terminal in project root, run `uv sync`
3. Done!

## Running an example
In the terminal, run the following: (or replace with any of the other examples)
`uv run v1_completion_simple.py`

## Examples
- v1_completion_simple.py: chat_completions endpoint, simple API call
- v1_responses_simple.py: the new responses endpoint, simple API call
- v2_completion_structured.py: chat_completions endpoint, returns structured output
- v3_completion_function_calls.py: chat_completions endpoint, calls functions
- v4_completion_multi_agent.py: chat_completions endpoint, calls functions that contain other LLMs
- mcp_calling.py: simple responses API example calling MCP