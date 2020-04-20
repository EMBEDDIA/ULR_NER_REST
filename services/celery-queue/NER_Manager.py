import json

from celeryApiUtils.synchronization import synchronized_method
from NER.NER import loadModelsWithConfig

# Singleton
class NERManager:
    class __NERManagerSingleton:
        def __init__(self):
            self.__loaded_models = {}
            self.__supported_languages = None
            self.__fasttext_path = None
            self.__komninos_path = None
            self.__model_base_path = None
            self.__use_cuda = False
            self.__configuration = self.__loadConfiguration()
            # We need to load in a better way BERT, to just load it once

        def getLanguageConfiguration(self, language):
            return self.__configuration[language]

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
            self.__supported_languages = configuration["languages"].keys()
            self.__global_configuration = {"fasttextPath": configuration["fasttextPath"],
                                           "komninosPath": configuration["komninosPath"],
                                           "modelBasePath": configuration["modelBasePath"],
                                           "useCuda": configuration["useCuda"],
                                           "embeddingsScripts" : configuration["embeddingsScripts"]}
            return configuration["languages"]

        @synchronized_method
        def getModel(self, language):
            if language in self.__supported_languages:
                if language not in self.__loaded_models:
                    model = loadModelsWithConfig(language, self.getLanguageConfiguration(language),
                                                 self.__global_configuration)
                    self.__loaded_models[language] = model
                else:
                    model = self.__loaded_models[language]
            else:
                raise Exception("Model not found")
            return model

    __instance = None

    def __init__(self):
        if NERManager.__instance is None:
            NERManager.__instance = NERManager.__NERManagerSingleton()

    def getLanguageConfiguration(self, language):
        return NERManager.__instance.getConfiguration(language)

    def getSupportedLanguages(self):
        return NERManager.__instance.getSupportedLanguages()

    def getModel(self, language):
        return NERManager.__instance.getModel(language)
