from __future__ import annotations

import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path


backend_dir = Path(__file__).resolve().parent.parent # 根據你的目錄結構調整
PROMPT_DIR = backend_dir / "prompts"
load_dotenv(backend_dir / ".env")


def load_prompt(name: str) -> str:
    prompt_file = PROMPT_DIR / f"{name}.md"
    return prompt_file.read_text(encoding="utf-8")


def _resolve_api_key(provider: str) -> str:
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY", "")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required in environment")
        return api_key
    raise ValueError(f"Unsupported provider: {provider}")


def generate_with_openai(*, model: str, system_prompt: str, user_prompt: str) -> str:
    """Call OpenAI Responses API using server-side API key from environment."""
    try:
        api_token = _resolve_api_key("openai")

        client = OpenAI(api_key=api_token)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=900,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"LLM Error: {e}")
        return (
            "[LLM_FALLBACK]\n"
            f"system={system_prompt[:120]}...\n"
            f"user={user_prompt[:220]}..."
        )


def default_model(provider: str) -> str:
    if provider == "openai":
        return os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    return "gpt-4.1-mini"
