from __future__ import unicode_literals, print_function
import random
from pathlib import Path
import sys, os

import spacy
from spacy.util import minibatch, compounding, decaying

INTENT_SPLIT = 0.8


def train(modelName, outputDirectory, categories, trainingData, iterations=20):
    model = spacy.blank('en')
    model.meta['name'] = modelName
    
    ner = model.create_pipe('ner')
    model.add_pipe(ner)

    for category in categories:
        textcat.add_label(category)

    split = len(trainingData) * INTENT_SPLIT
    trainingTexts = [ data["text"] for data in trainingData ][:split]
    trainingCategories = [ data["category"] for data in trainingData ][:split]
    evaluationTexts = [ data["text"] for data in trainingData ][split:]
    evaluationCategories = = [ data["category"] for data in trainingData ][split:]

    print("Using {} examples ({} training, {} evaluation)"
          .format(n_texts, len(trainingTexts), len(evaluationTexts)))

    zippedTrainingData = list(zip(trainingTexts,
                          [{'cats': cats} for cats in trainingCategories]))

    other_pipes = [pipe for pipe in model.pipe_names if pipe != 'textcat']
    
    with model.disable_pipes(*other_pipes):  # only train textcat
        optimizer = model.begin_training()

        print("Training the model...")
        print('{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}'.format('Iter #', 'LOSS', 'P', 'R', 'F'))
        
        for i in range(iterations):
            losses = {}
            # batch up the examples using spaCy's minibatch
            #batches = get_batches(train_data, 'textcat')
            batches = minibatch(train_data, size=compounding(4., 32., 1.001))
            dropout = decaying(0.6, 0.2, 1e-4)
            for batch in batches:
                texts, annotations = zip(*batch)

                nlp.update(texts, annotations, sgd=optimizer, drop=0.2,
                           losses=losses)
            with textcat.model.use_params(optimizer.averages):
                # evaluate on the dev data split off in load_data()
                scores = evaluate(nlp.tokenizer, textcat, dev_texts, dev_cats)
            print('{0}\t{1:.3f}\t{2:.3f}\t{3:.3f}\t{4:.3f}'  # print a simple table
                  .format(i, losses['textcat'], scores['textcat_p'],
                          scores['textcat_r'], scores['textcat_f']))

    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

def get_batches(train_data, model_type):
    max_batch_sizes = {'tagger': 32, 'parser': 16, 'ner': 16, 'textcat': 64}
    max_batch_size = max_batch_sizes[model_type]
    if len(train_data) < 1000:
        max_batch_size /= 2
    if len(train_data) < 500:
        max_batch_size /= 2
    batch_size = compounding(1, max_batch_size, 1.001)
    batches = minibatch(train_data, size=batch_size)
    return batches


def load_data(categories, limit=0, split=0.8):
    """Load data from the IMDB dataset."""
    # Partition off part of the train data for evaluation
    test_file = open('test_data.txt', "r")
    texts = []
    labels = []
    lines = []
    cats=[]
    for line in test_file:
        lines.append(line)
    random.shuffle(lines)
    print(limit)
    lines = lines[-limit:]
    
    for line in lines:
        test_sentence, intent = line.split('|');
        texts.append(test_sentence.strip())
        labels.append(intent.strip())

    category_counter  = {}
    for category in categories:
        category_counter[category] = 0

    for label in labels:
        category_counter[label] = category_counter[label] + 1
    
    print("Total training data set: ")
    print(category_counter)

    for label in labels:
        catsForRecord = {}
        for category in categories:
            if category == label:
                catsForRecord[category] = 1.0
            else:
                catsForRecord[category] = 0.0
        cats.append(catsForRecord)
        flag = 0;
        for key, value in catsForRecord.items():
            if(value == 1):
                flag = 1
        if(flag==0):
            print(str(catsForRecord), " ", str(label))
            
    test_file.close()
    split = int(len(texts) * split)
    return (texts[:split], cats[:split]), (texts[split:], cats[split:])


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