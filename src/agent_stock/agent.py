from __future__ import annotations

import json

from pydantic_ai import Agent, RunContext

from agent_stock.tools.stock_tools import get_popular_stocks, get_stock_list
from agent_stock.tools.account_tools import get_sim_accounts, get_account_positions, get_account_orders
from agent_stock.tools.news_tools import get_stock_news, get_stock_analysis
from agent_stock.tools.analysis_tools import get_strategies, get_backtest_results, get_stock_price

SYSTEM_PROMPT = """你是A股智能助手，一位专业的金融分析师。

你的职责：
1. 回答用户关于A股市场的问题
2. 帮助用户查询热门股票、行情数据、新闻资讯
3. 帮助用户了解模拟交易账户状态
4. 分析股票数据，提供专业的投资见解

回答风格：
- 专业、简洁、有数据支撑
- 使用中文回答
- 引用具体数据时说明数据来源
- 不提供具体的买卖建议，只提供分析和参考信息

你可以调用工具获取实时数据。当用户问到具体股票时，优先调用工具获取最新数据再回答。"""

stock_agent = Agent(
    "openai:gpt-4o",
    system_prompt=SYSTEM_PROMPT,
    retries=2,
)


@stock_agent.tool
async def tool_get_popular_stocks(ctx: RunContext) -> str:
    """获取今日A股热门股票排行。返回同花顺人气榜Top200的JSON数据。"""
    return await get_popular_stocks()


@stock_agent.tool
async def tool_get_stock_list(ctx: RunContext) -> str:
    """获取所有股票列表。返回数据库中所有股票代码和名称。"""
    return await get_stock_list()


@stock_agent.tool
async def tool_get_sim_accounts(ctx: RunContext) -> str:
    """获取用户的模拟交易账户列表。"""
    return await get_sim_accounts()


@stock_agent.tool
async def tool_get_account_positions(ctx: RunContext, account_id: int) -> str:
    """获取指定模拟账户的持仓信息。

    Args:
        account_id: 账户ID
    """
    return await get_account_positions(account_id)


@stock_agent.tool
async def tool_get_account_orders(ctx: RunContext, account_id: int) -> str:
    """获取指定模拟账户的委托记录。

    Args:
        account_id: 账户ID
    """
    return await get_account_orders(account_id)


@stock_agent.tool
async def tool_get_stock_news(ctx: RunContext, stock_code: str) -> str:
    """获取指定股票的新闻资讯。

    Args:
        stock_code: 股票代码，格式如 000001.SZ
    """
    return await get_stock_news(stock_code)


@stock_agent.tool
async def tool_get_stock_analysis(ctx: RunContext, stock_code: str) -> str:
    """获取指定股票的分析结果。

    Args:
        stock_code: 股票代码，格式如 000001.SZ
    """
    return await get_stock_analysis(stock_code)


@stock_agent.tool
async def tool_get_strategies(ctx: RunContext) -> str:
    """获取所有量化策略列表。"""
    return await get_strategies()


@stock_agent.tool
async def tool_get_backtest_results(ctx: RunContext) -> str:
    """获取回测结果列表。"""
    return await get_backtest_results()


@stock_agent.tool
async def tool_get_stock_price(ctx: RunContext, stock_code: str) -> str:
    """获取股票实时行情。

    Args:
        stock_code: 股票代码，格式如 000001.SZ
    """
    return await get_stock_price(stock_code)
