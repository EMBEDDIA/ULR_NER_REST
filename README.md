## Flask REST API skeleton with dockerized Flask + flask_restx, Gunicorn, Nginx, Celery, Flower and Redis


This repository extends [flask-on-docker](https://github.com/testdrivenio/flask-on-docker) with Celery, Redis and Flask_restx to provide a skeleton for building dockerized Flask RESTful APIs. However, for the NER part we use conda environments to load easily the requirements.

### Requirements
-  docker
-  docker-compose

#### Development

The following command

```sh
$ docker-compose up -d --build
```

will build the images and run the containers. If you go to [http://localhost:5000](http://localhost:5000) you will see a web interface where you can check and test your REST API. Flower monitor for Celery is running on [http://localhost:5555](http://localhost:5555). Note that the `web` folder is mounted into the container and the Flask development server reloads your code automatically so any changes will be visible immediately.

#### Production

The following command

```sh
$ docker-compose -f docker-compose.prod.yml up -d --build
```

will build the images and run the containers. The web interface is now available at [http://localhost](http://localhost) and the Flower monitor at [http://localhost:5555](http://localhost:5555). If you change the source code, you will have to do a rebuild for changes to take effect.
