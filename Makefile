build_web:
	cd frontend/ && yarn build

start_web:
	cd frontend/ && serve -s build -n &

stop_web:
	ps -ef | grep serve | grep build | awk '{print $$2}' | xargs kill

start_api:
	cd api/ && uvicorn main:app --host 0.0.0.0 --port 9000 &

stop_api:
	ps -ef | grep -i uvicorn | awk '{print $$2}' | xargs kill

copy_nginx:
	sudo cp nginx/nginx.conf /etc/nginx/conf.d/nomorewait.com.conf

nginx_start:
	sudo systemctl start nginx

nginx_restart:
	sudo systemctl restart nginx

nginx_status:
	sudo systemctl status nginx.service
