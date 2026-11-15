"""
Temperature demo: shows how the sampling temperature changes an LLM's output.

Low temperature  -> focused, (nearly) repeatable answers
High temperature -> more varied, more surprising answers
"""

import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_ollama import ChatOllama

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from configurations import http_config

load_dotenv()

MODEL = "qwen3.5:4b"
PROMPT = "Suggest a creative name for a coffee shop on the moon."
TEMPERATURES = [0.0, 0.7, 1.5]
RUNS_PER_TEMPERATURE = 3


def main():
    print(f"Prompt: {PROMPT}")

    for temperature in TEMPERATURES:
        model = ChatOllama(model=MODEL, temperature=temperature)

        print(f"\n=== Temperature {temperature} ===")
        for run in range(1, RUNS_PER_TEMPERATURE + 1):
            response = model.invoke(PROMPT)
            print(f"  Run {run}: {response.text.strip()}")


if __name__ == "__main__":
    main()