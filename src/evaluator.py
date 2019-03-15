import os

from configparser import ConfigParser
from spacy import load


import nlp.training.data as data
from definitions import ROOT_DIR, ABS_MODELS_DIR

def get_config():
    config = ConfigParser()
    config.read(os.path.join(ROOT_DIR, 'nlp', 'component.ini'))
    return config

CONFIG = get_config()

# analyse intents

def get_intent_model_accuracy(test_data):
    model = load(os.path.join(ABS_MODELS_DIR, CONFIG['models']['intent']))

    correct_predictions = 0
    total_predictions = 0

    for example in test_data["skill_data"]:
        total_predictions = total_predictions + 1
        utterance = example["sentence"]
        expected_intent = example["category"]
        prediction = model(utterance)
        predicted_intent = sorted(prediction.cats, key=prediction.cats.get, reverse=True)[0]
        if expected_intent[predicted_intent] == 1.0:
            correct_predictions = correct_predictions + 1
    return correct_predictions*100/total_predictions




# analyse requestType

def get_request_type_model_accuracy(test_data):
    model = load(os.path.join(ABS_MODELS_DIR, CONFIG['models']['request-type']))

    correct_predictions = 0
    total_predictions = 0

    for example in test_data["request_type_data"]:
        total_predictions = total_predictions + 1
        utterance = example["sentence"]
        expected_request_type = example["category"]
        prediction = model(utterance)
        predicted_request_type = sorted(prediction.cats, key=prediction.cats.get, reverse=True)[0]
        if expected_request_type[predicted_request_type] == 1.0:
            correct_predictions = correct_predictions + 1
    return correct_predictions*100/total_predictions




# analyse chat

def get_chat_model_accuracy(test_data):
    model = load(os.path.join(ABS_MODELS_DIR, CONFIG['models']['chat']))

    correct_predictions = 0
    total_predictions = 0

    for example in test_data["chat_data"]:
        total_predictions = total_predictions + 1
        utterance = example["sentence"]
        expected_chat_response = example["category"]
        prediction = model(utterance)
        predicted_chat_response = sorted(prediction.cats, key=prediction.cats.get, reverse=True)[0]
        if expected_chat_response[predicted_chat_response] == 1.0:
            correct_predictions = correct_predictions + 1
    return correct_predictions*100/total_predictions



# analyse entites

def get_entites_model_accuracy(test_data):
    model = load(os.path.join(ABS_MODELS_DIR, CONFIG['models']['entities']))

    correct_predictions = 0
    total_predictions = 0

    for example in test_data["skill_data"]:
        utterance = example["sentence"]
        expected_entities = example["entities"]
        prediction = model(utterance)
        predicted_entities = {}

        for ent in prediction.ents:
            predicted_entities[ent.label_] = ent.text

        for expected_entity in expected_entities:
            total_predictions = total_predictions + 1
            if expected_entity[2] in predicted_entities.keys():
                expected_entity_text = utterance[expected_entity[0]:expected_entity[1]]
                if expected_entity_text == predicted_entities[expected_entity[2]]:
                    correct_predictions = correct_predictions + 1
    return correct_predictions*100/total_predictions

def main():

    test_data = data.get_data()

    try:
        print("Intent Classifier Accuracy: {} percent".format(
            get_intent_model_accuracy(test_data)))
    # pylint: disable=broad-except
    except Exception:
        print("Error calculating accuracy of Intent Classifier")

    try:
        print("Request Type Classifier Accuracy: {} percent".format(
            get_request_type_model_accuracy(test_data)))
    # pylint: disable=broad-except
    except Exception:
        print("Error calculating accuracy of Request Type Classifier")

    try:
        print("Chat Classifier Accuracy: {} percent".format(get_chat_model_accuracy(test_data)))
    # pylint: disable=broad-except
    except Exception:
        print("Error calculating accuracy of Chat Classifier")

    try:
        print("Entities NER Accuracy: {} percent".format(get_entites_model_accuracy(test_data)))
    # pylint: disable=broad-except
    except Exception:
        print("Error calculating accuracy of Entities NER")

if __name__ == '__main__':
    main()
