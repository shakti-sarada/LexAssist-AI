from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1"
)


def rewrite_query(query, domain):
    prompt = f"""
You are a legal query optimizer.

Convert the user query into legal search terms.

DO NOT explain.
ONLY return improved search query.

Domain: {domain}

User Query:
{query}
"""

    try:
        res = client.chat.completions.create(
            model="meta/llama3-70b-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return res.choices[0].message.content.strip()

    except:
        return query  # fallback