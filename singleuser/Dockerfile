ARG DOCKER_NOTEBOOK_IMAGE
FROM $DOCKER_NOTEBOOK_IMAGE
ARG JUPYTERHUB_VERSION
RUN python3 -m pip install --no-cache jupyterhub==$JUPYTERHUB_VERSION

RUN git clone https://github.com/kwarc/jupyter-console-standalone && \
    cd jupyter-console-standalone/jcs/files && npm install && npm run build && cd ../../ && \
    python setup.py install && jupyter serverextension enable --sys-prefix --py jcs && cd .. && \
    rm -rf jupyter-console-standalone

