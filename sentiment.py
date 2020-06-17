# coding: utf-8

"""For correct work in runtime the packages :
sklearn, XGBoost should be installed.
module preprocessor also necessary, because stored vectorizer
model using tokenizer from it.

In case of troubles or inconvinience contact Ugulava George."""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pickle

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

vectorizer_file = open('sentiment_vectorizer.pickle','rb')
classifier_file = open('sentiment_classifier.pickle', 'rb')
classifier = pickle.load(classifier_file)
vectorizer = pickle.load(vectorizer_file)

def predict(message):
    '''messages the list of the messages to be classified
    returns label of the single message :
    1.0 - stands for positive label
    2.0 - stands for negative label
    3.0 - stands for neutral label
    '''
    message = [message]
    vectorized_message = vectorizer.transform(message)
    predictions = classifier.predict(vectorized_message)
    return str(int(predictions[0]))

def predict_collection(messages):
    '''messages the list of the messages to be classified
    returns the list of the predicted labels :
    1.0 - stands for positive label
    2.0 - stands for negative label
    3.0 - stands for neutral label
    '''
    vectorized_messages = vectorizer.transform(messages)
    predictions = classifier.predict(vectorized_messages)
    return predictions
