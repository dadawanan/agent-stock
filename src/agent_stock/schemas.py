from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class ChatHistoryMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatHistoryMessage] = []


class ChatChunk(BaseModel):
    type: Literal["token", "done", "error"]
    content: str = ""
