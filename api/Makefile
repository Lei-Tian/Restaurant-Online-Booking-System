all: ci

lint:
	flake8

checkformat:
	black --check .
	isort --check .

format:
	black .
	isort .

migrate:
	alembic upgrade head

rollback:
	alembic downgrade -1

migration:
	alembic revision --autogenerate -m "${MESSAGE}"

ci: checkformat lint