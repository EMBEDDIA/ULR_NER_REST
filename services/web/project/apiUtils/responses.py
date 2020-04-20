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

