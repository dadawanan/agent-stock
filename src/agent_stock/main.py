from __future__ import annotations

import json
import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

from agent_stock.agent import stock_agent
from agent_stock.config import settings
from agent_stock.schemas import ChatRequest, ChatHistoryMessage

logger = logging.getLogger("agent-stock")

app = FastAPI(title="Agent Stock API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _build_message_history(history: list[ChatHistoryMessage]) -> list[dict[str, str]]:
    """Convert ChatHistoryMessage list to Pydantic AI message_history format."""
    return [{"role": msg.role, "content": msg.content} for msg in history]


async def _stream_chat(request: ChatRequest):
    """Generator that yields SSE events from the AI agent."""
    message_history = _build_message_history(request.history)

    try:
        async with stock_agent.run_stream(
            request.message,
            message_history=message_history if message_history else None,
        ) as result:
            async for token in result.stream_text():
                yield {
                    "event": "message",
                    "data": json.dumps({"type": "token", "content": token}, ensure_ascii=False),
                }

            yield {
                "event": "message",
                "data": json.dumps({"type": "done"}, ensure_ascii=False),
            }
    except Exception as e:
        logger.exception("Chat stream error")
        yield {
            "event": "message",
            "data": json.dumps({"type": "error", "content": str(e)}, ensure_ascii=False),
        }


@app.post("/api/chat/stream")
async def api_chat_stream(request: ChatRequest):
    """SSE streaming chat endpoint."""
    return EventSourceResponse(_stream_chat(request))


@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "agent-stock"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.agent_host, port=settings.agent_port)
