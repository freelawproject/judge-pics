FROM python:3.8-slim

#Copy project to Docker image
RUN mkdir /project
WORKDIR /project

RUN apt-get update --option "Acquire::Retries=3" --quiet=2 && \
    apt-get install \
        --no-install-recommends \
        --assume-yes \
        --quiet=2 \
        # So we can use Python-slim
        build-essential gcc python-dev git

RUN pip install git+https://github.com/freelawproject/judge-pics
