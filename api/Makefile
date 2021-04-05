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

empty_migration:
	alembic revision -m "${MESSAGE}"

initdata:
	python3 scripts/initial_data.py

cleardata:
	python3 scripts/truncate_data.py

ci: checkformat lint