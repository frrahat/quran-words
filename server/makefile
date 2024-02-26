generate-requirements:
	pip install pip-tools
	pip-compile requirements.in

lint:
	flake8 app/ --config flake8.cfg

typecheck:
	mypy app/

format:
	black app/
	isort app/

test:
	mkdir -p client
    cp -r ../client/build client/
	pytest -vvv app/tests
