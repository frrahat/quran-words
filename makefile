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

	if [ ! -d "client/build" ]; then \
		yarn --cwd client/ build; \
	fi

# command: make start-all -j2
start-all: server-start client-start

server-start:
	uvicorn server.main:app --reload --reload-dir=server/

client-start:
	yarn --cwd client/ start

client-build:
	yarn --cwd client/ build

heroku-deploy:
	@echo "---> building client"
	yarn --cwd client/ build

	@echo "---> copying necessary files to heroku-build"
	mkdir -p heroku-build/client
	rsync -a server/ heroku-build/server/
	rsync -a client/build/ heroku-build/client/build/

	@echo "---> preparing heroku specific files"
	echo "-r server/requirements.txt" > heroku-build/requirements.txt
	echo "python-3.9.4" > heroku-build/runtime.txt
	echo "web: gunicorn -w 2 -k uvicorn.workers.UvicornWorker server.main:app" > heroku-build/Procfile

	@echo "---> running test"
	pytest -vvv heroku-build/server/tests/

	@echo "---> not tracking unnecessary files for prod"
	rsync -a .gitignore heroku-build/
	echo "tests/" >> heroku-build/.gitignore

	@echo "---> git commiting and pushing changes to heroku"
	cd heroku-build/ && git init
	cd heroku-build/ && git config user.email "fr.rahat@gmail.com"
	cd heroku-build/ && git config user.name "Fazle Rahat"
	cd heroku-build/ && git config init.defaultBranch master
	cd heroku-build/ && git add .
	cd heroku-build/ && git commit -m "foo" ; true
	cd heroku-build/ && git remote add heroku git@heroku.com:quran-words.git ; true
	cd heroku-build/ && git push heroku master -f
