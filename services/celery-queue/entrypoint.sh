#!/bin/sh

#Using entrypoint seems to do not be keeping the environment set in the dockerfile, thus we need to activate it manually
. /opt/conda/etc/profile.d/conda.sh
conda activate celery_queue	

flower -A celery_tasks --persistent=True --max-tasks=100000 --port=5555 --broker="$CELERY_BROKER_URL" --basic_auth="$FLOWER_USER":"$FLOWER_PASSWORD" &
celery -A celery_tasks worker --loglevel=info
