include .env
export

CODE = app

prepare:
	python -m venv .venv && source .venv/bin/activate && python -m pip install -r requirements.txt

run:
	uvicorn app.__main__:app  --host 0.0.0.0 --port=${FASTAPI_PORT} --log-level=warning

format:
	isort ${CODE}
	black ${CODE}

pylint:
	pylint ${CODE}