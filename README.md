# jupyterhub-console-deploy-docker

**jupyterhub-console-deploy-docker** provides a reference deployment of [jupyter-console-standalone](https://github.com/kwarc/jupyter-console-standalone), using [Docker](https://docs.docker.com). 

## Disclaimer

This deployment is **NOT** intended for a production environment. 
It is a reference implementation that does not meet traditional 
requirements in terms of availability nor scalability. 

## Technical Overview

Key components of this reference deployment are:

* **Host**: Runs the [JupyterHub components](https://jupyterhub.readthedocs.org/en/latest/getting-started.html#overview)
  in a Docker container on the host.

* **Authenticator**: Uses [tmpauthenticator](https://github.com/jupyterhub/tmpauthenticator) to create user accounts on the fly. 

* **Spawner**: Uses [DockerSpawner](https://github.com/jupyter/dockerspawner) to spawn single-user Jupyter Notebook servers in separate Docker containers on the same host.

* **Persistence of Hub data**: Persists JupyterHub data in a Docker volume on the host.

* **Persistence of user notebook directories**: Persists user notebook directories in Docker volumes on the host.

## Prerequisites

### Docker

This deployment uses Docker, via [Docker Compose](https://docs.docker.com/compose/overview/), for all the things.
[Docker Engine](https://docs.docker.com/engine) 1.12.0 or higher is
required.

1. Use [Docker's installation instructions](https://docs.docker.com/engine/installation/)
   to set up Docker for your environment.

2. To verify your docker installation, whether running docker as a local
   installation or using [docker-machine](./docs/docker-machine.md),
   enter these commands:

   ```bash
   docker version
   docker ps
   ```

### HTTPS and SSL/TLS certificate

This deployment configures JupyterHub to use HTTPS. You must provide a
certificate and key file in the JupyterHub configuration. To configure:

1. Obtain the domain name that you wish to use for JupyterHub, for
   example, `myfavoritesite.com` or `jupiterplanet.org`.

1. If you do not have an existing certificate and key, you can:

   - obtain one from [Let's Encrypt](https://letsencrypt.org) using
     the [certbot](https://certbot.eff.org) client,
   - use the helper script in this repo's [letsencrypt example](examples/letsencrypt/README.md), or
   - [create a self-signed certificate](https://jupyter-notebook.readthedocs.org/en/latest/public_server.html#using-ssl-for-encrypted-communication).

1. Copy the certificate and key files to a
   directory named `secrets` in this repository's root directory.  These will be
   added to the JupyterHub Docker image at build time. For example, create a
   `secrets` directory in the root of this repo and copy the certificate and
   key files (`jupyterhub.crt` and `jupyterhub.key`) to this directory:

   ```bash
   mkdir -p secrets
   cp jupyterhub.crt jupyterhub.key secrets/
   ```

## Build the JupyterHub Docker image

Finish configuring JupyterHub and then build the hub's Docker image. (We'll
build the Jupyter Notebook image in the next section.)

1. Use [docker-compose](https://docs.docker.com/compose/reference/) to build
   the JupyterHub Docker image on the active Docker machine host by running
   the `make build` command:

   ```bash
   make build
   ```


## Spawner: Prepare the Jupyter Notebook Image

You can pull the image using the following command:

```bash
make notebook_image
```


## Run JupyterHub

Run the JupyterHub container on the host.

To run the JupyterHub container in detached mode:

```bash
docker-compose up -d
```

Once the container is running, you should be able to access the JupyterHub console at

**file**
```
https://myhost.mydomain
```

To bring down the JupyterHub container:

```bash
docker-compose down
```