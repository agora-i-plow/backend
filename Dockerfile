FROM python:3.10-slim
WORKDIR /code
COPY . .
RUN python -m pip install -r requirements.txt
CMD uvicorn app.__main__:app  --host 0.0.0.0 --port=${FASTAPI_PORT} --log-level=warning
