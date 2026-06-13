from __future__ import annotations

import json
import logging

import httpx

from agent_stock.config import settings

logger = logging.getLogger(__name__)


async def get_sim_accounts() -> str:
    """获取用户的模拟交易账户列表。返回所有模拟账户的JSON数据，包含账户ID、名称、资金等。"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{settings.stock_api_url}/api/quant/sim/accounts")
            resp.raise_for_status()
            return json.dumps(resp.json(), ensure_ascii=False)
    except Exception as e:
        logger.exception("get_sim_accounts failed")
        return json.dumps({"error": f"获取模拟账户失败: {e}"}, ensure_ascii=False)


async def get_account_positions(account_id: int) -> str:
    """获取指定模拟账户的持仓信息。参数account_id为账户ID。"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{settings.stock_api_url}/api/quant/sim/{account_id}/positions")
            resp.raise_for_status()
            return json.dumps(resp.json(), ensure_ascii=False)
    except Exception as e:
        logger.exception("get_account_positions failed")
        return json.dumps({"error": f"获取持仓失败: {e}"}, ensure_ascii=False)


async def get_account_orders(account_id: int) -> str:
    """获取指定模拟账户的委托记录。参数account_id为账户ID。"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{settings.stock_api_url}/api/quant/sim/{account_id}/orders")
            resp.raise_for_status()
            return json.dumps(resp.json(), ensure_ascii=False)
    except Exception as e:
        logger.exception("get_account_orders failed")
        return json.dumps({"error": f"获取委托记录失败: {e}"}, ensure_ascii=False)
