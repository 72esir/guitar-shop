FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY broker/ ./broker/
COPY event_contracts/ ./event_contracts/
COPY orders_service/ ./orders_service/
ENV PYTHONPATH=/app
CMD ["python", "-m", "orders_service.main"]