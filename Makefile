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

self-signed-cert:
	# make a self-signed cert

secrets/postgres.env:
	@echo "Generating postgres password in $@"
	@echo "POSTGRES_PASSWORD=$(shell openssl rand -hex 32)" > $@

secrets/jupyterhub.crt:
	@echo "Need an SSL certificate in secrets/jupyterhub.crt"
	@exit 1

secrets/jupyterhub.key:
	@echo "Need an SSL key in secrets/jupyterhub.key"
	@exit 1

# Do not require cert/key files if SECRETS_VOLUME defined
secrets_volume = $(shell echo $(SECRETS_VOLUME))
ifeq ($(secrets_volume),)
	cert_files=
else
	cert_files=
endif

check-files: $(cert_files) .config/postgres

pull:
	docker pull $(DOCKER_NOTEBOOK_IMAGE)
	docker pull kwarc/mmt:devel

# builds the images
notebook_images: pull singleuser/Dockerfile-mmt singleuser/Dockerfile-mosis mmt_image mosis_image

# builds the images without cache
force_notebook_images: pull singleuser/Dockerfile-mmt singleuser/Dockerfile-mosis force_mmt_image force_mosis_image

# builds the MoSIS image
mmt_image: singleuser/Dockerfile-mmt
	docker build -t $(LOCAL_NOTEBOOK_IMAGE_MMT) \
		--file singleuser/Dockerfile-mmt \
		--build-arg JUPYTERHUB_VERSION=$(JUPYTERHUB_VERSION) \
		--build-arg DOCKER_NOTEBOOK_IMAGE=$(DOCKER_NOTEBOOK_IMAGE) \
		singleuser

# builds the MMT image without cache
force_mmt_image: singleuser/Dockerfile-mmt
	docker build --no-cache -t $(LOCAL_NOTEBOOK_IMAGE_MMT) \
		--file singleuser/Dockerfile-mmt \
		--build-arg JUPYTERHUB_VERSION=$(JUPYTERHUB_VERSION) \
		--build-arg DOCKER_NOTEBOOK_IMAGE=$(DOCKER_NOTEBOOK_IMAGE) \
		singleuser

# builds the MoSIS image
mosis_image: singleuser/Dockerfile-mosis
	docker build -t $(LOCAL_NOTEBOOK_IMAGE_INTERVIEW)  \
	 	--file singleuser/Dockerfile-mosis \
	 	--build-arg JUPYTERHUB_VERSION=$(JUPYTERHUB_VERSION) \
	 	--build-arg DOCKER_NOTEBOOK_IMAGE=$(DOCKER_NOTEBOOK_IMAGE) \
	 	singleuser

# builds the MoSIS image without  cache
force_mosis_image: singleuser/Dockerfile-mosis
	docker build --no-cache -t $(LOCAL_NOTEBOOK_IMAGE_INTERVIEW)  \
		--file singleuser/Dockerfile-mosis \
	 	--build-arg JUPYTERHUB_VERSION=$(JUPYTERHUB_VERSION) \
	 	--build-arg DOCKER_NOTEBOOK_IMAGE=$(DOCKER_NOTEBOOK_IMAGE) \
	 	singleuser

build: check-files network volumes
	docker-compose build

.PHONY: network volumes check-files pull notebook_image build
