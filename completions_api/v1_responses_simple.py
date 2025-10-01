from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    return client


def llm_simple_output(user_prompt: str) -> str:
    client = get_openai_client()
    system_prompt = "You are a helpful assistant that tries to figure out the work role of the user based on their input. You should tell me both the work role and the confidence in percent of how sure you are."
    model = "gpt-5"

    response = client.responses.create(
        model=model,
        instructions=system_prompt,
        input=user_prompt,
        reasoning={
            "effort": "minimal"
        },
    )

    message = response.output_text
    return message


if __name__ == "__main__":
    prompt = "today we're gonna learn about dinosaurs, kids"
    result = llm_simple_output(prompt)
    print(result)