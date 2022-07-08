local: dependencies-lock code-format lint

dependencies-lock:
	poetry lock --no-update

code-format:
	isort .
	black .

lint:
	flake8
	isort --check .
	black --check .

pre-commit:
	pre-commit install
