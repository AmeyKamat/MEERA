import random
from pathlib import Path

import spacy
from spacy.util import minibatch, compounding

def train(model_name, model_directory, entity_types, training_data, iterations=20):

    model = get_model(model_name, model_directory)
    optimizer = setup_pipeline(model, entity_types)
    formatted_training_data = get_formatted_training_data(training_data)

    other_pipes = [pipe for pipe in model.pipe_names if pipe != 'ner']

    with model.disable_pipes(*other_pipes):
        for iteration in range(iterations):
            random.shuffle(formatted_training_data)
            losses = {}
            batches = minibatch(formatted_training_data, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                model.update(texts, annotations, drop=0.5, losses=losses, sgd=optimizer)
            print('{0:40}\t\t\t\t\t\tloss={1}'.format(
                "{0}({1}/{2})".format(model_name, iteration, iterations),
                losses['ner']))

    save_model(model, model_directory)

def get_model(model_name, model_directory):
    model_path = Path(model_directory)
    if model_path is not None and model_path.exists():
        model = spacy.load(model_path)
        print("Loaded model from {0}".format(model_directory))
    else:
        model = spacy.blank('en')
        print("No existing model found created new")

    model.meta['name'] = model_name
    return model

def setup_pipeline(model, entity_types):
    if 'ner' not in model.pipe_names:
        ner = model.create_pipe('ner')
        model.add_pipe(ner)
    else:
        ner = model.get_pipe('ner')

    optimizer = model.begin_training()

    for entity_type in entity_types:
        ner.add_label(entity_type)
        optimizer = model.entity.create_optimizer()
    return optimizer

def get_formatted_training_data(training_data):
    return [
        (
            data["sentence"],
            {"entities": data["entities"]}
        ) for data in training_data
    ]

def save_model(model, model_directory):
    if model_directory is not None:
        model_path = Path(model_directory)
        if not model_path.exists():
            model_path.mkdir()
        model.to_disk(model_path)
        print("Saved model to", model_path)
