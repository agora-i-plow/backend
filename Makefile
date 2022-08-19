CODE = app

prepare:
	python -m venv .venv && source .venv/bin/activate && python -m pip install -r requirements.txt

run:
	uvicorn app.__main__:app --port=8000

format:
	isort ${CODE}
	black ${CODE}

pylint:
	pylint ${CODE}