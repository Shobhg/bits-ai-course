import os
from dotenv import load_dotenv

load_dotenv()

PROVIDER=os.getenv("LLM_PROVIDER", "openai")
MODEL= os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

def generate(task_prompt: str, user_text: str) -> dict:
    """
    Send a completion request to the configured LLM provider
    Returns dict with 'content' and 'toekns_used' keys.
    """

    if PROVIDER == "openai":
        return _call_openai(task_prompt, user_text)
    else:
        raise ValueError(f"Unsupported provider: {PROVIDER}")




def _call_openai(task_prompt: str, user_text: str) -> dict:
    from openai import OpenAI, RateLimitError, APIConnectionError, AuthenticationError

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("API Key not configured")

    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(

            model=MODEL,
            messages=[
                {"role":"system", "content": task_prompt},
                {"role":"user", "content": user_text},
            ],
            temperature=0.7,
            max_tokens=1000,
        )
        return{
            "content": response.choices[0].message.content,
            "tokens_used":response.usage.total_tokens if response.usage else None,
        }
    except AuthenticationError:
        raise PermissionError("Invalid API key")
    except RateLimitError:
        raise RuntimeError("Rate limit exceeded. Try after sometime")
    except APIConnectionError:
        raise ConnectionError("Cannot reach the LLM API")



def get_provider_info() -> dict:
        return{"provider": PROVIDER, "model": MODEL}