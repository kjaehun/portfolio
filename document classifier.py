## Document Classification
## 09/28/2021

# for windows 10, need to specify UTF-8 encoding
# given a corpus with two possible labels: 2016, 2020
# train classifier to determine the most likely label of a query document

import os
import math


def load_training_data(vocab, directory):
    """ Create the list of dictionaries """
    top_level = os.listdir(directory)
    dataset = []
    for d in top_level:
        if d[0]=='.': # to skip hidden directories for e.g.  '.DStore' directory
            continue
        if d[-1] == '/':
            label = d[:-1]
            subdir = d
        else:
            label = d
            subdir = d+"/"
        files = os.listdir(directory+subdir)
        for f in files:
            bow = create_bow(vocab, directory+subdir+f)
            dataset.append({'label': label, 'bow': bow})
    return dataset

def create_vocabulary(directory, cutoff):
    """ Create a vocabulary from the training directory
        return a sorted vocabulary list
    """

    top_level = os.listdir(directory)
    vocab = {}
    for d in top_level:
        if d[0]=='.': # to skip hidden directories for e.g.  '.DStore' directory
            continue  
        subdir = d if d[-1] == '/' else d+'/'
        files = os.listdir(directory+subdir)
        for f in files:
            with open(directory+subdir+f,'r') as doc:
                for word in doc:
                    word = word.strip()
                    if not word in vocab and len(word) > 0:
                        vocab[word] = 1
                    elif len(word) > 0:
                        vocab[word] += 1
    return sorted([word for word in vocab if vocab[word] >= cutoff])

def create_bow(vocab, filepath):
    """ Create a single dictionary for the data
        Note: label may be None
    """
    bow = {}
    with open(filepath, 'r') as doc:
        for word in doc:
            word = word.strip()
            if word in vocab and not word in bow and len(word) > 0:
                bow[word] = 1
            elif word in vocab and len(word) > 0:
                bow[word] += 1
            elif len(word) > 0 and not None in bow:
                bow[None] = 1
            elif len(word) > 0:
                bow[None] += 1
    return bow

def prior(training_data, label_list):
    """ return the prior probability of the label in the training set
        => frequency of DOCUMENTS
    """

    smooth = 1 # smoothing factor
    logprob = {}
    label2016 = 0
    label2020 = 0
    for item in training_data:
        if item["label"] == "2016":
            label2016 += 1
        else:
            label2020 += 1

    logprob['2020'] = math.log(label2020 + smooth) - math.log(label2016 + label2020 + 2)
    logprob['2016'] = math.log(label2016 + smooth) - math.log(label2016 + label2020 + 2)

    return logprob

def p_word_given_label(vocab, training_data, label):
    """ return the class conditional probability of label over all words, with smoothing """

    smooth = 1 # smoothing factor
    word_prob = {}
    total = 0
    size = len(vocab)
    for item in training_data: # get total word count for label
        if item["label"] == label:
            for key in item["bow"]:
                total += item["bow"][key]

    for word in vocab:
        wordcount = 0
        for item in training_data:
            if item["label"] == label:
                if word in item["bow"]:
                    wordcount += item["bow"][word]
        word_prob[word] = math.log((wordcount + smooth * 1) / (total + smooth * (size + 1)))

    wordcount = 0
    for item in training_data:
        if item["label"] == label:
            if None in item["bow"]:
                wordcount += item["bow"][None]
    word_prob[None] = math.log((wordcount + smooth * 1) / (total + smooth * (size + 1)))
    
    return word_prob

def train(training_directory, cutoff):
    """ return a dictionary formatted as follows:
            {
             'vocabulary': <the training set vocabulary>,
             'log prior': <the output of prior()>,
             'log p(w|y=2016)': <the output of p_word_given_label() for 2016>,
             'log p(w|y=2020)': <the output of p_word_given_label() for 2020>
            }
    """
    retval = {}
    label_list = os.listdir(training_directory)

    vocab = create_vocabulary(training_directory, cutoff)
    training_data = load_training_data(vocab, training_directory)
    pr = prior(training_data, ['2020', '2016'])
    
    retval['vocabulary'] = vocab
    retval['log prior'] = pr
    retval['log p(w|y=2020)'] = p_word_given_label(vocab, training_data, '2020')
    retval['log p(w|y=2016)'] = p_word_given_label(vocab, training_data, '2016')


    return retval

def classify(model, filepath):
    """ return a dictionary formatted as follows:
            {
             'predicted y': <'2016' or '2020'>,
             'log p(y=2016|x)': <log probability of 2016 label for the document>,
             'log p(y=2020|x)': <log probability of 2020 label for the document>
            }
    """
    retval = {}
    dict2016 = model['log p(w|y=2016)']
    dict2020 = model['log p(w|y=2020)']
    vocab = model['vocabulary']
    sum2016 = 0
    sum2020 = 0

    bow = create_bow(vocab, filepath)
    for word in bow:
        sum2016 += (bow[word]) * (dict2016[word])
        sum2020 += (bow[word]) * (dict2020[word])

    sum2016 += model['log prior']['2016']
    sum2020 += model['log prior']['2020']

    retval['log p(y=2020|x)'] = sum2020
    retval['log p(y=2016|x)'] = sum2016
    if sum2016 > sum2020:
        retval['predicted y'] = '2016'
    else:
        retval['predicted y'] = '2020'


    return retval
