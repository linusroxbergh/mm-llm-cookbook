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

class EducationalInput(BaseModel):
    role: str
    education_level: str
    confidence: int

HANDLE_EDU_FUNCTION = pydantic_function_tool(
        model=EducationalInput,
        name="handle_edu",
        description="If the text contains education related content, guess the role (student, teacher), education_level (elementary, middle, high, university) and the confidence in percent of how sure you are overall about your guesses",
    )

def llm_function_calls(user_prompt: str) -> str:
    openai_client = get_openai_client()
    system_prompt = "You are a helpful assistant that tries to figure out educational context. Call the appropriate function based on the user's input. If not, return the empty string 'input not relevant'."
    model = "gpt-4.1"

    response = openai_client.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        tools=[HANDLE_EDU_FUNCTION]
    )

    tool_calls = response.choices[0].message.tool_calls
    if tool_calls:
        tool_call = tool_calls[0]
        tool_name = tool_call.function.name
        tool_arguments = json.loads(tool_call.function.arguments)
        print(f"Tool name: {tool_name}")
        print(f"Tool arguments: {tool_arguments}")
        print("--------------------------------")
        if tool_name == "handle_edu":
            # here we want to do stuff
    content = response.choices[0].message.content
    print(content)
    return content, tool_calls


if __name__ == "__main__":
    #prompt = "asdqwdwq"
    prompt = "today we're gonna learn about dinosaurs, kids"
    result, tool_calls = llm_function_calls(prompt)




# notes:
# if edu, save to csv, create headers etc

