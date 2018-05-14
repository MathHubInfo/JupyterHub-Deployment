# JupyterHub-Deployment

**JupyterHub-Deployment** provides a reference deployment of [jupyter-console-standalone](https://github.com/kwarc/jupyter-console-standalone), the [mmt_kernel](https://github.com/UniFormal/mmt_jupyter_kernel) and the [MoSIS interview_kernel](https://github.com/MathHubInfo/MoSIS_Jupyter_Kernel) using [Docker](https://docs.docker.com).

## Disclaimer

This deployment is **NOT** intended for a production environment.
It is a reference implementation that does not meet traditional
requirements in terms of availability nor scalability.

## Technical Overview

Key components of this reference deployment are:

* **Host**: Runs the [JupyterHub components](https://jupyterhub.readthedocs.org/en/latest/getting-started.html#overview) and a [MMT](https://uniformal.github.io/) server
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


## Configure your setup

Run the configure script with:
``` bash
./configure
```
Here you can choose your domain name and also state additional archives that should be installed to your MMT.

## Run JupyterHub

Run the JupyterHub container on the host.

To run the JupyterHub container in detached mode:

```bash
docker-compose up -d
```

Once the container is running, you should be able to access the JupyterHub console at

```
https://mydomain
```

To bring down the JupyterHub container:

```bash
docker-compose down
```
