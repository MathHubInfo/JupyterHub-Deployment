# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG JUPYTERHUB_VERSION=0.9.2
FROM jupyterhub/jupyterhub:$JUPYTERHUB_VERSION

# Install dockerspawner, tmpauthenticator, postgres
RUN /opt/conda/bin/conda install -yq psycopg2=2.7 && \
    /opt/conda/bin/conda clean -tipsy && \
    /opt/conda/bin/pip install --no-cache-dir dockerspawner==0.10.* && \
    /opt/conda/bin/pip install git+https://github.com/jupyterhub/tmpauthenticator && \
    /opt/conda/bin/pip install jupyterhub-tmpauthenticator

COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py
