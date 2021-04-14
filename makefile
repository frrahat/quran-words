default: test

test:
	pytest -vvv server/tests

start-server:
	uvicorn server.main:app --reload --reload-dir=server/
