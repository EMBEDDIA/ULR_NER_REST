## Flask REST API skeleton with dockerized Flask + flask_restx, Gunicorn, Nginx, Celery, Flower and Redis

This repository is based on [flask-rest-docker](https://github.com/EMBEDDIA/flask-rest-docker) which in turn extends [flask-on-docker](https://github.com/testdrivenio/flask-on-docker) with Celery, Redis and Flask_restx to provide a skeleton for building dockerized Flask RESTful APIs. This version for the celery_queue container, make use of miniconda to facilitate the import of requirements. 

### Main Requirements
-  docker
-  docker-compose

#### Development

The following command

```sh
$ docker-compose build
```

will build the images and run the containers.

The following command

```sh
$ docker-compose up
```

If you go to [http://localhost:5000](http://localhost:5000) you will see a web interface where you can check and test your REST API. Flower monitor for Celery is running on [http://localhost:5555](http://localhost:5555). Note that the `web` folder is mounted into the container and the Flask development server reloads your code automatically so any changes will be visible immediately.

## License

This work has been attributed an MIT License and makes use of portions of code from the following repositories:

- [flask-rest-docker](https://github.com/EMBEDDIA/flask-rest-docker): MIT License
- [flask-on-docker](https://github.com/testdrivenio/flask-on-docker): MIT License


