# Embeddia Project - Named Entity Recognition
# Copyright © 2020 Luis Adrián Cabrera Diego - La Rochelle Université
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
# to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

FROM python:3.8.1-slim-buster

ADD ./requirements.txt /tmp/requirements.txt

WORKDIR /queue

COPY . /queue

RUN pip install --upgrade pip && \
	pip install -r /tmp/requirements.txt

ENV	CELERY_BROKER_URL=redis://redis:6379/0 \
	CELERY_RESULT_BACKEND=redis://redis:6379/0 \
	C_FORCE_ROOT=true \
	NER_SERVICE_PORT=18861 \
	NER_SERVICE_HOST=ner

ENTRYPOINT ["/queue/entrypoint.sh"]
