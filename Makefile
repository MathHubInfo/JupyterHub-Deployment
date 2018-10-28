# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

include .env
include .config/makefile

.DEFAULT_GOAL=build

network:
	@docker network inspect $(DOCKER_NETWORK_NAME) >/dev/null 2>&1 || docker network create $(DOCKER_NETWORK_NAME)

volumes:
	@docker volume inspect $(DATA_VOLUME_HOST) >/dev/null 2>&1 || docker volume create --name $(DATA_VOLUME_HOST)
	@docker volume inspect $(DB_VOLUME_HOST) >/dev/null 2>&1 || docker volume create --name $(DB_VOLUME_HOST)
	@docker volume inspect $(MMT_VOLUME_HOST) >/dev/null 2>&1 || docker volume create --name $(MMT_VOLUME_HOST)

self-signed-cert:
	# make a self-signed cert

secrets/postgres.env:
	@echo "Generating postgres password in $@"
	@echo "POSTGRES_PASSWORD=$(shell openssl rand -hex 32)" > $@

# Do not require cert/key files if SECRETS_VOLUME defined
secrets_volume = $(shell echo $(SECRETS_VOLUME))
ifeq ($(secrets_volume),)
	cert_files=
else
	cert_files=
endif

check-files: $(cert_files) .config/postgres

configure:
	./configure

pull:
	docker pull $(DOCKER_NOTEBOOK_IMAGE)
	docker-compose pull

build: check-files network volumes
	docker build -t mathhub/jupyter .
	docker-compose build

.PHONY: network volumes check-files pull build
