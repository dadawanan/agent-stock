FROM python:3.12-slim

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com .

EXPOSE 8001

CMD ["uvicorn", "agent_stock.main:app", "--host", "0.0.0.0", "--port", "8001"]
