# adapted from original JupyterHub_config.py file
# which is Copyright (c) Jupyter Development Team, see LICENSE

import os
from dockerspawner import DockerSpawner

c = get_config()

# use our custom spawnwer dor jupyterhub config
class MathHubSpawner(DockerSpawner):
    def __init__(self, *args, **kwargs):
        super(MathHubSpawner, self).__init__(*args, **kwargs)
        self.env_keep += ['MMT_FRONTEND_BASE_URL', 'UPLOAD_REDIRECT_PREFIX']
        self.container_image = os.environ['DOCKER_NOTEBOOK_IMAGE']
c.JupyterHub.spawner_class = MathHubSpawner

# Command used to spawn jupyter hub inside of DockerSpawner
spawn_cmd = os.environ.get('DOCKER_SPAWN_CMD', "start-singleuser.sh")
c.DockerSpawner.extra_create_kwargs.update({ 'command': spawn_cmd })

# Docker Spawner network configuration
c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.extra_host_config = { 'network_mode': c.DockerSpawner.network_name }
c.DockerSpawner.use_internal_ip = True

# Docker Volumes and Notebook directory
c.DockerSpawner.notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': c.DockerSpawner.notebook_dir }
c.DockerSpawner.volumes[os.environ.get('MMT_VOLUME_HOST')] = {'bind' : '/content/', 'mode' : 'ro' }

c.DockerSpawner.remove_containers = True
c.DockerSpawner.debug = True

# Jupyter Hub Public URL
c.JupyterHub.port = 80

# Jupyter Hub Internal URL (for docker containers)
c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8080

# cookie secret can be found in the data_volume container under /data
data_dir = os.environ.get('DATA_VOLUME_CONTAINER', '/data')
c.JupyterHub.cookie_secret_file = os.path.join(data_dir, 'jupyterhub_cookie_secret')

# postgresql database config
c.JupyterHub.db_url = 'postgresql://postgres:{password}@{host}/{db}'.format(
    host=os.environ['POSTGRES_HOST'],
    password=os.environ['POSTGRES_PASSWORD'],
    db=os.environ['POSTGRES_DB']
)

# Authentication Setup for JupyterHub
# TODO: Try using GitLab OAuth here
c.JupyterHub.authenticator_class = 'tmpauthenticator.TmpAuthenticator'