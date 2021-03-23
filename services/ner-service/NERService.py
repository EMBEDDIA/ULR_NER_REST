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

import json
import os
import traceback
import subprocess


import rpyc

from NER import loadModelsWithConfig, getTags, generateDictOutput
from utils.processInputText import readText
from utils.synchronization import synchronized_method


class NERService(rpyc.Service):

    __NER_instance = None

    class __NERSingleton:
        def __init__(self):
            self.__models_loaded = False
            self.__loaded_models = {}
            self.__supported_languages = None
            self.__fasttext_path = None
            self.__komninos_path = None
            self.__model_base_path = None
            self.__use_cuda = False
            self.__languages_configuration = None
            self.__tf_graph = None
            self.__models_loaded = False
            self.__loadConfiguration()
            
        def __downloadEmbeddings(self):
            print(f"Downloading bert model")
            subprocess.run([f"{self.__global_configuration['embeddingsScripts']}/download_BERT.sh"], check=True)
            print(self.__supported_languages)
            for language in self.__supported_languages:
                print(f"Downloading embeddings for {language}")
                subprocess.run([f"{self.__global_configuration['embeddingsScripts']}/fasttext_embeddings.sh", language, self.__languages_configuration[language]["fastTextSha"], f"Getting embeddings for {language}"], check=True)

        @synchronized_method
        def loadModels(self):
            if not self.__models_loaded:
                #We need to download here the embeddings, because we need the object running as fast as possible
                self.__downloadEmbeddings()
                self.__loadModels()
                print("Models have been loaded")
            else:
                print("Models were loaded before")

        def getUseCuda(self):
            return self.__global_configuration["use_cuda"]

        def getSupportedLanguages(self):
            return self.__supported_languages

        def getFasttextPath(self):
            return self.__global_configuration["fasttext_path"]

        def getKomninosPath(self):
            return self.__global_configuration["komninos_path"]

        def getModelBasePath(self):
            return self.__global_configuration["model_base_path"]

        def __loadConfiguration(self):
            with open("./config.json") as json_file:
                configuration = json.load(json_file)
            self.__languages_configuration = configuration["languagesConfiguration"]
            if "loadLanguages" in configuration.keys():
                load_languages = configuration["loadLanguages"]
                self.__supported_languages = list(set(load_languages) & self.__languages_configuration.keys())
                for language in list(self.__languages_configuration.keys()):
                    if language not in self.__supported_languages:
                        del(self.__languages_configuration[language])
            else:
                self.__supported_languages = list(self.__languages_configuration.keys())

            self.__global_configuration = {"fasttextPath": configuration["fasttextPath"],
                                           "komninosPath": configuration["komninosPath"],
                                           "modelBasePath": configuration["modelBasePath"],
                                           "useCuda": configuration["useCuda"],
                                           "embeddingsScripts": configuration["embeddingsScripts"]}

        def setTFGraph(self):
            import keras
            if keras.backend.backend() == "tensorflow":
                import tensorflow as tf
                self.__tf_graph = tf.get_default_graph()

        def __loadModels(self):
            self.setTFGraph()
            print("Loading models")
            for language in self.__supported_languages:
                if language not in self.__loaded_models:
                    try:
                        self.__loaded_models[language] = loadModelsWithConfig(language, self.__languages_configuration[language], self.__global_configuration, tf_graph=self.__tf_graph)
                        self.__models_loaded = True
                    except Exception:
                        traceback.print_exc()
                        self.__models_loaded = False
                        break

        def areModelsLoaded(self):
            return self.__models_loaded

        def getModel(self, language):
            if language in self.__supported_languages:
                if language in self.__loaded_models:
                    model = self.__loaded_models[language]
                else:
                    raise Exception("Language supported but model not found")
            else:
                raise Exception("Language not supported")
            return model

        def getTFGraph(self):
            return self.__tf_graph

    def __init__(self):
        super()
        print("I'm creating service in constructor")
        if NERService.__NER_instance is None:
            self.__createNERService()

    #We ensure that only one NER Service is created at the beginning
    #The syncronized method will block the creation until one has finished
    @synchronized_method
    def __createNERService(self):
        if NERService.__NER_instance is None:
            NERService.__NER_instance = NERService.__NERSingleton()

    def exposed_loadModels(self):
        NERService.__NER_instance.loadModels()

    def exposed_processNERRequest(self, language, data_set):
        try:
            model = NERService.__NER_instance.getModel(language)
            tags = getTags(data_set, model, tf_graph=NERService.__NER_instance.getTFGraph())
            json_output = generateDictOutput(data_set, tags)
        except Exception as e:
            raise e
        return json_output

    def exposed_createDataset(self, text, input_format):
        return readText(text, input_format)

    def exposed_getSupportedLanguages(self):
        return NERService.__NER_instance.getSupportedLanguages()

    def exposed_areModelsLoaded(self):
        return NERService.__NER_instance.areModelsLoaded()


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    port = os.getenv("NER_SERVICE_PORT")
    if port is None:
        port = 18861
    else:
        port = int(port)
    t = ThreadedServer(NERService, port=port,  protocol_config={'allow_pickle': True})
    t.start()
