FROM python:3.12-slim

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com .

ENV AGENT_PORT=9002
EXPOSE ${AGENT_PORT}

CMD ["sh", "-c", "uvicorn agent_stock.main:app --host 0.0.0.0 --port ${AGENT_PORT}"]
