from __future__ import annotations

import json
import logging

import httpx

from agent_stock.config import settings

logger = logging.getLogger(__name__)

# Shared HTTP client with connection pooling
_http_client: httpx.AsyncClient | None = None


async def get_http_client() -> httpx.AsyncClient:
    global _http_client
    if _http_client is None or _http_client.is_closed:
        _http_client = httpx.AsyncClient(timeout=10.0)
    return _http_client


async def get_popular_stocks() -> str:
    """获取今日A股热门股票排行。返回同花顺人气榜Top200的JSON数据，包含股票代码、名称、排名等。"""
    try:
        client = await get_http_client()
        resp = await client.get(f"{settings.stock_api_url}/api/popularity/latest")
        resp.raise_for_status()
        data = resp.json()
        return json.dumps(data, ensure_ascii=False)
    except Exception:
        logger.exception("get_popular_stocks failed")
        return json.dumps({"error": "获取热门股票失败，请稍后重试"}, ensure_ascii=False)


async def get_stock_list() -> str:
    """获取所有股票列表。返回数据库中所有股票代码和名称的JSON数据。"""
    try:
        client = await get_http_client()
        resp = await client.get(f"{settings.stock_api_url}/api/stocks")
        resp.raise_for_status()
        data = resp.json()
        return json.dumps(data, ensure_ascii=False)
    except Exception:
        logger.exception("get_stock_list failed")
        return json.dumps({"error": "获取股票列表失败，请稍后重试"}, ensure_ascii=False)
