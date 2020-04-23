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

from celery import Celery
from flask import request
from flask_restx import Resource, reqparse, fields, Namespace

from .apiUtils.responses import createErrorResponse, createIdResponse, createGenericResponse, createOptionsResponse, createDocumentationResponse
from .apiUtils.synchronization import synchronized_function

# API description
api = Namespace('ner', description='NER related operations')
celery_app = Celery("NER_API", broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')


@api.route("/documentation")
class documentation(Resource):

    def get(self):
        return createDocumentationResponse(request)


@api.route('/supportedLanguages')
class SupportedLanguages(Resource):

    __supported_languages = None

    #Lazy singleton
    @staticmethod
    @synchronized_function
    def __retrieveSupportedLanguages():
        if SupportedLanguages.__supported_languages is None:
            task = celery_app.send_task("celery_tasks.supportedLanguages")
            response = celery_app.AsyncResult(task.id)
            while response.state != "SUCCESS":
                response = celery_app.AsyncResult(task.id)
            SupportedLanguages.__supported_languages = response.info["languages"]

    @staticmethod
    def getSupportedLanguages():
        if SupportedLanguages.__supported_languages is None:
            SupportedLanguages.__retrieveSupportedLanguages()
        return SupportedLanguages.__supported_languages

    def get(self):
        supported = {"languages": SupportedLanguages.getSupportedLanguages()}
        return createGenericResponse(supported, 200)

    def options(self):
        return createOptionsResponse(self)


@api.route('/predict/retrievePredictions/<string:task_id>')
class predictNER(Resource):

    def get(self, task_id):
        responde_code = 200
        task = celery_app.AsyncResult(task_id)
        if task.state == 'PENDING':
            response = {
                'state': task.state,
                'status': 'Pending'
            }
        elif task.state != 'FAILURE':
            if task.info["state"] == "FAILURE":
                responde_code = 500
            response = {}
            for field in task.info:
                response[field] = task.info[field]
        else:
            response = {}
            for field in task.info:
                response[field] = task.info[field]
            response['state'] = task.state
        return createGenericResponse(response, responde_code)

    def options(self, task_id):
        return createOptionsResponse(self)


@api.route('/predict/rawText/<string:language>/')
class nerRaw(Resource):

    @api.doc(params={
        'language': 'Language in which the analysis will be done',
        'text': 'Text to process'
    })
    def post(self, language):
        parser = reqparse.RequestParser()
        parser.add_argument("text", required=True)
        args = parser.parse_args()
        if language in SupportedLanguages.getSupportedLanguages():
            if args["text"] is not None and args["text"] != "":
                task = celery_app.send_task("celery_tasks.processNERRequest", args=[language, args["text"], "plain"])
                return createIdResponse(task.id, language)
            return createErrorResponse("Empty text", 400)
        return createErrorResponse("Unsupported language", 400)

    def options(self, language):
        return createOptionsResponse(self)


@api.route('/predict/sentences/<string:language>/')
class nerSentences(Resource):

    resource_input = api.model('Resource', {
        'sentences': fields.List(fields.String),
    })

    @api.expect(resource_input)
    def post(self, language):
        sentences = request.json["sentences"]
        if language in SupportedLanguages.getSupportedLanguages():
            if sentences is not None and len(sentences) > 0:
                task = celery_app.send_task("celery_tasks.processNERRequest", args=[language, sentences, "sentences"])
                return createIdResponse(task.id, language)
            return createErrorResponse("Empty text", 400)
        return createErrorResponse("Unsupported language", 400)

    def options(self, language):
        return createOptionsResponse(self)


@api.route('/predict/tokens/<language>/')
class nerTokens(Resource):

    resource_input = api.model('Resource', {
        'sentences': fields.List(fields.List(fields.String)),
    })

    @api.expect(resource_input)
    def post(self, language):
        sentences = request.json["sentences"]
        if language in SupportedLanguages.getSupportedLanguages():
            if sentences is not None and len(sentences) > 0:
                task = celery_app.send_task("celery_tasks.processNERRequest", args=[language, sentences, "tokens"])
                return createIdResponse(task.id, language)
            return createErrorResponse("Empty text", 400)
        return createErrorResponse("Unsupported language", 400)

    def options(self, language):
        return createOptionsResponse(self)

