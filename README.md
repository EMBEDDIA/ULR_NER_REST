## Flask REST API skeleton with dockerized Flask + flask_restx, Gunicorn, Nginx, Celery, Flower and Redis

This repository is based on [flask-rest-docker](https://github.com/EMBEDDIA/flask-rest-docker) which in turn extends [flask-on-docker](https://github.com/testdrivenio/flask-on-docker) with Celery, Redis and Flask_restx to provide a skeleton for building dockerized Flask RESTful APIs. This version includes a container (`ner-service`) which make use of miniconda to facilitate the import of requirements. 

### Main Requirements
-  docker
-  docker-compose

### Selecting which models to load

In the path `services/ner-service` there is a configuration file (`config.json`). Currently, only one model is being loaded as indicated with `"loadLanguages": ["hr"]`. If more languages want to be loaded, it is necessary to add them to the list. However, if all the models want to be loaded, you can remove that line from the configuration file and the program will load all the available models.

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

If you go to [http://0.0.0.0:5000](http://0.0.0.0:5000) you will see a web interface where you can check and test your REST API. Flower monitor for Celery is running on [http://0.0.0.0:5555](http://0.0.0.0:5555). Note that the `web` folder is mounted into the container and the Flask development server reloads your code automatically so any changes will be visible immediately.

## License

This work has been attributed an MIT License and makes use of portions of code from the following repositories:

- [flask-rest-docker](https://github.com/EMBEDDIA/flask-rest-docker): MIT License
- [flask-on-docker](https://github.com/testdrivenio/flask-on-docker): MIT License


