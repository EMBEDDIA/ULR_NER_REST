from flask.cli import FlaskGroup
from flask_cors import CORS
from project import flask_app

CORS(flask_app)
cli = FlaskGroup(flask_app)


if __name__ == "__main__":
    cli()
