from __future__ import annotations

import json
import logging

import httpx

from agent_stock.config import settings

logger = logging.getLogger(__name__)


async def get_stock_news(stock_code: str) -> str:
    """获取指定股票的新闻资讯。参数stock_code为股票代码（如 000001.SZ）。"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{settings.stock_api_url}/api/news/{stock_code}")
            resp.raise_for_status()
            return json.dumps(resp.json(), ensure_ascii=False)
    except Exception as e:
        logger.exception("get_stock_news failed")
        return json.dumps({"error": f"获取新闻失败: {e}"}, ensure_ascii=False)


async def get_stock_analysis(stock_code: str) -> str:
    """获取指定股票的分析结果。参数stock_code为股票代码（如 000001.SZ）。"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{settings.stock_api_url}/api/analysis/{stock_code}")
            resp.raise_for_status()
            return json.dumps(resp.json(), ensure_ascii=False)
    except Exception as e:
        logger.exception("get_stock_analysis failed")
        return json.dumps({"error": f"获取分析结果失败: {e}"}, ensure_ascii=False)
