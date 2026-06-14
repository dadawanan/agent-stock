from __future__ import annotations

import json
import logging

from agent_stock.config import settings
from agent_stock.tools.news_tools import _validate_stock_code
from agent_stock.tools.stock_tools import get_http_client

logger = logging.getLogger(__name__)


async def get_strategies() -> str:
    """获取所有量化策略列表。返回策略的JSON数据，包含策略ID、名称、参数等。"""
    try:
        client = await get_http_client()
        resp = await client.get(f"{settings.stock_api_url}/api/quant/strategies")
        resp.raise_for_status()
        return json.dumps(resp.json(), ensure_ascii=False)
    except Exception:
        logger.exception("get_strategies failed")
        return json.dumps({"error": "获取策略列表失败，请稍后重试"}, ensure_ascii=False)


async def get_backtest_results() -> str:
    """获取回测结果列表。返回所有回测记录的JSON数据。"""
    try:
        client = await get_http_client()
        resp = await client.get(f"{settings.stock_api_url}/api/quant/backtest/results")
        resp.raise_for_status()
        return json.dumps(resp.json(), ensure_ascii=False)
    except Exception:
        logger.exception("get_backtest_results failed")
        return json.dumps({"error": "获取回测结果失败，请稍后重试"}, ensure_ascii=False)


async def get_stock_price(stock_code: str) -> str:
    """获取股票实时行情。参数stock_code为股票代码（如 000001.SZ）。"""
    if err := _validate_stock_code(stock_code):
        return json.dumps({"error": err}, ensure_ascii=False)
    try:
        client = await get_http_client()
        resp = await client.get(
            f"{settings.stock_api_url}/api/quant/market/prices",
            params={"codes": stock_code},
        )
        resp.raise_for_status()
        return json.dumps(resp.json(), ensure_ascii=False)
    except Exception:
        logger.exception("get_stock_price failed")
        return json.dumps({"error": "获取行情失败，请稍后重试"}, ensure_ascii=False)
