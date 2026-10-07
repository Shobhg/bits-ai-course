import os
import sys
from dotenv import load_dotenv
from openai import  OpenAI,AuthenticationError, APIConnectionError

load_dotenv()

api_key=os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OPENAI_API_KEY not found!")
    sys.exit(1)


client=OpenAI(api_key=api_key)
MODEL= os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

print("Sending prompt: 'What is generation AI in one sentence?'")

try:
    response= client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a harvard university  professor. Be concise."},
            {"role": "user", "content": "What is generation AI in one sentence?"},

        ],
        temperature=0.7,
        max_tokens=100,
    )

    print(f"Response: {response.choices[0].message.content}")
    print(f"Tokens Used: {response.usage.total_tokens}")

except AuthenticationError:
    print("Error: Invalid API Key. Check your .env file. ")
except APIConnectionError:
    print("Error: Cannot Connect. Check your internet. ")
except Exception as e:
    print(f"Unexpected error: {e} ")