FROM nvidia/cuda:11.6.2-cudnn8-devel-ubuntu20.04 as base
LABEL maintainer="macal@agh.edu.pl"

ENV PYTHON_VERSION=3.10
ENV RAY_VERSION=2.1.0
ENV TORCH_VERSION=1.13.1+cu116
ENV TORCHVISION_VERSION=0.14.1+cu116
ENV MINICONDA_URL https://repo.continuum.io/miniconda/Miniconda3-4.7.12.1-Linux-x86_64.sh
ENV PYTORCH_URL https://download.pytorch.org/whl/cu116

# LOCALE & INSTALLATION UTILITY
# -------------------------------------------------------------------------------------------- #
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN echo 'Etc/UTC' > /etc/timezone \
    && ln -s /usr/share/zoneinfo/Etc/UTC /etc/localtime \
    && apt update > /dev/null \
    && apt upgrade -y \
    && apt install -q -y --no-install-recommends \
        bash \
        ca-certificates \
        curl \
        locales \
        sudo \
        tzdata \
        zsh \
    && rm -rf /var/lib/apt/lists/* \
    && locale-gen ${LC_ALL} > /dev/null \
    && dpkg-reconfigure locales > /dev/null

# Create an user
# -------------------------------------------------------------------------------------------- #
RUN mkdir /mnt/ws \
    && addgroup user \
    && adduser --disabled-password --gecos '' --ingroup user --shell /bin/bash user \
    && ln -s /mnt/ws /home/user/ws \
    && chown -R user:user /mnt/ws /home/user \
    && echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-user

RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true \
    && usermod --shell /bin/zsh root \
    && usermod --shell /bin/zsh user

ENV HOME /home/user
USER user

# Miniconda environment
# -------------------------------------------------------------------------------------------- #
ENV CONDA_AUTO_UPDATE_CONDA false
ENV PATH /home/user/miniconda/bin:$PATH

RUN curl -sL ${MINICONDA_URL} > ~/miniconda.sh \
    && chmod +x ~/miniconda.sh \
    && ~/miniconda.sh -b -p ~/miniconda \
    && rm ~/miniconda.sh \
    && conda install -y python==${PYTHON_VERSION} \
    && conda clean -ya

# PyTorch + torchvision
# -------------------------------------------------------------------------------------------- #
RUN pip3 install torch==$TORCH_VERSION torchvision==$TORCHVISION_VERSION --extra-index-url ${PYTORCH_URL} \
    && rm -rf /home/user/.cache/pip

# Jupyterlab
# -------------------------------------------------------------------------------------------- #
RUN conda install \
        jupyterlab \
    && mkdir -p /home/user/.jupyter \
    && (echo "c.NotebookApp.ip = '*'"; echo "c.NotebookApp.notebook_dir = '/mnt/ws'")  >> /home/user/.jupyter/jupyter_notebook_config.py \
    && conda clean -ya \
    && python3 -m pip install \
        black \
        black[jupyter] \
        isort \
        jupyterlab-code-formatter

# TOOLS
# -------------------------------------------------------------------------------------------- #
USER root
RUN apt update > /dev/null && apt install -y \
        bash-completion \
        dnsutils \
        git \
        htop \
        iproute2 \
        iputils-ping \
        mc \
        neovim \
        net-tools \
        ranger \
        tmux \
        wget \
    && rm -rf /var/lib/apt/lists/*

# Python packages
# -------------------------------------------------------------------------------------------- #
USER user
RUN conda install \
        matplotlib \
        pandas \
        pyyaml \
        tensorboard \ 
    && conda clean -ya


# -------------------------------------------------------------------------------------------- #
FROM base as env_frameworks

ENV MUJOCO_BIN_URL=https://mujoco.org/download/mujoco210-linux-x86_64.tar.gz

# ENV frameworks
# -------------------------------------------------------------------------------------------- #
USER root
RUN apt update > /dev/null && apt install -y \
        libgl1-mesa-glx \
        libglew2.1 \ 
        libglfw3 \ 
        libosmesa6-dev \
        patchelf \
        xvfb \
    && rm -rf /var/lib/apt/lists/*

USER user
RUN python3 -m pip install \
        PyOpenGL \
        #TODO Quick workaround for PyOpenGL-accelerate https://github.com/mcfletch/pyopengl/issues/78
        git+https://github.com/mcfletch/pyopengl.git@227f9c66976d9f5dadf62b9a97e6beaec84831ca#subdirectory=accelerate \
    && python3 -m pip install \
        dm_control \
        gputil \
        gym \
        gymnasium \
        gymnasium-robotics \
        mujoco \
        procgen \
        pygame \
        pyrender \
    && rm -rf /home/user/.cache/pip \
    && mkdir -p ~/.mujoco \
    && curl -sL ${MUJOCO_BIN_URL} > /home/user/.mujoco/mujoco210.tar.gz \
    && tar -xf /home/user/.mujoco/mujoco210.tar.gz -C /home/user/.mujoco \
    && rm /home/user/.mujoco/mujoco210.tar.gz \
    && echo "LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:/home/user/.mujoco/mujoco210/bin" >> ~/.bashrc


# -------------------------------------------------------------------------------------------- #
FROM env_frameworks as ray_rrlib

# Info about fixes: 
# This numpy version leaves a problematic folder...
# grpcio in version 1.48.0 crahses the main Ray node
RUN rm -rf /home/user/miniconda/lib/python3.10/site-packages/numpy-1.24.3.dist-info \
    && python3 -m pip install -U "ray[rllib]==$RAY_VERSION" "ray[serve]==$RAY_VERSION" \
    && python3 -m pip install grpcio==1.42.0 \
    && rm -rf /home/user/.cache/pip

# ENTRYPOINT
# -------------------------------------------------------------------------------------------- #
COPY entrypoint.sh /home/user/.
ENTRYPOINT ["/home/user/entrypoint.sh"]
WORKDIR /mnt/ws
CMD ["zsh"]
