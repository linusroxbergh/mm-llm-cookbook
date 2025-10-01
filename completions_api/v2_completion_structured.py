from openai import OpenAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    return client


class UserRole(BaseModel):
    work_role: str
    confidence: int

def llm_structured_output(user_prompt: str) -> str:
    openai_client = get_openai_client()
    system_prompt = "You are a helpful assistant that tries to figure out the work role of the user based on their input. You should tell me both the work role and the confidence in percent of how sure you are."
    model = "gpt-4.1"

    response = openai_client.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        response_format=UserRole
    )

    message = response.choices[0].message.parsed
    return message


if __name__ == "__main__":
    prompt = "today we're gonna learn about dinosaurs, kids"
    result = llm_structured_output(prompt)
    print(result)