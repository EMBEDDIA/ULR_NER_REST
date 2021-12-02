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

FROM continuumio/miniconda3

ADD environment.yml /tmp/environment.yml

WORKDIR /ner_service

COPY . /ner_service

RUN apt-get --allow-releaseinfo-change -y update && \
	apt-get -y upgrade && \
	apt-get -y install g++ unzip && \
	apt-get -y autoremove && \
	apt-get -y autoclean && \
	apt-get clean && \
	conda env create -f /tmp/environment.yml && \
	wget https://github.com/EMBEDDIA/bert-bilstm-cnn-crf-ner/archive/master.zip && \
	unzip master.zip && \
	rm master.zip && \
	mv ./bert-bilstm-cnn-crf-ner-master/ ./NER/

ENV	NER_SERVICE_PORT=18861 \
	C_FORCE_ROOT=true \
	PYTHONPATH="/ner_service/NER/"

ENTRYPOINT ["/ner_service/entrypoint.sh"]
