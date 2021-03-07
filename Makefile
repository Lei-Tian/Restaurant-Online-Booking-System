run_web:
	cd frontend/ && serve -s build -n &

run_api:
	cd api/ && uvicorn main:app --host 0.0.0.0 --port 9000

copy_nginx:
	sudo cp nginx/nginx.conf /etc/nginx/conf.d/nomorewait.com.conf

nginx_start:
	sudo systemctl start nginx

nginx_restart:
	sudo systemctl restart nginx

nginx_status:
	sudo systemctl status nginx.service
