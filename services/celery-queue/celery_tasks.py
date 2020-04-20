from celery import Celery, states

from NER.NER import getTags, generateDictOutput
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

