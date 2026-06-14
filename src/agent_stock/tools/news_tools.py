from __future__ import annotations

import json
import logging
import re

from agent_stock.config import settings
from agent_stock.tools.stock_tools import get_http_client, _auth_headers

logger = logging.getLogger(__name__)

_STOCK_CODE_RE = re.compile(r"^\d{6}\.(SZ|SH|BJ)$")


def _validate_stock_code(stock_code: str) -> str | None:
    """Validate stock code format. Returns error message if invalid, None if OK."""
    if not _STOCK_CODE_RE.match(stock_code):
        return f"无效的股票代码格式: {stock_code}，正确格式如 000001.SZ"
    return None


async def get_stock_news(stock_code: str) -> str:
    """获取指定股票的新闻资讯。参数stock_code为股票代码（如 000001.SZ）。"""
    if err := _validate_stock_code(stock_code):
        return json.dumps({"error": err}, ensure_ascii=False)
    try:
        client = await get_http_client()
        resp = await client.get(f"{settings.stock_api_url}/api/news/{stock_code}", headers=_auth_headers())
        resp.raise_for_status()
        return json.dumps(resp.json(), ensure_ascii=False)
    except Exception:
        logger.exception("get_stock_news failed")
        return json.dumps({"error": "获取新闻失败，请稍后重试"}, ensure_ascii=False)


async def get_stock_analysis(stock_code: str) -> str:
    """获取指定股票的分析结果。参数stock_code为股票代码（如 000001.SZ）。"""
    if err := _validate_stock_code(stock_code):
        return json.dumps({"error": err}, ensure_ascii=False)
    try:
        client = await get_http_client()
        resp = await client.get(f"{settings.stock_api_url}/api/analysis/{stock_code}", headers=_auth_headers())
        resp.raise_for_status()
        return json.dumps(resp.json(), ensure_ascii=False)
    except Exception:
        logger.exception("get_stock_analysis failed")
        return json.dumps({"error": "获取分析结果失败，请稍后重试"}, ensure_ascii=False)
