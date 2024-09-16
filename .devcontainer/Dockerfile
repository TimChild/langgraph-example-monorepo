# syntax=docker/dockerfile:1
# Keep this syntax directive! It's used to enable Docker BuildKit

# Adapted from https://github.com/Standard-IO/devcontainers-templates/tree/main/src/python3-poetry-pyenv
FROM mcr.microsoft.com/devcontainers/base:bullseye as base

ARG DEBIAN_FRONTEND=noninteractive
ARG USER=vscode
ARG HOME="/home/$USER"
ARG PYTHON_VERSION=3.12

ENV PYTHONFAULTHANDLER=1 \
     PYTHONUNBUFFERED=1 \
     PYTHONHASHSEED=random \
     PIP_NO_CACHE_DIR=off \
     PIP_DISABLE_PIP_VERSION_CHECK=on \
     PIP_DEFAULT_TIMEOUT=100 \
     # Poetry's configuration:
     POETRY_NO_INTERACTION=1 \
     POETRY_VIRTUALENVS_CREATE=false \
     POETRY_CACHE_DIR="${HOME}/.cache/pypoetry" \
     PYENV_ROOT="${HOME}/.pyenv" \
     # For pytest-pretty to display wider
     COLUMNS=120

RUN DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install -y build-essential --no-install-recommends make \
        ca-certificates \
        git \
        libssl-dev \
        zlib1g-dev \
        libbz2-dev \
        libreadline-dev \
        libsqlite3-dev \
        wget \
        curl \
        llvm \
        libncurses5-dev \
        xz-utils \
        tk-dev \
        libxml2-dev \
        libxmlsec1-dev \
        libffi-dev \
        liblzma-dev \
        entr

# Python and poetry installation
USER $USER
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${HOME}/.local/bin:$PATH"

RUN echo "done 0" \
    && curl https://pyenv.run | bash \
    && echo "done 1" \
    && pyenv install ${PYTHON_VERSION} \
    && echo "done 2" \
    && pyenv global ${PYTHON_VERSION} \
    && echo "done 3" \
    && curl -sSL https://install.python-poetry.org | python3 -

FROM base as dev

# Note: Working in the /home/... directory for initial setup, but workspace will be in /workspace/...
#  This works because poetry is set to install without virtual envs, and the global python is set via pyenv
WORKDIR $HOME
# # Install playwright before pyproject.toml so that it stays cached on version change
# RUN pip install playwright && \
#     playwright install chromium --with-deps

COPY pyproject.toml poetry.lock* initial_deps/
RUN cd initial_deps && poetry install --with test --no-root
