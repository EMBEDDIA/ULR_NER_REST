FROM continuumio/miniconda3

ADD environment.yml /tmp/environment.yml

WORKDIR /queue

COPY . /queue

RUN apt-get -y upgrade && \
	apt-get -y install g++ unzip && \
	conda env create -f /tmp/environment.yml && \
	wget https://github.com/EMBEDDIA/bert-bilstm-cnn-crf-ner/archive/master.zip && \
	unzip master.zip && \
	mv ./bert-bilstm-cnn-crf-ner-master/ ./NER/ && \
	rm master.zip

ENV	CELERY_BROKER_URL=redis://redis:6379/0 \
	CELERY_RESULT_BACKEND=redis://redis:6379/0 \
	C_FORCE_ROOT=true \
	PYTHONPATH="/queue/NER/"

ENTRYPOINT ["/queue/entrypoint.sh"]
