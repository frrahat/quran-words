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
	if [ ! -f "client/build/index.html" ]; then \
        mkdir -p client/build; \
		touch client/build/index.html; \
    fi
	pytest -vvv app/tests
