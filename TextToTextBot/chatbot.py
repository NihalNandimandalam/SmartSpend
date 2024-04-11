# import random
# import json
# import pickle
# import numpy as np

# import nltk
# from nltk.stem import WordNetLemmatizer

# from keras.models import load_model

# lemmatiser = WordNetLemmatizer()
# intents = json.loads(open('TextToTextBot/intents.json').read())

# words = pickle.load(open('TextToTextBot/words.pkl', 'rb'))
# classes = pickle.load(open('TextToTextBot/classes.pkl', 'rb'))
# model = load_model('chatbot.h5')

# def clean_up_sentence(sentence):
#     sentence_words = nltk.word_tokenize(sentence)
#     sentence_words = [lemmatiser.lemmatize(word) for word in sentence_words]
#     return sentence_words

# def bag_of_words(sentence):
#     sentence_words = clean_up_sentence(sentence)
#     bag = [0] * len(words)
#     for w in sentence_words:
#         for i, word in enumerate(words):
#             if word == w:
#                 bag[i] = 1
#     return np.array(bag)

# def predict_class(sentence):
#     bow = bag_of_words(sentence)
#     res = model.predict(np.array([bow]))[0]

#     error_threshold = 0.25
#     results = [[i, r] for i, r in enumerate(res) if r > error_threshold]

#     results.sort(key=lambda x: x[1], reverse=True)
#     return_list=[]
#     for r in results:
#         return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
#     return return_list

# def get_response(intents_list, intents_json):
#     tag = intents_list[0]['intents']
#     list_of_intents = intents_json['intents']
#     for i in list_of_intents:
#         if i['tag'] == tag:
#             result = random.choice(i['responses'])
#             break
#     return result

# print("Bot is ruuning")

# while True:
#     message = input("")
#     ints = predict_class(message)
#     res = get_response(ints, intents)
#     print(res)

import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import load_model

lemmatiser = WordNetLemmatizer()
intents = json.loads(open('TextToTextBot/intents.json').read())

words = pickle.load(open('TextToTextBot/words.pkl', 'rb'))
classes = pickle.load(open('TextToTextBot/classes.pkl', 'rb'))
model = load_model('chatbot.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatiser.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    # Reshape the bag-of-words vector to match the expected input shape of the model
    # res = model.predict(np.array([bow.reshape(1, -1)]))[0]
    bow_reshaped = bow.reshape((-1, 1))
    res = model.predict(bow_reshaped)[0]

    error_threshold = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > error_threshold]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list=[]
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

print("Bot is ruuning")

while True:
    message = input("")
    ints = predict_class(message)
    res = get_response(ints, intents)
    print(res)