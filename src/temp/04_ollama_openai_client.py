from ollama import chat

MODEL = "qwen3.5:4b"

response = chat(
    model="qwen3.5:4b",
    messages=[
        {"role": "user", "content": "Suggest a creative name for a coffee shop on the moon."}
    ],
)


print(response.message.content)