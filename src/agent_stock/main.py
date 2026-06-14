from __future__ import annotations

import json
import logging

from fastapi import FastAPI, HTTPException
from pydantic_ai.messages import ModelRequest, ModelResponse, UserPromptPart, TextPart
from sse_starlette.sse import EventSourceResponse

from agent_stock.agent import stock_agent
from agent_stock.config import settings
from agent_stock.schemas import ChatRequest, ChatHistoryMessage

logger = logging.getLogger("agent-stock")

app = FastAPI(title="Agent Stock API", version="0.1.0")


def _build_message_history(history: list[ChatHistoryMessage]) -> list[ModelRequest | ModelResponse]:
    """Convert ChatHistoryMessage list to Pydantic AI message_history format."""
    messages = []
    for msg in history:
        if msg.role == "user":
            messages.append(ModelRequest(parts=[UserPromptPart(content=msg.content)]))
        elif msg.role == "assistant":
            messages.append(ModelResponse(parts=[TextPart(content=msg.content)]))
    return messages


async def _stream_chat(request: ChatRequest):
    """Generator that yields SSE events from the AI agent."""
    message_history = _build_message_history(request.history)

    try:
        async with stock_agent.run_stream(
            request.message,
            message_history=message_history if message_history else None,
        ) as result:
            async for token in result.stream_text(delta=True):
                yield {
                    "event": "message",
                    "data": json.dumps({"type": "token", "content": token}, ensure_ascii=False),
                }

            yield {
                "event": "message",
                "data": json.dumps({"type": "done"}, ensure_ascii=False),
            }
    except Exception:
        logger.exception("Chat stream error")
        yield {
            "event": "message",
            "data": json.dumps({"type": "error", "content": "AI 服务处理出错，请稍后重试"}, ensure_ascii=False),
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
