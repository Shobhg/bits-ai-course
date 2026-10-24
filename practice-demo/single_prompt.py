import os
import sys
from dotenv import load_dotenv
from openai import OpenAI, APIConnectionError, AuthenticationError

load_dotenv()

api_key=os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OPENAI_API_KEY not found!")
    sys.exit(1)

client=OpenAI(api_key=api_key)
MODEL= os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


print("Sending prompt:'")

try:
    response= client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Can you summarize, extract keywords and  give a headline to following text: LangGraph acts as a highly customizable state-machine framework for LLMs, built on three core pillars: state management, nodes, and edges. At its heart lies the StateGraph, a centralized, thread-safe memory object that stores the shared application state and allows specialized computing nodes (Python functions representing agents or tasks) to read from and modify data seamlessly. Unlike traditional linear pipeline tools, execution pathways in LangGraph are governed by both static and conditional edges. These conditional edges evaluate the live state at runtime to route execution dynamically, which natively empowers developers to build complex, cyclical reflection loops where AI agents can autonomously review, critique, and correct their own code or text outputs before finalizing a task. Furthermore, the framework provides built-in persistence layers for automatic step checkpointing, native node-by-node token streaming, and human-in-the-loop interrupt triggers. These primitives allow developers to pause execution for human verification or state modification, providing the granular architectural control and system resilience required to safely scale experimental multi-agent prototypes into production-grade enterprise software."},

        ],
        temperature=0.1,
        max_tokens=1000,
    )

    print(f"Response: {response.choices[0].message.content}")
    print(f"Tokens Used: {response.usage.total_tokens}")

except AuthenticationError:
    print("Error: Invalid API Key. Check your .env file. ")
except APIConnectionError:
    print("Error: Cannot Connect. Check your internet. ")
except Exception as e:
    print(f"Unexpected error: {e} ")
