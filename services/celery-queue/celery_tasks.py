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

from celery import Celery, states
from NER import getTags, generateDictOutput
from NER_Manager import NERManager
from celeryApiUtils.processInputText import readText

celery_app = Celery("NER_API", broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
NER_Manager = NERManager()


@celery_app.task()
def supportedLanguages():
    return {"languages": list(NER_Manager.getSupportedLanguages())}


@celery_app.task(bind=True, track_started=True)
def processNERRequest(task, language, text, input_format):
    output = {
                "state": "PROCESSING",
                "status": "Processing Text"
             }
    task.update_state(meta=output)
    data_set = readText(text, input_format)
    output = {
                    "state": "PROCESSING",
                    "status": "Retrieving model"
            }
    task.update_state(meta=output)
    try:
        model = NER_Manager.getModel(language)
        output = {
                    "state": "PROCESSING",
                    "status": "Predicting named entities"
                }
        task.update_state(meta=output)
        tags = getTags(data_set, model)
        output = {
                    "state": "PROCESSING",
                    "status": "Processing predicted named entities"
                }
        task.update_state(meta=output)
        json_output = generateDictOutput(data_set, tags)
        output = {
                    "state": "SUCCESS",
                    "status": "Task completed",
                    "result": json_output
                 }
        task.update_state(state=states.SUCCESS)
    except Exception:
        output = {
                    "state": "FAILURE",
                    "status": "Model not found",
                    "language": language
                 }
        task.update_state(meta=output)
    return output

