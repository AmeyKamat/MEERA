from pathlib import Path
import os

import spacy
from spacy.util import minibatch, compounding, decaying

INTENT_SPLIT = 0.8

def train(modelName, outputDirectory, categories, trainingData, iterations=20):
    model = spacy.blank('en')
    model.meta['name'] = modelName
    
    textcat = model.create_pipe('textcat')
    model.add_pipe(textcat)

    for category in categories:
        textcat.add_label(category)

    split = int(len(trainingData) * INTENT_SPLIT)
    #trainingTexts = [ data["sentence"] for data in trainingData ][:split]
    #trainingCategories = [ data["category"] for data in trainingData ][:split]
    #evaluationTexts = [ data["sentence"] for data in trainingData ][split:]
    #evaluationCategories = [ data["category"] for data in trainingData ][split:]
    trainingTexts = [ data["sentence"] for data in trainingData ]
    trainingCategories = [ data["category"] for data in trainingData ]

    zippedTrainingData = list(zip(trainingTexts,
                          [{'cats': cats} for cats in trainingCategories]))

    other_pipes = [pipe for pipe in model.pipe_names if pipe != 'textcat']
    
    with model.disable_pipes(*other_pipes):  # only train textcat
        optimizer = model.begin_training()
        
        #print('{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}'.format('Iter #', 'LOSS', 'P', 'R', 'F'))
        
        for i in range(iterations):
            losses = {}
            
            batches = minibatch(zippedTrainingData, size=compounding(4., 32., 1.001))
            dropout = decaying(0.6, 0.2, 1e-4)
            
            for batch in batches:
                texts, annotations = zip(*batch)

                model.update(texts, annotations, sgd=optimizer, drop=0.2,
                           losses=losses)
            #with textcat.model.use_params(optimizer.averages):
            #    scores = evaluate(model.tokenizer, textcat, evaluationTexts, evaluationCategories)
            print('{}({}/{})\t\t\t\t\t\tloss={}'.format(modelName, i, iterations, losses['textcat']))
            #print('{0}: {1}\t{2:.3f}\t{3:.3f}\t{4:.3f}\t{5:.3f}'
            #      .format(modelName, i, losses['textcat'], scores['textcat_p'],
            #              scores['textcat_r'], scores['textcat_f']))

    if outputDirectory is not None:
        outputDirectory = Path(outputDirectory)
        if not outputDirectory.exists():
            outputDirectory.mkdir()
        model.to_disk(outputDirectory)
        print("Saved model to", outputDirectory)

def evaluate(tokenizer, textcat, texts, cats):
    docs = (tokenizer(text) for text in texts)
    tp = 1e-8  # True positives
    fp = 1e-8  # False positives
    fn = 1e-8  # False negatives
    tn = 1e-8  # True negatives
    for i, doc in enumerate(textcat.pipe(docs)):
        gold = cats[i]
        for label, score in doc.cats.items():
            if label not in gold:
                continue
            if score >= 0.5 and gold[label] >= 0.5:
                tp += 1.
            elif score >= 0.5 and gold[label] < 0.5:
                fp += 1.
            elif score < 0.5 and gold[label] < 0.5:
                tn += 1
            elif score < 0.5 and gold[label] >= 0.5:
                fn += 1
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f_score = 2 * (precision * recall) / (precision + recall)
    return {'textcat_p': precision, 'textcat_r': recall, 'textcat_f': f_score}