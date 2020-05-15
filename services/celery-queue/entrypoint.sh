#!/bin/sh

./wait-for-it.sh "$NER_SERVICE_HOST":"$NER_SERVICE_PORT"
flower -A celery_tasks --persistent=True --max-tasks=100000 --port=5555 --broker="$CELERY_BROKER_URL" --basic_auth="$FLOWER_USER":"$FLOWER_PASSWORD" &
celery -A celery_tasks worker --loglevel=info
