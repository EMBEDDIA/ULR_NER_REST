# pull official base image
FROM python:3.8.1-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	NER_SERVICE_PORT=18861 \
	NER_SERVICE_HOST=ner

#Copy requirements and project
COPY ./requirements.txt /usr/src/app/requirements.txt

COPY . /usr/src/app/

# install system dependencies
RUN apt-get update && \
	apt-get install -y netcat && \
	pip install --upgrade pip && \
	pip install -r requirements.txt

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
