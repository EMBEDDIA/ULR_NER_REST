from flask import Flask
from flask_restx import Api
from .NER_API import api as ner_api

flask_app = Flask("NER_API")
flask_app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
flask_app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

api = Api(
          title="NER API",
          version="0.1",
          description="API for NER from ULR"
          )

api.add_namespace(ner_api, path="/ner")

api.init_app(flask_app)

#flask_app.run(debug=True)


