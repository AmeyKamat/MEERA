import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding

def train(modelName, outputDirectory, entityTypes, trainingData, iterations=20):
    
    model = spacy.blank('en')
    model.meta['name'] = modelName
    
    ner = model.create_pipe('ner')
    model.add_pipe(ner)
        
    optimizer = model.begin_training()
    
    for type in entityTypes:
        ner.add_label(type)
        optimizer = model.entity.create_optimizer()

    formattedTrainingData = [(data["sentence"], {"entities": data["entities"]}) for data in trainingData]

    other_pipes = [pipe for pipe in model.pipe_names if pipe != 'ner']

    with model.disable_pipes(*other_pipes):
        for iteration in range(iterations):
            random.shuffle(formattedTrainingData)
            losses = {}
            batches = minibatch(formattedTrainingData, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                model.update(texts, annotations, drop=0.5, losses=losses, sgd=optimizer)
            print('{}({}/{})\t\t\t\t\t\tloss={}'.format(modelName, iteration, iterations, losses['ner']))

    if outputDirectory is not None:
        outputDirectory = Path(outputDirectory)
        if not outputDirectory.exists():
            outputDirectory.mkdir()
        model.to_disk(outputDirectory)
        print("Saved model to", outputDirectory)