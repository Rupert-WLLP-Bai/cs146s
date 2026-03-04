from __future__ import annotations

from collections.abc import Callable

from fastapi import APIRouter, HTTPException, Query

from .. import db
from ..schemas import (
    ActionItemRead,
    ExtractedItem,
    ExtractRequest,
    ExtractResponse,
    MarkDoneRequest,
    MarkDoneResponse,
)
from ..services.extract import (
    LLMExtractionError,
    extract_action_items,
    extract_action_items_llm,
)

router = APIRouter(prefix="/action-items", tags=["action-items"])


def _extract_and_store(text: str, save_note: bool, extractor: Callable[[str], list[str]]) -> ExtractResponse:
    # Shared storage path keeps the heuristic and LLM endpoints consistent.
    items = extractor(text)
    note_id: int | None = None
    if save_note:
        note_id = db.insert_note(text)
    ids = db.insert_action_items(items, note_id=note_id)
    return ExtractResponse(
        note_id=note_id,
        items=[
            ExtractedItem(id=item_id, text=item_text)
            for item_id, item_text in zip(ids, items, strict=True)
        ],
    )


@router.post("/extract", response_model=ExtractResponse)
def extract(payload: ExtractRequest) -> ExtractResponse:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")
    return _extract_and_store(text, payload.save_note, extract_action_items)


@router.post("/extract-llm", response_model=ExtractResponse)
def extract_llm(payload: ExtractRequest) -> ExtractResponse:
    # Week2 TODO4: Expose dedicated LLM extraction endpoint.
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")
    try:
        return _extract_and_store(text, payload.save_note, extract_action_items_llm)
    except LLMExtractionError as exc:
        raise HTTPException(status_code=503, detail="LLM extraction unavailable") from exc


@router.get("", response_model=list[ActionItemRead])
def list_all(note_id: int | None = Query(default=None)) -> list[ActionItemRead]:
    rows = db.list_action_items(note_id=note_id)
    return [
        ActionItemRead(
            id=r["id"],
            note_id=r["note_id"],
            text=r["text"],
            done=bool(r["done"]),
            created_at=r["created_at"],
        )
        for r in rows
    ]


@router.post("/{action_item_id}/done", response_model=MarkDoneResponse)
def mark_done(action_item_id: int, payload: MarkDoneRequest) -> MarkDoneResponse:
    updated = db.mark_action_item_done(action_item_id, payload.done)
    if not updated:
        raise HTTPException(status_code=404, detail="action item not found")
    return MarkDoneResponse(id=action_item_id, done=payload.done)
