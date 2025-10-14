# utils/ai_client.py
import asyncio
import base64
from goldmansachs.openai import OpenAI

client = OpenAI()
MODEL = 'meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8'

async def ai_analyze_text(input_data, prompt):
    """Run AI on input data asynchronously."""
    try:
        completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "text", "text": str(input_data)}
                ]
            }],
            model=MODEL
        )
        return completion.choices[0].message.content.splitlines()
    except Exception as e:
        print(f"[AIClient] Error: {e}")
        return []
