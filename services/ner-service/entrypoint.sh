#!/bin/sh

#Using entrypoint seems to do not be keeping the environment set in the dockerfile, thus we need to activate it manually
. /opt/conda/etc/profile.d/conda.sh
conda activate ner_service	

python NERService.py
