run_web:
    cd frontend && serve -s build -n &

run_api:
    cd api && uvicorn main:app --host 0.0.0.0 --port 9000
