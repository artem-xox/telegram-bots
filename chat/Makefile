# variables
IMAGE=chat-bot

debug:
	poetry run python3 app/bot.py

test:
	pytest .

# docker
docker-build:
	docker build -t ${IMAGE} .

docker-run: docker-build
	docker run --rm --env-file .env --name ${IMAGE}-container ${IMAGE}
