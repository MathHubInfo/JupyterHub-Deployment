# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os

c = get_config()

from dockerspawner import DockerSpawner

class FormSpawner(DockerSpawner):
    def _options_form_default(self):
        default_image  = "jupyter/minimal-notebook"
        return """
        <div> To spawn a <a href="https://gl.kwarc.info/theresa_pollinger/MoSIS">MoSIS</a> notebook please select <b>MoSIS</b> and click on the <b>Spawn</b> button below. </div>
        <div> Now navigate to the <b>New</b> dropdown menu on the right and select <b>MoSIS</b>. </div>
        <div> Similarly to this you can also spawn a <a href="https://github.com/UniFormal/mmt_jupyter_kernel">MMT</a> notebook.</div>
        <label for="notebook_image">Select your desired Notebook image</label>
        <select name="notebook_image" size="1">
        <option value="MoSIS">MoSIS </option>
        <option value="MMT">MMT </option>
        <script>
            document.title = "MoSIS"
        </script>
        </select>
        """.format(notebook_image=default_image)

    def options_from_form(self, formdata):
        options = {}
        options['notebook_image'] = formdata['notebook_image']
        container_image = ''.join(formdata['notebook_image'])
        if container_image == 'MMT':
            print("SPAWN: " + container_image + " IMAGE" )
            self.container_image = os.environ['DOCKER_NOTEBOOK_IMAGE_MMT']
        elif container_image == 'MoSIS':
            print("SPAWN: " + container_image + " IMAGE" )
            self.container_image = os.environ['DOCKER_NOTEBOOK_IMAGE_INTERVIEW']
        else:
            print("No valid option!")
        return options

c.JupyterHub.spawner_class = FormSpawner

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

# JupyterHub requires a single-user instance of the Notebook server, so we
# default to using the `start-singleuser.sh` script included in the
# jupyter/docker-stacks *-notebook images as the Docker run command when
# spawning containers.  Optionally, you can override the Docker run command
# using the DOCKER_SPAWN_CMD environment variable.
spawn_cmd = os.environ.get('DOCKER_SPAWN_CMD', "start-singleuser.sh")
c.DockerSpawner.extra_create_kwargs.update({ 'command': spawn_cmd })
# Connect containers to this Docker network
network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name
# Pass the network name as argument to spawned containers
c.DockerSpawner.extra_host_config = { 'network_mode': network_name }
# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir
# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }
# c.DockerSpawner.extra_create_kwargs.update({ 'volume_driver': 'local' })
# Remove containers once they are stopped
c.DockerSpawner.remove_containers = True
# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8080

# TLS config
c.JupyterHub.port = 80
#c.JupyterHub.ssl_key = os.environ['SSL_KEY']
#c.JupyterHub.ssl_cert = os.environ['SSL_CERT']

# Authenticate users with TmpAuthenticator
c.JupyterHub.authenticator_class = 'tmpauthenticator.TmpAuthenticator'

# Persist hub data on volume mounted inside container
data_dir = os.environ.get('DATA_VOLUME_CONTAINER', '/data')

c.JupyterHub.cookie_secret_file = os.path.join(data_dir,
    'jupyterhub_cookie_secret')

c.JupyterHub.db_url = 'postgresql://postgres:{password}@{host}/{db}'.format(
    host=os.environ['POSTGRES_HOST'],
    password=os.environ['POSTGRES_PASSWORD'],
    db=os.environ['POSTGRES_DB']
)
