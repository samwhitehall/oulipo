FROM python:2.7
MAINTAINER Sam Whitehall <me@samwhitehall.com>

ENV INSTALL_PATH /oulipo

RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

# Install requirements including spacy English corpus (~500MB)
COPY requirements requirements
RUN pip install -r requirements
RUN python -m spacy.en.download

COPY ./oulipo .

# Don't run as the default superuser (celery isn't happy doing this)
RUN useradd -ms /bin/bash oulipo
USER oulipo
