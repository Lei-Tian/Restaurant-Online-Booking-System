start_api:
	cd api/ && uvicorn main:app --host 0.0.0.0 --port 9000 &

stop_api:
	ps -ef | grep -i uvicorn | awk '{print $$2}' | xargs kill

start_web:
	cd frontend/ && yarn build && serve -s build -n &

stop_web:
	ps -ef | grep serve | grep build | awk '{print $$2}' | xargs kill

start_worker:
	cd api/ && celery -A app.core.celery_app worker --loglevel=INFO -f /tmp/nomorewait/nomorewait_worker.log &

stop_worker:
	ps -ef | grep celery_app | awk '{print $$2}' | xargs kill

copy_nginx:
	sudo cp nginx/nginx.conf /etc/nginx/conf.d/nomorewait.com.conf

nginx_start:
	sudo systemctl start nginx

nginx_restart:
	sudo systemctl restart nginx

nginx_status:
	sudo systemctl status nginx.service

publish_web:
	cd frontend/ && yarn build && rm -rf ../api/public && mv build ../api/public
