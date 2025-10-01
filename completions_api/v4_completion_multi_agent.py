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

class TranslationInput(BaseModel):
    original_text: str
    english_translation: str

HANDLE_TRANSLATION_FUNCTION = pydantic_function_tool(
        model=TranslationInput,
        name="handle_translation",
        description="If the text contains swedish related content, translate it to english along with the original content",
    )


def poet_agent(tool_arguments):
    print("Poet agent is called")
    openai_client = get_openai_client()
    system_prompt = "You are great at writing poems that contains two languages. Take the user input in both languages and write a short poem that mixes both languages in a beautiful way."
    user_prompt = tool_arguments["original_text"] + "\n" + tool_arguments["english_translation"]
    
    model = "gpt-4.1"

    response = openai_client.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
    )

    message = response.choices[0].message.content

    with open("poem.txt", "a") as f:
        f.write(message + "\n")
        f.write("--------------------------------\n")
    

def llm_multi_agent(user_prompt: str) -> str:
    openai_client = get_openai_client()
    system_prompt = "You are a helpful assistant that tries to figure out educational context and if its NOT in english. Call the appropriate function based on the user's input. If not, return the empty string 'input not relevant'. call handle_translation if the input is in another language than english."
    model = "gpt-4.1"

    response = openai_client.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        tools=[HANDLE_EDU_FUNCTION, HANDLE_TRANSLATION_FUNCTION]
    )

    tool_calls = response.choices[0].message.tool_calls
    for tool in tool_calls:
        tool_name = tool.function.name
        tool_arguments = json.loads(tool.function.arguments)
        print(f"Tool name: {tool_name}")
        print(f"Tool arguments: {tool_arguments}")
        print("--------------------------------")
        if tool_name == "handle_translation":
            poet_agent(tool_arguments)
    content = response.choices[0].message.content
    return content, tool_calls


if __name__ == "__main__":
    #prompt = "asdqwdwq"
    #prompt = "today we're gonna learn about dinosaurs, kids"
    prompt = "idag ska vi lära oss om dinosaurier för att det är kul"
    result, tool_calls = llm_multi_agent(prompt)


# add function for either tool call

