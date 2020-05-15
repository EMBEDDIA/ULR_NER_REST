#!/bin/sh

./wait-for-it.sh "$NER_SERVICE_HOST":"$NER_SERVICE_PORT"
exec "$@"
