default: test

test:
	pytest -vvv server/tests

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
start-all: start-server start-client

start-server:
	uvicorn server.main:app --reload --reload-dir=server/

start-client:
	yarn --cwd client/ start
