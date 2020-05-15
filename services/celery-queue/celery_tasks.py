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
import os
import traceback

import rpyc
from celery import Celery, states

#Loading NER service and models
ner_port = os.getenv("NER_SERVICE_PORT")
if ner_port is None:
    ner_port = 18861
else:
    ner_port = int(ner_port)
    
ner_host = os.getenv("NER_SERVICE_HOST")
if ner_host is None:
    ner_host = "localhost"
    
NER_service = rpyc.connect(ner_host, ner_port, config=dict(allow_pickle=True))

asynch_check_status = rpyc.async_(NER_service.root.loadModels)
print("Waiting while models are being loaded")
service_status = asynch_check_status()
service_status.set_expiry(None)
service_status.wait()
print(f"Models have been loaded: {NER_service.root.areModelsLoaded()}")
del asynch_check_status
del service_status

#Loading Celery
celery_app = Celery("NER_API", broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

#Creating asynch NER methods
process_text = rpyc.async_(NER_service.root.createDataset)
process_ner = rpyc.async_(NER_service.root.processNERRequest)


@celery_app.task(bind=True, track_started=True)
def processNERRequest(task, language, text, input_format):
    try:
        output = {
            "state": "PROCESSING",
            "status": "Processing Text"
        }
        task.update_state(meta=output)
        request = process_text(text, input_format)
        request.set_expiry(None)
        request.wait()
        data_set = request.value
        output = {
                    "state": "PROCESSING",
                    "status": "Predicting named entities"
                }
        task.update_state(meta=output)
        #We need to obtain a true dictionary (this is done by dereferening the netref object and asking a local copy)
        request = process_ner(language, data_set)
        request.set_expiry(None)
        request.wait()
        json_output = rpyc.classic.obtain(request.value)
        output = {
                    "state": "SUCCESS",
                    "status": "Task completed",
                    "result": json_output
                 }
        task.update_state(state=states.SUCCESS)
    except Exception:
        traceback.print_exc()
        output = {
                    "state": "FAILURE",
                    "error": traceback.format_exc()
                 }
        task.update_state(meta=output)
    return output

