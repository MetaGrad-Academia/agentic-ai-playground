import sys
from pathlib import Path

from dotenv import load_dotenv
from langsmith import traceable
from ollama import chat

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from configurations import http_config  # noqa: E402, F401

load_dotenv()

chat = traceable(chat, run_type="llm", name="Temperature Example")

prompt = (
    "Invent a brand-new flavor of ice cream and describe it in one short sentence."
)

for temp in [0.0, 0.8, 2.0]:
    print(f"\n=== Temperature {temp} ===")
    for run in range(5):
        response = chat(
            model="gemma4:12b",
            messages=[{"role": "user", "content": prompt}],
            think=False,  # Prevents thinking tokens from eating your num_predict budget
            options={
                "temperature": temp,
                "num_predict": 35,
            },
        )
        clean_text = response.message.content.strip().replace("\n", " ")
        print(f"Run {run + 1}: {clean_text}")