# Agent Stock - AI智能助手服务 项目文档

## 项目概览

**项目名称**: Agent Stock (AI智能助手服务)
**项目版本**: 0.1.0
**Python版本**: >=3.12
**许可证**: Private

### 核心功能

#### 1. AI聊天助手
- 基于Pydantic AI的A股智能助手
- 理解自然语言问题
- 调用工具获取实时数据
- 提供专业的金融分析和见解

#### 2. 实时数据查询
- 热门股票排行（同花顺人气榜Top200）
- 股票列表查询
- 实时行情数据
- 股票新闻资讯
- 股票分析结果

#### 3. 模拟账户管理
- 查询模拟交易账户列表
- 查询账户持仓信息
- 查询委托记录

#### 4. 量化策略查询
- 获取策略列表
- 获取回测结果

#### 5. SSE流式响应
- 支持Server-Sent Events流式输出
- 实时返回AI生成内容
- 支持聊天历史上下文

### 项目目标
为A股投资者提供一个AI驱动的智能助手，能够理解自然语言问题并调用Stock API获取实时数据，提供专业的金融分析和见解。

---

## 项目架构

### 整体架构图
```
┌─────────────────────────────────────────────────────────────────┐
│                        用户界面                                  │
│                   (浏览器/移动端)                                 │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Agent Stock API                              │
│                   http://localhost:9002                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  POST /api/chat/stream  │  GET /api/health              │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Pydantic AI Agent                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  系统提示词: A股智能助手，专业金融分析师                      │   │
│  │  模型: mimo-v2.5-pro (OpenAI兼容接口)                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  工具注册 (10个工具)                                      │   │
│  │  ├── tool_get_popular_stocks                             │   │
│  │  ├── tool_get_stock_list                                 │   │
│  │  ├── tool_get_sim_accounts                               │   │
│  │  ├── tool_get_account_positions                          │   │
│  │  ├── tool_get_account_orders                             │   │
│  │  ├── tool_get_stock_news                                 │   │
│  │  ├── tool_get_stock_analysis                             │   │
│  │  ├── tool_get_strategies                                 │   │
│  │  ├── tool_get_backtest_results                           │   │
│  │  └── tool_get_stock_price                                │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    工具层 (Tools)                                │
│  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐        │
│  │ stock_tools   │ │ account_tools │ │ news_tools    │        │
│  │ - get_popular │ │ - get_accounts│ │ - get_news    │        │
│  │ - get_list    │ │ - get_positions│ │ - get_analysis│        │
│  └───────────────┘ └───────────────┘ └───────────────┘        │
│  ┌───────────────┐                                            │
│  │analysis_tools │                                            │
│  │ - get_strategies│                                           │
│  │ - get_backtest │                                            │
│  │ - get_price    │                                            │
│  └───────────────┘                                            │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    HTTP客户端 (httpx)                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  连接池复用 | 超时10秒 | JWT认证                          │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Stock API                                    │
│                   http://localhost:8000                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  /api/popularity/*  │  /api/analysis/*  │  /api/quant/* │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 目录结构
```
agent-stock/
├── src/agent_stock/            # 核心业务代码
│   ├── __init__.py             # 包初始化
│   ├── main.py                 # FastAPI应用入口
│   ├── agent.py                # Pydantic AI Agent定义
│   ├── config.py               # 配置管理
│   ├── schemas.py              # 数据模型定义
│   └── tools/                  # 工具函数模块
│       ├── __init__.py         # 工具模块初始化
│       ├── stock_tools.py      # 股票数据工具
│       ├── account_tools.py    # 模拟账户工具
│       ├── news_tools.py       # 新闻数据工具
│       └── analysis_tools.py   # 分析数据工具
├── tests/                      # 单元测试
├── docker-compose.yml          # Docker配置
├── Dockerfile                  # Docker构建文件
├── pyproject.toml              # Python依赖配置
├── .env.example                # 环境变量模板
├── .env                        # 环境变量配置
├── .gitignore                  # Git忽略文件
└── README.md                   # 项目说明
```

---

## 技术栈

### 核心依赖
| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.12+ | 主要编程语言 |
| FastAPI | 0.136.1+ | Web框架 |
| Pydantic AI | 0.2.0+ | AI Agent框架 |
| Pydantic | 2.0+ | 数据验证 |
| httpx | 0.27.0+ | HTTP客户端 |
| OpenAI SDK | 1.50.0+ | AI模型接口 |
| SSE-Starlette | 2.0.0+ | SSE流式响应 |
| python-jose | 3.3.0+ | JWT令牌处理 |

### 开发依赖
| 技术 | 版本 | 用途 |
|------|------|------|
| pytest | 9.0.3+ | 测试框架 |
| pytest-asyncio | 1.3.0+ | 异步测试 |
| respx | 0.21.0+ | HTTP模拟 |

### AI模型
| 模型 | 提供商 | 用途 |
|------|--------|------|
| mimo-v2.5-pro | Xiaomi (OpenAI兼容) | 主要AI模型 |

### 部署
| 工具 | 用途 |
|------|------|
| Docker | 容器化部署 |
| Uvicorn | ASGI服务器 |

---

## 文件详情

### 配置文件

#### `/pyproject.toml`
**用途**: Python项目依赖和构建配置
**关键配置**:
```toml
[project]
name = "agent-stock"
version = "0.1.0"
description = "AI 智能助手服务 - Pydantic AI Agent"
requires-python = ">=3.12"

