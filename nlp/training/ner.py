import random
from pathlib import Path
import spacy

def train(modelName, outputDirectory, entityTypes, trainingData, iterations=20):
    
    model = spacy.blank('en')
    model.meta['name'] = modelName
    
    ner = model.create_pipe('ner')
    model.add_pipe(ner)
        
    optimizer = model.begin_training()
    
    for type in entityTypes:
        ner.add_label(type)
        optimizer = model.entity.create_optimizer()

    other_pipes = [pipe for pipe in model.pipe_names if pipe != 'ner']

    with model.disable_pipes(*other_pipes):
        for iteration in range(iterations):
            random.shuffle(trainingData)
            losses = {}
            for text, entities in train_data:
                model.update([text], [entities], sgd=optimizer, drop=0.35,
                           losses=losses)
            print('losses in iteration',itn, ': ', losses['ner'])

    if outputDirectory is not None:
        outputDirectory = Path(outputDirectory)
        if not outputDirectory.exists():
            outputDirectory.mkdir()
        model.to_disk(outputDirectory)
        print("Saved model to", outputDirectory)