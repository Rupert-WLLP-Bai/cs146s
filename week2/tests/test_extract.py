import pytest

from ..app.services import extract as extract_service
from ..app.services.extract import (
    LLMExtractionError,
    extract_action_items,
    extract_action_items_llm,
)


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


def test_extract_action_items_llm_with_bullets(monkeypatch: pytest.MonkeyPatch):
    class _FakeMessage:
        content = '{"items": ["Set up database", "Write tests", "set up database"]}'

    class _FakeResponse:
        message = _FakeMessage()

    def fake_chat(**kwargs):
        assert kwargs["model"]
        assert kwargs["format"]
        return _FakeResponse()

    monkeypatch.setattr(extract_service, "chat", fake_chat)
    items = extract_action_items_llm("- [ ] Set up database\n- Write tests")
    assert items == ["Set up database", "Write tests"]


def test_extract_action_items_llm_with_keywords(monkeypatch: pytest.MonkeyPatch):
    class _FakeMessage:
        content = '{"items": ["TODO: refactor db layer", "ACTION: add endpoint"]}'

    class _FakeResponse:
        message = _FakeMessage()

    monkeypatch.setattr(extract_service, "chat", lambda **_: _FakeResponse())
    items = extract_action_items_llm("TODO: refactor db layer\nACTION: add endpoint")
    assert items == ["TODO: refactor db layer", "ACTION: add endpoint"]


def test_extract_action_items_llm_empty_input_does_not_call_chat(monkeypatch: pytest.MonkeyPatch):
    def fake_chat(**_):
        raise AssertionError("chat should not be called on empty input")

    monkeypatch.setattr(extract_service, "chat", fake_chat)
    assert extract_action_items_llm("   ") == []


def test_extract_action_items_llm_invalid_json_raises(monkeypatch: pytest.MonkeyPatch):
    class _FakeMessage:
        content = "not-json"

    class _FakeResponse:
        message = _FakeMessage()

    monkeypatch.setattr(extract_service, "chat", lambda **_: _FakeResponse())
    with pytest.raises(LLMExtractionError):
        extract_action_items_llm("Draft notes")
