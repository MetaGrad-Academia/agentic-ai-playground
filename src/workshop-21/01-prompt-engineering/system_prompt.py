
import sys
from pathlib import Path

from dotenv import load_dotenv
from langsmith import traceable
from ollama import chat

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from configurations import http_config  # noqa: E402, F401

load_dotenv()

chat = traceable(chat, run_type="llm", name="System Prompt Example")

question = "What is Python?"

system_prompts = {
    "Programmer": (
        "You are a software developer. "
        "Python means the PROGRAMMING LANGUAGE, not the snake. "
        "Explain it in exactly 2 short sentences."
    ),
    "Snake Catcher": (
        "You are a wildlife expert who catches snakes. "
        "Python means the ANIMAL, not the programming language. "
        "Explain the snake in exactly 2 short sentences. "
        "Do not mention software or computers."
    )
}

for role, system_prompt in system_prompts.items():
    response = chat(
        model="qwen3.5:4b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        options={
            "temperature": 0,
            
        }
    )

    print(f"\n--- {role} ---")
    print(response.message.content)
