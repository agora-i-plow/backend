include .env
export

CODE = app

prepare:
	python -m venv .venv && source .venv/bin/activate && python -m pip install -r requirements.txt

db:
	docker compose up -d

run:
	uvicorn app.__main__:app  --host 0.0.0.0 --port=${FASTAPI_PORT} --log-level=warning

down:
	docker compose down

format:
	isort ${CODE}
	black ${CODE}

pylint:
	pylint ${CODE}

open_postgres:
	docker exec -it postgresql psql -U ${POSTGRES_USERNAME} -d ${POSTGRES_DATABASE}

open_mongo:
	docker exec -it mongodb mongo mongodb://${MONGO_USER}:${MONGO_PASSWORD}@localhost