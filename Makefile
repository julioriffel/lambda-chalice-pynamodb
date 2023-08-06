NAME=lambda-chalice-pynamodb
VERSION=0.0.1

DB_PORT = 8000
API_PORT = 8010
JWT_SECRET ?= development
CHALICE_ENV = "dev"


.PHONY: pull run stop restart rm

pull:
	docker pull amazon/dynamodb-local

dynamo:
	docker run --rm --name dynamodb-local -d -p $(DB_PORT):$(DB_PORT) amazon/dynamodb-local

config:
	sed "s/<JWT_SECRET>/$(JWT_SECRET)/" .chalice/config.json.template > .chalice/config.json
run:
	docker run --rm --name dynamodb-local -d -p $(DB_PORT):$(DB_PORT) amazon/dynamodb-local
	# Wait for local DB to start
	sleep 5
	chalice local --port $(API_PORT) --no-autoreload

stop:
	docker stop dynamodb-local

restart:
	docker restart dynamodb-local

chalice:
	chalice local --port $(API_PORT) --no-autoreload

ci-server:
	sh -c "chalice local --port $(API_PORT) --no-autoreload &"

deploy:
	chalice deploy --stage $(CHALICE_ENV)

default: run

clean: stop

test:
	@coverage run -m pytest  && coverage report && google-chrome htmlcov/index.html

install:
	@pipenv install

install-dev:
	@pipenv install --dev

requirements:
	@pipenv requirements > requirements.txt
	@pipenv requirements --dev-only > requirements-dev.txt
