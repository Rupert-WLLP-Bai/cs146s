from __future__ import annotations

import json
import os
import re
from typing import Any

from dotenv import load_dotenv
from ollama import chat

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)
DEFAULT_OLLAMA_MODEL = "llama3.1:8b"

ACTION_ITEMS_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "items": {"type": "string"},
        }
    },
    "required": ["items"],
    "additionalProperties": False,
}


class LLMExtractionError(RuntimeError):
    pass


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def _dedupe_items(items: list[str]) -> list[str]:
    # Preserve order but dedupe case-insensitively so UI does not show duplicates.
    seen: set[str] = set()
    unique: list[str] = []
    for item in items:
        cleaned = item.strip()
        if not cleaned:
            continue
        lowered = cleaned.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(cleaned)
    return unique


def extract_action_items(text: str) -> list[str]:
    lines = text.splitlines()
    extracted: list[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    return _dedupe_items(extracted)


def _extract_message_content(response: Any) -> str:
    if isinstance(response, dict):
        message = response.get("message", {})
        return str(message.get("content", ""))
    message = getattr(response, "message", None)
    if message is None:
        return ""
    content = getattr(message, "content", "")
    return content if isinstance(content, str) else ""


def extract_action_items_llm(text: str, model: str | None = None) -> list[str]:
    # Week2 TODO1: LLM extraction path with structured JSON output via Ollama.
    prompt_text = text.strip()
    if not prompt_text:
        return []

    selected_model = model or os.getenv("OLLAMA_MODEL") or DEFAULT_OLLAMA_MODEL

    try:
        response = chat(
            model=selected_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You extract actionable TODO items from notes. "
                        "Return JSON only with this shape: {\"items\": [\"...\"]}. "
                        "Do not include extra keys."
                    ),
                },
                {"role": "user", "content": prompt_text},
            ],
            format=ACTION_ITEMS_SCHEMA,
            options={"temperature": 0},
        )
    except Exception as exc:  # pragma: no cover - exercised by route integration path
        raise LLMExtractionError("Failed to call Ollama chat API") from exc

    raw_content = _extract_message_content(response)
    try:
        payload = json.loads(raw_content)
    except json.JSONDecodeError as exc:
        raise LLMExtractionError("LLM returned non-JSON content") from exc

    if not isinstance(payload, dict):
        raise LLMExtractionError("LLM returned unexpected response shape")

    raw_items = payload.get("items")
    if not isinstance(raw_items, list) or any(not isinstance(item, str) for item in raw_items):
        raise LLMExtractionError("LLM returned unexpected action item list")

    return _dedupe_items(raw_items)


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters
