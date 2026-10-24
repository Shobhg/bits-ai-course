import os
import sys
from dotenv import load_dotenv
from openai import OpenAI, APIConnectionError, AuthenticationError
from pathlib import Path

load_dotenv()

api_key=os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OPENAI_API_KEY not found!")
    sys.exit(1)

client=OpenAI(api_key=api_key)
MODEL= os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

PROMPT_DIR = Path("prompts")
TEXT_FILE = Path("long_text.txt")



def load_text(filepath):
    if not filepath.exists():
        raise FileNotFoundError(
            f"Long Text File not found: {filepath}"
        )
    return filepath.read_text(encoding="utf-8").strip()



def load_prompt(prompt_name, **variables):
    prompt_file = PROMPT_DIR / prompt_name
    if not prompt_file.exists():
            raise FileNotFoundError(
                f"Fle not found: {prompt_file}"
            )
    template  = prompt_file.read_text(encoding="utf-8").strip()
    return template.format(**variables)



print("Sending prompt:'")

def call_llm(prompt: str, temperature: float = 0.1) -> tuple[str, int]:
    """Call the LLM and return (respnse_text, tokens_user)."""
    
    try:

        response= client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=1000,
            )
        tokens = response.usage.total_tokens

        text = response.choices[0].message.content
      
        return text, tokens
    
    except AuthenticationError:
        print("Error: Invalid API Key. Check your .env file. ")
    except APIConnectionError:
        print("Error: Cannot Connect. Check your internet. ")
    except Exception as e:
        print(f"Unexpected error: {e} ")




try:

    text = load_text(TEXT_FILE)
    print (f"Loaded Text from {TEXT_FILE}")
    print(f"Characters: {len(text)}")


    summarize_prompt = load_prompt("summarize_v1.txt", text=text)

    print("\n ---------SUMMARIZATION PROMPT----------")
    print(summarize_prompt)

    response = call_llm(summarize_prompt)

    print ("\n-----------SUMMARY ---------")
    print(response[0])
    print ("\n-----------TOKENS USED FOR SUMMARY ---------")
    print(response[1])



    keyword_prompt = load_prompt("extract_keywords.txt", text=text)

    print("\n ---------KEYWORD PROMPT----------")
    print(keyword_prompt)

    response = call_llm(keyword_prompt)

    print ("\n-----------KEYWORD ---------")
    print(response[0])
    print ("\n-----------TOKENS USED FOR KEYWORD ---------")
    print(response[1])




    headline_prompt = load_prompt("headline.txt", text=text)

    print("\n ---------HEADLINE PROMPT----------")
    print(headline_prompt)

    response = call_llm(headline_prompt)

    print ("\n-----------HEADLINE ---------")
    print(response[0])
    print ("\n-----------TOKENS USED FOR HEADLINE ---------")
    print(response[1])


except Exception as e:
    print(f"Unexpected error: {e} ")



