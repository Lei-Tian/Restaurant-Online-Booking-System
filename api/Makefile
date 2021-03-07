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

initdata:
	python3 app/scripts/initial_data.py

cleardata:
	python3 app/scripts/truncate_data.py

ci: checkformat lint