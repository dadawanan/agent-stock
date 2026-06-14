from __future__ import annotations

import json
import logging

from jose import jwt
from datetime import datetime, timezone, timedelta

from agent_stock.tools.stock_tools import get_http_client

logger = logging.getLogger(__name__)

# 服务级 token 缓存
_service_token: str | None = None


def _get_service_token() -> str:
    """生成一个服务级 JWT token，用于内部 API 调用。"""
    global _service_token
    if _service_token is not None:
        return _service_token
    from agent_stock.config import settings
    expire = datetime.now(timezone.utc) + timedelta(hours=24)
    payload = {
        "sub": "1",
        "username": "agent-stock",
        "type": "access",
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    _service_token = jwt.encode(payload, settings.jwt_secret_key, algorithm="HS256")
    return _service_token


def _auth_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {_get_service_token()}"}


async def get_sim_accounts() -> str:
    """获取用户的模拟交易账户列表。返回所有模拟账户的JSON数据，包含账户ID、名称、资金等。"""
    try:
        from agent_stock.config import settings
        client = await get_http_client()
        resp = await client.get(f"{settings.stock_api_url}/api/quant/sim/accounts", headers=_auth_headers())
        resp.raise_for_status()
        return json.dumps(resp.json(), ensure_ascii=False)
    except Exception:
        logger.exception("get_sim_accounts failed")
        return json.dumps({"error": "获取模拟账户失败，请稍后重试"}, ensure_ascii=False)


async def get_account_positions(account_id: int) -> str:
    """获取指定模拟账户的持仓信息。参数account_id为账户ID。"""
    try:
        from agent_stock.config import settings
        client = await get_http_client()
        resp = await client.get(f"{settings.stock_api_url}/api/quant/sim/{account_id}/positions", headers=_auth_headers())
        resp.raise_for_status()
        return json.dumps(resp.json(), ensure_ascii=False)
    except Exception:
        logger.exception("get_account_positions failed")
        return json.dumps({"error": "获取持仓失败，请稍后重试"}, ensure_ascii=False)


async def get_account_orders(account_id: int) -> str:
    """获取指定模拟账户的委托记录。参数account_id为账户ID。"""
    try:
        from agent_stock.config import settings
        client = await get_http_client()
        resp = await client.get(f"{settings.stock_api_url}/api/quant/sim/{account_id}/orders", headers=_auth_headers())
        resp.raise_for_status()
        return json.dumps(resp.json(), ensure_ascii=False)
    except Exception:
        logger.exception("get_account_orders failed")
        return json.dumps({"error": "获取委托记录失败，请稍后重试"}, ensure_ascii=False)
