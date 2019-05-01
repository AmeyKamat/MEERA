import sys
import os
from copy import deepcopy
from threading import Thread

from configparser import ConfigParser

import nlp.training.ner as ner
import nlp.training.textcat as textcat
import nlp.training.data as data
from definitions import ROOT_DIR, ABS_MODELS_DIR

def get_number_of_skill_utterances(training_data):
    skill_data = training_data["skill_data"]
    return len(skill_data)

def get_number_of_intents(training_data):
    intents = training_data["intents"]
    return len(intents)

def get_number_of_tagged_entities(training_data):
    tagged_entities = training_data["skill_data"]
    counter = 0
    for record in tagged_entities:
        counter += len(record["entities"])
    return counter

def get_number_of_entity_classes(training_data):
    entity_classes = training_data["entities"]
    return len(entity_classes)

def get_number_of_chat_categories(training_data):
    chat_categories = training_data["chat_categories"]
    return len(chat_categories)


def main():
    config = ConfigParser()
    config.read(os.path.join(ROOT_DIR, 'nlp', 'component.ini'))

    training_data = data.get_data()

    print("# of utterance: {}".format(get_number_of_skill_utterances(training_data)))
    print()
    print("# of intents: {}".format(get_number_of_intents(training_data)))
    print("Intents: " + training_data["intents"].__str__())
    print()
    print("# of entity classes: {}".format(get_number_of_entity_classes(training_data)))
    print("# of tagged entities: {}".format(get_number_of_tagged_entities(training_data)))
    print("Entity classes: " + training_data["entities"].__str__())
    print()
    print("# of chat categories: {}".format(get_number_of_chat_categories(training_data)))
    print("Chat categories: " + training_data["chat_categories"].__str__())

    iterations = int(sys.argv[1])

    intent_training_thread = Thread(
        target=textcat.train,
        args=(
            "en.assistant.intent.model",
            os.path.join(ABS_MODELS_DIR, config['models']['intent']),
            training_data["intents"],
            deepcopy(training_data["skill_data"]),
            iterations
        )
    )

    entity_traning_thread = Thread(
        target=ner.train,
        args=(
            "en.assistant.entity.model",
            os.path.join(ABS_MODELS_DIR, config['models']['entities']),
            training_data["entities"],
            deepcopy(training_data["skill_data"]),
            iterations
        )
    )

    chat_training_thread = Thread(
        target=textcat.train,
        args=(
            "en.assistant.chat.model",
            os.path.join(ABS_MODELS_DIR, config['models']['chat']),
            training_data["chat_categories"],
            deepcopy(training_data["chat_data"]),
            iterations
        )
    )

    request_type_training_thread = Thread(
        target=textcat.train,
        args=(
            "en.assistant.requestType.model",
            os.path.join(ABS_MODELS_DIR, config['models']['request-type']),
            training_data["request_types"],
            deepcopy(training_data["request_type_data"]),
            iterations
        )
    )

    #entity_traning_thread.start()
    #intent_training_thread.start()
    chat_training_thread.start()
    #request_type_training_thread.start()

    #intent_training_thread.join()
    chat_training_thread.join()
    #request_type_training_thread.join()
    #entity_traning_thread.join()

if __name__ == '__main__':
    main()
