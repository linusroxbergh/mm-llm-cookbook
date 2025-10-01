from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    return client


def llm_simple_output(user_prompt: str) -> str:
    openai_client = get_openai_client()
    system_prompt = "You are a helpful assistant that tries to figure out the work role of the user based on their input. You should tell me both the work role and the confidence in percent of how sure you are."

    response = openai_client.chat.completions.parse(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
    )

    message = response.choices[0].message.content
    return message


if __name__ == "__main__":
    prompt = "today we're gonna learn about dinosaurs, kids"
    result = llm_simple_output(prompt)
    print(result)

# menti-ai example: assistant response in chat