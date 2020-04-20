from flask_restx import Api
from .NER_API import api as ner_api
from . import flask_app

api = Api(
          title="NER API",
          version="0.1",
          description="API for NER from ULR"
          )

api.add_namespace(ner_api, path="/ner")

api.init_app(flask_app)

flask_app.run(debug=True)
