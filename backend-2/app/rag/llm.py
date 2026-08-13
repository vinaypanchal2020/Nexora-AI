import os
from dotenv import load_dotenv
from groq import AsyncGroq

load_dotenv()

client = AsyncGroq(
    api_key = os.environ.get("GROQ_API_KEY")
)

async def generate_response(prompt: str, history=None) -> str:
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        }
    ]

    if history:
        for entry in history:
            role = entry.get("role") if isinstance(entry, dict) else None
            content = entry.get("content") if isinstance(entry, dict) else None
            if role in {"user", "assistant"} and isinstance(content, str):
                messages.append({"role": role, "content": content})

    messages.append({
        "role": "user",
        "content": prompt
    })

    response = await client.chat.completions.create(
        model=os.environ.get("GROQ_MODEL"),
        messages=messages
    )

    return response.choices[0].message.content