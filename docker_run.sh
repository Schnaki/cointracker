docker run --name flaskapp --restart=always \
	-p 4001:80 \
	-v /path/to/app/:/app \
	-d jazzdd/alpine-flask:python3