[project.optional-dependencies]
dev = [
    "pytest>=9.0.3",
    "pytest-asyncio>=1.3.0",
    "respx>=0.21.0",
]

[tool.setuptools]
package-dir = {"" = "src"}
```

**核心依赖**:
- `pydantic-ai>=0.2.0`: AI Agent框架
- `pydantic>=2.0`: 数据验证
- `fastapi>=0.136.1`: Web框架
- `httpx>=0.27.0`: HTTP客户端
- `openai>=1.50.0`: AI模型接口
- `sse-starlette>=2.0.0`: SSE流式响应
- `python-jose[cryptography]>=3.3.0`: JWT处理

#### `/docker-compose.yml`
**用途**: Docker容器编排配置
**服务**:
```yaml
services:
  agent-stock:
    build: .
    container_name: agent-stock
    restart: always
    ports:
      - "9002:9002"
    environment:
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      OPENAI_BASE_URL: ${OPENAI_BASE_URL:-https://api.openai.com/v1}
      STOCK_API_URL: ${STOCK_API_URL:-http://host.docker.internal:8000}
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
      AGENT_PORT: 9002
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

#### `/Dockerfile`
**用途**: Docker镜像构建文件
**构建步骤**:
1. 基础镜像: python:3.12-slim
2. 安装依赖
3. 复制源码
4. 暴露端口9002
5. 启动命令: uvicorn

#### `/.env.example`
**用途**: 环境变量模板
**关键配置**:
```bash
# AI模型配置
OPENAI_API_KEY=sk-your-key-here
OPENAI_BASE_URL=https://token-plan-cn.xiaomimimo.com/v1

# Stock API地址
STOCK_API_URL=http://localhost:8000

# 服务配置
AGENT_HOST=0.0.0.0
AGENT_PORT=9002

# JWT密钥（需要与stock服务的JWT_SECRET_KEY一致）
JWT_SECRET_KEY=your_jwt_secret_key_here
```

#### `/.env`
**用途**: 环境变量配置（实际配置，已在.gitignore中）

#### `/.gitignore`
**用途**: Git忽略文件
**忽略内容**:
- `.venv/`: 虚拟环境
- `__pycache__/`: Python缓存
- `.env`: 环境变量
- `*.egg-info`: 包信息
- `.pytest_cache/`: 测试缓存

### 核心文件

#### `/src/agent_stock/__init__.py`
**用途**: 包初始化文件

#### `/src/agent_stock/main.py`
**用途**: FastAPI应用入口
**功能**:
- 创建FastAPI应用实例
- 定义SSE流式聊天接口 `/api/chat/stream`
- 定义健康检查接口 `/api/health`
- 构建消息历史格式转换
- 处理AI Agent流式响应

**代码结构**:
```python
app = FastAPI(title="Agent Stock API", version="0.1.0")

def _build_message_history(history: list[ChatHistoryMessage]) -> list:
    """将ChatHistoryMessage列表转换为Pydantic AI消息历史格式"""
    messages = []
    for msg in history:
        if msg.role == "user":
            messages.append(ModelRequest(parts=[UserPromptPart(content=msg.content)]))
        elif msg.role == "assistant":
            messages.append(ModelResponse(parts=[TextPart(content=msg.content)]))
    return messages

async def _stream_chat(request: ChatRequest):
    """从AI Agent生成SSE事件的生成器"""
    message_history = _build_message_history(request.history)
    async with stock_agent.run_stream(
        request.message,
        message_history=message_history if message_history else None,
    ) as result:
        async for token in result.stream_text(delta=True):
            yield {
                "event": "message",
                "data": json.dumps({"type": "token", "content": token}),
            }
        yield {
            "event": "message",
            "data": json.dumps({"type": "done"}),
        }

@app.post("/api/chat/stream")
async def api_chat_stream(request: ChatRequest):
    """SSE流式聊天端点"""
    return EventSourceResponse(_stream_chat(request))

@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "agent-stock"}
```

**关键接口**:
- `POST /api/chat/stream`: SSE流式聊天
  - 请求体: `ChatRequest` (message, history)
  - 响应: SSE事件流
    - `type: token` - 流式文本片段
    - `type: done` - 流式结束
    - `type: error` - 错误信息

- `GET /api/health`: 健康检查
  - 响应: `{"status": "ok", "service": "agent-stock"}`

#### `/src/agent_stock/agent.py`
**用途**: Pydantic AI Agent定义
**功能**:
- 创建OpenAI Provider（支持自定义base_url）
- 创建AI模型实例（mimo-v2.5-pro）
- 定义系统提示词
- 注册10个工具函数

**代码结构**:
```python
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

# 创建OpenAI Provider
openai_provider = OpenAIProvider(
    base_url=settings.openai_base_url,
    api_key=settings.openai_api_key,
)

# 创建AI模型
openai_model = OpenAIChatModel("mimo-v2.5-pro", provider=openai_provider)

# 创建Agent
stock_agent = Agent(
    openai_model,
    system_prompt=SYSTEM_PROMPT,
    retries=2,
)

# 注册工具
@stock_agent.tool
async def tool_get_popular_stocks(ctx: RunContext) -> str:
    """获取今日A股热门股票排行"""
    return await get_popular_stocks()

# ... 其他工具注册
```

**系统提示词**:
```
你是A股智能助手，一位专业的金融分析师。

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

你可以调用工具获取实时数据。当用户问到具体股票时，优先调用工具获取最新数据再回答。
```

**注册的工具**:
| 工具名称 | 功能 | 参数 | 返回值 |
|----------|------|------|--------|
| `tool_get_popular_stocks` | 获取热门股票排行 | 无 | JSON字符串 |
| `tool_get_stock_list` | 获取股票列表 | 无 | JSON字符串 |
| `tool_get_sim_accounts` | 获取模拟账户列表 | 无 | JSON字符串 |
| `tool_get_account_positions` | 获取账户持仓 | account_id: int | JSON字符串 |
| `tool_get_account_orders` | 获取委托记录 | account_id: int | JSON字符串 |
| `tool_get_stock_news` | 获取股票新闻 | stock_code: str | JSON字符串 |
| `tool_get_stock_analysis` | 获取股票分析 | stock_code: str | JSON字符串 |
| `tool_get_strategies` | 获取策略列表 | 无 | JSON字符串 |
| `tool_get_backtest_results` | 获取回测结果 | 无 | JSON字符串 |
| `tool_get_stock_price` | 获取实时行情 | stock_code: str | JSON字符串 |

#### `/src/agent_stock/config.py`
**用途**: 配置管理
**功能**:
- 加载.env文件
- 惰性加载环境变量
- 提供配置访问接口

**代码结构**:
```python
def _load_dotenv() -> None:
    """加载.env文件"""
    for env_path in [Path.cwd() / ".env", Path(__file__).resolve().parents[3] / ".env"]:
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                stripped = line.strip()
                if not stripped or stripped.startswith("#") or "=" not in stripped:
                    continue
                key, value = stripped.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())
            break

class Settings:
    """惰性设置：属性首次被访问时才读取环境变量"""
    
    def __init__(self) -> None:
        self._cache: dict[str, object] = {}
    
    def _get(self, key: str, loader) -> object:
        if key not in self._cache:
            self._cache[key] = loader()
        return self._cache[key]
    
    @property
    def openai_api_key(self) -> str:
        return self._get("openai_api_key", lambda: os.environ.get("OPENAI_API_KEY", ""))
    
    @property
    def openai_base_url(self) -> str:
        return self._get("openai_base_url", lambda: os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"))
    
    @property
    def stock_api_url(self) -> str:
        return self._get("stock_api_url", lambda: os.environ.get("STOCK_API_URL", "http://localhost:8000"))
    
    @property
    def agent_host(self) -> str:
        return self._get("agent_host", lambda: os.environ.get("AGENT_HOST", "0.0.0.0"))
    
    @property
    def agent_port(self) -> int:
        return self._get("agent_port", lambda: int(os.environ.get("AGENT_PORT", "8001")))
    
    @property
    def jwt_secret_key(self) -> str:
        return self._get("jwt_secret_key", lambda: os.environ.get("JWT_SECRET_KEY", "change-me-in-production"))

settings = Settings()
```

**配置项详情**:
| 配置名 | 环境变量 | 默认值 | 说明 | 是否必需 |
|--------|----------|--------|------|----------|
| openai_api_key | OPENAI_API_KEY | (空) | OpenAI API密钥 | 是 |
| openai_base_url | OPENAI_BASE_URL | https://api.openai.com/v1 | OpenAI API地址 | 否 |
| stock_api_url | STOCK_API_URL | http://localhost:8000 | Stock API地址 | 否 |
| agent_host | AGENT_HOST | 0.0.0.0 | 服务监听地址 | 否 |
| agent_port | AGENT_PORT | 8001 | 服务端口 | 否 |
| jwt_secret_key | JWT_SECRET_KEY | change-me-in-production | JWT密钥 | 否 |

#### `/src/agent_stock/schemas.py`
**用途**: Pydantic数据模型定义
**模型详情**:
```python
from typing import Literal
from pydantic import BaseModel

class ChatHistoryMessage(BaseModel):
    """聊天历史消息"""
    role: Literal["user", "assistant"]  # 角色：用户或助手
    content: str  # 消息内容

class ChatRequest(BaseModel):
    """聊天请求"""
    message: str  # 用户消息
    history: list[ChatHistoryMessage] = []  # 聊天历史（可选）

class ChatChunk(BaseModel):
    """聊天响应块"""
    type: Literal["token", "done", "error"]  # 类型：文本片段、结束、错误
    content: str = ""  # 内容
```

### 工具模块

#### `/src/agent_stock/tools/__init__.py`
**用途**: 工具模块初始化

#### `/src/agent_stock/tools/stock_tools.py`
**用途**: 股票数据工具
**功能**:
- `get_popular_stocks()`: 获取热门股票排行
- `get_stock_list()`: 获取股票列表
- `get_http_client()`: 获取共享的httpx客户端
- `_auth_headers()`: 获取认证头

**代码结构**:
```python
import json
import httpx
from agent_stock.config import settings

# 共享HTTP客户端
_http_client: httpx.AsyncClient | None = None

async def get_http_client() -> httpx.AsyncClient:
    """获取共享的httpx客户端（连接池）"""
    global _http_client
    if _http_client is None or _http_client.is_closed:
        _http_client = httpx.AsyncClient(timeout=10.0)
    return _http_client

def _auth_headers() -> dict[str, str]:
    """获取认证头"""
    from agent_stock.tools.account_tools import _get_service_token
    return {"Authorization": f"Bearer {_get_service_token()}"}

async def get_popular_stocks() -> str:
    """获取今日A股热门股票排行"""
    try:
        client = await get_http_client()
        resp = await client.get(
            f"{settings.stock_api_url}/api/popularity/latest",
            headers=_auth_headers()
        )
        resp.raise_for_status()
        data = resp.json()
        return json.dumps(data, ensure_ascii=False)
    except Exception:
        logger.exception("get_popular_stocks failed")
        return json.dumps({"error": "获取热门股票失败，请稍后重试"}, ensure_ascii=False)

async def get_stock_list() -> str:
    """获取所有股票列表"""
    try:
        client = await get_http_client()
        resp = await client.get(
            f"{settings.stock_api_url}/api/stocks",
            headers=_auth_headers()
        )
        resp.raise_for_status()
        data = resp.json()
        return json.dumps(data, ensure_ascii=False)
    except Exception:
        logger.exception("get_stock_list failed")
        return json.dumps({"error": "获取股票列表失败，请稍后重试"}, ensure_ascii=False)
```

**函数详情**:

| 函数 | 功能 | 参数 | 返回值 | 调用API |
|------|------|------|--------|---------|
| `get_http_client()` | 获取HTTP客户端 | 无 | httpx.AsyncClient | 无 |
| `_auth_headers()` | 获取认证头 | 无 | dict | 无 |
| `get_popular_stocks()` | 获取热门股票 | 无 | JSON字符串 | GET /api/popularity/latest |
| `get_stock_list()` | 获取股票列表 | 无 | JSON字符串 | GET /api/stocks |

#### `/src/agent_stock/tools/account_tools.py`
**用途**: 模拟账户工具
**功能**:
- `get_sim_accounts()`: 获取模拟账户列表
- `get_account_positions(account_id)`: 获取账户持仓
- `get_account_orders(account_id)`: 获取委托记录
- `_get_service_token()`: 生成服务级JWT token

**代码结构**:
```python
import json
from jose import jwt
from datetime import datetime, timezone, timedelta

# 服务级token缓存
_service_token: str | None = None

def _get_service_token() -> str:
    """生成服务级JWT token（用于内部API调用）"""
    global _service_token
    if _service_token is not None:
        return _service_token
    
    from agent_stock.config import settings
    expire = datetime.now(timezone.utc) + timedelta(hours=24)
    payload = {
        "sub": "45",                    # 用户ID（固定）
        "username": "agent-stock",       # 用户名（固定）
        "type": "access",
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    _service_token = jwt.encode(payload, settings.jwt_secret_key, algorithm="HS256")
    return _service_token

async def get_sim_accounts() -> str:
    """获取用户的模拟交易账户列表"""
    try:
        from agent_stock.config import settings
        client = await get_http_client()
        resp = await client.get(
            f"{settings.stock_api_url}/api/quant/sim/accounts",
            headers=_auth_headers()
        )
        resp.raise_for_status()
        return json.dumps(resp.json(), ensure_ascii=False)
    except Exception:
        logger.exception("get_sim_accounts failed")
        return json.dumps({"error": "获取模拟账户失败，请稍后重试"}, ensure_ascii=False)

async def get_account_positions(account_id: int) -> str:
    """获取指定模拟账户的持仓信息"""
    try:
        from agent_stock.config import settings
        client = await get_http_client()
        resp = await client.get(
            f"{settings.stock_api_url}/api/quant/sim/{account_id}/positions",
            headers=_auth_headers()
        )
        resp.raise_for_status()
        return json.dumps(resp.json(), ensure_ascii=False)
    except Exception:
        logger.exception("get_account_positions failed")
        return json.dumps({"error": "获取持仓失败，请稍后重试"}, ensure_ascii=False)

async def get_account_orders(account_id: int) -> str:
    """获取指定模拟账户的委托记录"""
    try:
        from agent_stock.config import settings
        client = await get_http_client()
        resp = await client.get(
            f"{settings.stock_api_url}/api/quant/sim/{account_id}/orders",
            headers=_auth_headers()
        )
        resp.raise_for_status()
        return json.dumps(resp.json(), ensure_ascii=False)
    except Exception:
        logger.exception("get_account_orders failed")
        return json.dumps({"error": "获取委托记录失败，请稍后重试"}, ensure_ascii=False)
```

**函数详情**:

| 函数 | 功能 | 参数 | 返回值 | 调用API |
|------|------|------|--------|---------|
| `_get_service_token()` | 生成JWT token | 无 | str | 无 |
| `get_sim_accounts()` | 获取模拟账户 | 无 | JSON字符串 | GET /api/quant/sim/accounts |
| `get_account_positions(account_id)` | 获取账户持仓 | account_id: int | JSON字符串 | GET /api/quant/sim/{id}/positions |
| `get_account_orders(account_id)` | 获取委托记录 | account_id: int | JSON字符串 | GET /api/quant/sim/{id}/orders |

**JWT Token详情**:
```python
{
    "sub": "45",                    # 用户ID（固定为45）
    "username": "agent-stock",       # 用户名（固定）
    "type": "access",               # Token类型
    "exp": 1718500000,              # 过期时间（24小时后）
    "iat": 1718413600               # 签发时间
}
```

#### `/src/agent_stock/tools/news_tools.py`
**用途**: 新闻数据工具
**功能**:
- `get_stock_news(stock_code)`: 获取股票新闻
- `get_stock_analysis(stock_code)`: 获取股票分析
- `_validate_stock_code(stock_code)`: 验证股票代码格式

**代码结构**:
```python
import re

_STOCK_CODE_RE = re.compile(r"^\d{6}\.(SZ|SH|BJ)$")

def _validate_stock_code(stock_code: str) -> str | None:
    """验证股票代码格式"""
    if not _STOCK_CODE_RE.match(stock_code):
        return f"无效的股票代码格式: {stock_code}，正确格式如 000001.SZ"
    return None

async def get_stock_news(stock_code: str) -> str:
    """获取指定股票的新闻资讯"""
    if err := _validate_stock_code(stock_code):
        return json.dumps({"error": err}, ensure_ascii=False)
    try:
        client = await get_http_client()
        resp = await client.get(
            f"{settings.stock_api_url}/api/news/{stock_code}",
            headers=_auth_headers()
        )
        resp.raise_for_status()
        return json.dumps(resp.json(), ensure_ascii=False)
    except Exception:
        logger.exception("get_stock_news failed")
        return json.dumps({"error": "获取新闻失败，请稍后重试"}, ensure_ascii=False)

async def get_stock_analysis(stock_code: str) -> str:
    """获取指定股票的分析结果"""
    if err := _validate_stock_code(stock_code):
        return json.dumps({"error": err}, ensure_ascii=False)
    try:
        client = await get_http_client()
        resp = await client.get(
            f"{settings.stock_api_url}/api/analysis/{stock_code}",
            headers=_auth_headers()
        )
        if resp.status_code == 404:
            return json.dumps({"message": f"{stock_code} 暂无分析数据，请先运行分析"}, ensure_ascii=False)
        resp.raise_for_status()
        return json.dumps(resp.json(), ensure_ascii=False)
    except Exception:
        logger.exception("get_stock_analysis failed")
        return json.dumps({"error": "获取分析结果失败，请稍后重试"}, ensure_ascii=False)
```

**函数详情**:

| 函数 | 功能 | 参数 | 返回值 | 调用API |
|------|------|------|--------|---------|
| `_validate_stock_code(stock_code)` | 验证股票代码 | stock_code: str | str \| None | 无 |
| `get_stock_news(stock_code)` | 获取股票新闻 | stock_code: str | JSON字符串 | GET /api/news/{stock_code} |
| `get_stock_analysis(stock_code)` | 获取股票分析 | stock_code: str | JSON字符串 | GET /api/analysis/{stock_code} |

**股票代码格式**:
- 深圳: 000001.SZ
- 上海: 600036.SH
- 北京: 830799.BJ

#### `/src/agent_stock/tools/analysis_tools.py`
**用途**: 分析数据工具
**功能**:
- `get_strategies()`: 获取策略列表
- `get_backtest_results()`: 获取回测结果
- `get_stock_price(stock_code)`: 获取实时行情

**代码结构**:
```python
async def get_strategies() -> str:
    """获取所有量化策略列表"""
    try:
        client = await get_http_client()
        resp = await client.get(
            f"{settings.stock_api_url}/api/quant/strategies",
            headers=_auth_headers()
        )
        resp.raise_for_status()
        return json.dumps(resp.json(), ensure_ascii=False)
    except Exception:
        logger.exception("get_strategies failed")
        return json.dumps({"error": "获取策略列表失败，请稍后重试"}, ensure_ascii=False)

async def get_backtest_results() -> str:
    """获取回测结果列表"""
    try:
        client = await get_http_client()
        resp = await client.get(
            f"{settings.stock_api_url}/api/quant/backtest/results",
            headers=_auth_headers()
        )
        resp.raise_for_status()
        return json.dumps(resp.json(), ensure_ascii=False)
    except Exception:
        logger.exception("get_backtest_results failed")
        return json.dumps({"error": "获取回测结果失败，请稍后重试"}, ensure_ascii=False)

async def get_stock_price(stock_code: str) -> str:
    """获取股票实时行情"""
    if err := _validate_stock_code(stock_code):
        return json.dumps({"error": err}, ensure_ascii=False)
    try:
        client = await get_http_client()
        resp = await client.get(
            f"{settings.stock_api_url}/api/quant/market/prices",
            params={"codes": stock_code},
            headers=_auth_headers(),
        )
        resp.raise_for_status()
        return json.dumps(resp.json(), ensure_ascii=False)
    except Exception:
        logger.exception("get_stock_price failed")
        return json.dumps({"error": "获取行情失败，请稍后重试"}, ensure_ascii=False)
```

**函数详情**:

| 函数 | 功能 | 参数 | 返回值 | 调用API |
|------|------|------|--------|---------|
| `get_strategies()` | 获取策略列表 | 无 | JSON字符串 | GET /api/quant/strategies |
| `get_backtest_results()` | 获取回测结果 | 无 | JSON字符串 | GET /api/quant/backtest/results |
| `get_stock_price(stock_code)` | 获取实时行情 | stock_code: str | JSON字符串 | GET /api/quant/market/prices |

---

## 环境变量配置

### 必需配置
```bash
# AI模型配置
OPENAI_API_KEY=sk-your-key-here
OPENAI_BASE_URL=https://token-plan-cn.xiaomimimo.com/v1

# Stock API地址
STOCK_API_URL=http://localhost:8000

# JWT密钥（需要与stock服务的JWT_SECRET_KEY一致）
JWT_SECRET_KEY=your_jwt_secret_key_here
```

### 可选配置
```bash
# 服务配置
AGENT_HOST=0.0.0.0
AGENT_PORT=9002
```

### Docker环境配置
```bash
# Docker环境使用host.docker.internal访问宿主机
STOCK_API_URL=http://host.docker.internal:8000
```

### 配置说明
| 配置项 | 说明 | 默认值 | 是否必需 |
|--------|------|--------|----------|
| OPENAI_API_KEY | AI模型API密钥 | (空) | 是 |
| OPENAI_BASE_URL | AI模型API地址 | https://api.openai.com/v1 | 否 |
| STOCK_API_URL | Stock API地址 | http://localhost:8000 | 否 |
| AGENT_HOST | 服务监听地址 | 0.0.0.0 | 否 |
| AGENT_PORT | 服务端口 | 9002 | 否 |
| JWT_SECRET_KEY | JWT密钥 | change-me-in-production | 否 |

---

## 快速开始

### 环境要求
- Python 3.12+
- Stock API服务（端口8000）

### 安装
```bash
# 克隆项目
git clone <repo-url>
cd agent-stock

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -e .
```

### 配置
```bash
# 复制环境变量
cp .env.example .env

# 编辑 .env 填写配置
# 必需: OPENAI_API_KEY, JWT_SECRET_KEY
# 可选: STOCK_API_URL (如果Stock API不在localhost:8000)
```

### 启动服务
```bash
# 直接运行
python -m agent_stock.main

# 或使用uvicorn
uvicorn agent_stock.main:app --host 0.0.0.0 --port 9002

# Docker方式
docker-compose up -d
```

### 访问
- API文档: http://localhost:9002/docs
- 健康检查: http://localhost:9002/api/health

---

## API接口列表

### 聊天接口
- `POST /api/chat/stream` - SSE流式聊天
  - 请求体:
    ```json
    {
      "message": "今天热门股票有哪些？",
      "history": [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好！我是A股智能助手。"}
      ]
    }
    ```
  - 响应: SSE事件流
    ```
    event: message
    data: {"type": "token", "content": "根据"}

    event: message
    data: {"type": "token", "content": "最新"}

    event: message
    data: {"type": "token", "content": "的"}

    event: message
    data: {"type": "token", "content": "数据"}

    ...

    event: message
    data: {"type": "done"}
    ```

### 健康检查
- `GET /api/health` - 健康检查
  - 响应:
    ```json
    {
      "status": "ok",
      "service": "agent-stock"
    }
    ```

---

## 工具使用示例

### 1. 查询热门股票
**用户输入**: "今天热门股票有哪些？"
**AI调用**: `tool_get_popular_stocks()`
**返回**: 同花顺人气榜Top200数据

**示例响应**:
```
根据最新数据，今日A股热门股票Top10如下：

1. 平安银行 (000001.SZ) - 人气排名: 1, 涨幅: +2.35%
2. 贵州茅台 (600519.SH) - 人气排名: 2, 涨幅: +1.28%
3. 宁德时代 (300750.SZ) - 人气排名: 3, 涨幅: -0.56%
...

数据来源：同花顺人气榜
```

### 2. 查询股票新闻
**用户输入**: "000001.SZ有什么新闻？"
**AI调用**: `tool_get_stock_news("000001.SZ")`
**返回**: 平安银行相关新闻列表

**示例响应**:
```
平安银行 (000001.SZ) 最近新闻：

1. [利好] 平安银行一季度净利润同比增长15%
   - 来源: 东方财富
   - 时间: 2026-06-15

2. [中性] 平安银行发布2025年年度报告
   - 来源: 同花顺
   - 时间: 2026-06-14
...
```

### 3. 查询模拟账户
**用户输入**: "我的模拟账户情况怎么样？"
**AI调用**: `tool_get_sim_accounts()`
**返回**: 所有模拟账户列表

**示例响应**:
```
您有以下模拟账户：

账户1: 我的策略账户
- 初始资金: ¥1,000,000
- 当前资金: ¥1,052,300
- 总资产: ¥1,085,600
- 收益率: +8.56%
- 状态: 活跃

账户2: 技术面测试
- 初始资金: ¥500,000
- 当前资金: ¥523,400
- 总资产: ¥535,200
- 收益率: +7.04%
- 状态: 活跃
```

### 4. 查询持仓
**用户输入**: "账户1的持仓情况？"
**AI调用**: `tool_get_account_positions(1)`
**返回**: 账户1的持仓明细

**示例响应**:
```
账户1 当前持仓：

1. 平安银行 (000001.SZ)
   - 数量: 1000股
   - 成本价: ¥12.30
   - 现价: ¥12.50
   - 市值: ¥12,500
   - 盈亏: +¥200 (+1.63%)

2. 贵州茅台 (600519.SH)
   - 数量: 10股
   - 成本价: ¥1,800.00
   - 现价: ¥1,825.00
   - 市值: ¥18,250
   - 盈亏: +¥250 (+1.39%)
...
```

### 5. 查询实时行情
**用户输入**: "000001.SZ现在什么价格？"
**AI调用**: `tool_get_stock_price("000001.SZ")`
**返回**: 平安银行实时行情

**示例响应**:
```
平安银行 (000001.SZ) 实时行情：

- 最新价: ¥12.50
- 涨跌幅: +2.35%
- 涨跌额: +0.29
- 成交量: 1,234,567手
- 成交额: ¥15.43亿
- 换手率: 0.64%
```

### 6. 查询策略
**用户输入**: "有哪些量化策略？"
**AI调用**: `tool_get_strategies()`
**返回**: 所有策略列表

**示例响应**:
```
系统中有以下量化策略：

1. 人气榜策略 (popularity)
   - 类型: 人气驱动
   - 状态: 活跃

2. 技术面策略 (technical)
   - 类型: 技术指标
   - 状态: 活跃

3. 多因子策略 (multi_factor)
   - 类型: 综合策略
   - 状态: 活跃
...
```

### 7. 查询回测结果
**用户输入**: "回测结果怎么样？"
**AI调用**: `tool_get_backtest_results()`
**返回**: 所有回测记录

**示例响应**:
```
历史回测结果：

1. 技术面策略回测
   - 回测区间: 2025-01-01 ~ 2026-06-15
   - 总收益率: +25.6%
   - 年化收益率: +18.2%
   - 最大回撤: -12.3%
   - 夏普比率: 1.45
   - 胜率: 58.3%

2. 人气榜策略回测
   - 回测区间: 2025-01-01 ~ 2026-06-15
   - 总收益率: +18.9%
   - 年化收益率: +13.5%
   - 最大回撤: -15.6%
   - 夏普比率: 1.12
   - 胜率: 52.1%
...
```

---

## 技术细节

### AI Agent架构
- **框架**: Pydantic AI
- **模型**: mimo-v2.5-pro (OpenAI兼容接口)
- **功能**: 
  - 支持工具调用（Function Calling）
  - 支持流式响应
  - 支持聊天历史上下文
- **重试**: 2次

### 认证机制
- **方式**: JWT Bearer Token
- **用户ID**: 45 (固定)
- **用户名**: agent-stock (固定)
- **有效期**: 24小时
- **签名算法**: HS256
- **密钥**: 与Stock API的JWT_SECRET_KEY一致

### HTTP客户端
- **库**: httpx.AsyncClient
- **连接池**: 全局单例复用
- **超时**: 10秒
- **错误处理**: 返回JSON错误信息

### 错误处理
- **工具函数**: 返回JSON格式错误信息
- **AI Agent**: 自动处理工具调用失败
- **SSE流式**: 发送error事件

### SSE流式响应
- **格式**: Server-Sent Events
- **事件类型**: 
  - `message`: 消息事件
  - `data`: JSON数据
- **数据类型**:
  - `token`: 流式文本片段
  - `done`: 流式结束
  - `error`: 错误信息

---

## 常用命令

```bash
# 启动服务
python -m agent_stock.main

# 使用uvicorn启动
uvicorn agent_stock.main:app --host 0.0.0.0 --port 9002 --reload

# 运行测试
python -m pytest tests/ -v

# Docker构建
docker build -t agent-stock .

# Docker运行
docker run -p 9002:9002 agent-stock

# Docker Compose启动
docker-compose up -d

# 查看日志
docker-compose logs -f agent-stock
```

---

## 与Stock API的交互

### 调用的API接口
| 工具 | API接口 | 方法 | 说明 |
|------|---------|------|------|
| get_popular_stocks | /api/popularity/latest | GET | 获取热门股票 |
| get_stock_list | /api/stocks | GET | 获取股票列表 |
| get_sim_accounts | /api/quant/sim/accounts | GET | 获取模拟账户 |
| get_account_positions | /api/quant/sim/{id}/positions | GET | 获取账户持仓 |
| get_account_orders | /api/quant/sim/{id}/orders | GET | 获取委托记录 |
| get_stock_news | /api/news/{stock_code} | GET | 获取股票新闻 |
| get_stock_analysis | /api/analysis/{stock_code} | GET | 获取股票分析 |
| get_strategies | /api/quant/strategies | GET | 获取策略列表 |
| get_backtest_results | /api/quant/backtest/results | GET | 获取回测结果 |
| get_stock_price | /api/quant/market/prices | GET | 获取实时行情 |

### 认证方式
- **方式**: JWT Bearer Token
- **Header**: `Authorization: Bearer <token>`
- **Token生成**: `_get_service_token()` 函数
- **签名**: 使用Stock API的JWT_SECRET_KEY

### 请求示例
```python
import httpx

# 获取token
token = _get_service_token()

# 发送请求
client = httpx.AsyncClient()
resp = await client.get(
    "http://localhost:8000/api/popularity/latest",
    headers={"Authorization": f"Bearer {token}"}
)
data = resp.json()
```

### 响应处理
- **成功**: 返回JSON数据
- **失败**: 返回错误信息
- **404**: 返回提示信息（如无分析数据）

---

## License

Private
