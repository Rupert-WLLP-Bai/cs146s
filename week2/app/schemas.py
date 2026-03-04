from __future__ import annotations

from pydantic import BaseModel


class ExtractRequest(BaseModel):
    text: str
    save_note: bool = False


class ExtractedItem(BaseModel):
    id: int
    text: str


class ExtractResponse(BaseModel):
    note_id: int | None
    items: list[ExtractedItem]


class ActionItemRead(BaseModel):
    id: int
    note_id: int | None
    text: str
    done: bool
    created_at: str


class MarkDoneRequest(BaseModel):
    done: bool = True


class MarkDoneResponse(BaseModel):
    id: int
    done: bool


class NoteCreate(BaseModel):
    content: str


class NoteRead(BaseModel):
    id: int
    content: str
    created_at: str
