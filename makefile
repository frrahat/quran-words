default: typecheck lint test

test:
	pytest -vvv server/tests

typecheck:
	mypy --config-file=server/mypy.ini server/

lint:
	flake8 server/
	yarn --cwd client/ eslint

setup:
	echo "setting up server"
	if [ -z "${VIRTUAL_ENV}" ] ; then \
		echo "Virtual env needs to be activated first"; \
		exit 1; \
	fi

	pip install -r server/requirements.txt


	echo "setting up client"
	yarn --cwd client/

# command: make start-all -j2
start-all: server-start client-start

server-start:
	uvicorn server.main:app --reload --reload-dir=server/

client-start:
	yarn --cwd client/ start
