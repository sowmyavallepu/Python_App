start:
	uvicorn app.main:app --reload

spellcheck:
	codespell ./app ./tests

test:
	pytest --cov=app --cov-report=xml

build:
	docker build -t fastapi-azure-app .

requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes
