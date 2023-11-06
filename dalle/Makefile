# variables
IMAGE=dalle-bot

debug:
	poetry run python3 -m app.bot

# docker
docker-build:
	docker build -t ${IMAGE} .

docker-run:
	docker run --rm --env-file .env --name ${IMAGE}-container ${IMAGE}

docker: docker-build docker-run
