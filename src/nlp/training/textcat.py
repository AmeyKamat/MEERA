from pathlib import Path

import spacy
from spacy.util import minibatch, compounding

def train(model_name, model_directory, categories, training_data, iterations=20):

    model = get_model(model_name, model_directory)
    setup_pipeline(model, categories)
    zipped_training_data = get_zipped_training_data(training_data)

    other_pipes = [pipe for pipe in model.pipe_names if pipe != 'textcat']

    with model.disable_pipes(*other_pipes):  # only train textcat
        optimizer = model.begin_training()

        for i in range(iterations):
            losses = {}

            for batch in minibatch(zipped_training_data, size=compounding(4., 32., 1.001)):
                texts, annotations = zip(*batch)
                model.update(texts, annotations, sgd=optimizer, drop=0.2, losses=losses)

            print('{0:40}\t\t\t\t\t\tloss={1}'.format(
                "{0}({1}/{2})".format(model_name, i, iterations),
                losses['textcat']))

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

def setup_pipeline(model, categories):
    if 'textcat' not in model.pipe_names:
        textcat = model.create_pipe('textcat')
        model.add_pipe(textcat)
    else:
        textcat = model.get_pipe('textcat')

    for category in categories:
        textcat.add_label(category)

def get_zipped_training_data(training_data):
    training_texts = [data["sentence"] for data in training_data]
    training_categories = [data["category"] for data in training_data]

    return list(
        zip(
            training_texts,
            [{'cats': cats} for cats in training_categories]
        )
    )

def save_model(model, model_directory):
    if model_directory is not None:
        model_path = Path(model_directory)
        if not model_path.exists():
            model_path.mkdir()
        model.to_disk(model_path)
        print("Saved model to", model_path)
