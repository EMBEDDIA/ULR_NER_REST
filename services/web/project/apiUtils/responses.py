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

import inspect

import requests
from flask import make_response, jsonify

__possible_methods = ["post", "get", "delete", "put", "options"]

def createErrorResponse(message, code):
    message = {"error": {
        "code": code,
        "message": message
        }
    }
    return make_response(jsonify(message), code)


def createIdResponse(task_id, language):
    message = {
        "data":
            {
                "task_id": task_id,
                "language": language
            }
    }
    return make_response(jsonify(message), 200)


def createGenericResponse(data, code):
    message = {
        "data": data
    }
    return make_response(jsonify(message), code)


def createOptionsResponse(object):
    class_methods = inspect.getmembers(object, predicate=inspect.ismethod)
    api_methods = []
    for method in class_methods:
        method = method[0]
        if method in __possible_methods:
            api_methods.append(method.upper())
    response = make_response("", 204)
    response.headers["Allow"] = api_methods
    del response.headers["Content-type"]
    return response

#Flask restx has issues generating the schema from the API, thus
#I need to retrieve from the swagger.json
def createDocumentationResponse(request):
    url = request.host_url + "swagger.json"
    output = requests.get(url).json()
    return make_response(output, 200)

