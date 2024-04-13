import random
import json
import pickle
import numpy as np
import tensorflow as tf

import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

from nltk.stem import WordNetLemmatizer

lemmatizer=WordNetLemmatizer()

nltk.download('punkt')
nltk.download('wordnet')

words=[]
classes=[]
documents=[]
ignoreList = ['?','!',',',"'s"]

data_file=open('TextToTextBot/intents.json').read()
intents=json.loads(data_file)

for intent in intents['intents']:
    for pattern in intent['patterns']:
        wordList=nltk.word_tokenize(pattern)
        words.extend(wordList)
        documents.append((wordList,intent['tag']))       
        if intent['tag'] not in classes:
            classes.append(intent['tag'])
            
words=[lemmatizer.lemmatize(word.lower()) for word in words if word not in ignoreList]
words=sorted(list(set(words)))

classes=sorted(list(set(classes)))

pickle.dump(words,open('TextToTextBot/words.pkl','wb'))
pickle.dump(classes,open('TextToTextBot/classes.pkl','wb'))

#training data
training=[]
outputEmpty= [0] * len(classes)

for doc in documents:
    bag=[]
    pattern= doc[0]
    pattern= [lemmatizer.lemmatize(word.lower()) for word in pattern]
    
    for word in words: bag.append(1) if word.lower() in pattern else bag.append(0)
    output_row=list(outputEmpty)
    output_row[classes.index(doc[1])]=1
    
    training.append(bag + output_row)
    
random.shuffle(training)

training=np.array(training).reshape(-1,1)

X_train=list(training[:, :len(words)])
y_train=list(training[:, :len(words)])

model = Sequential()

model.add(Dense(128, input_shape=(1,), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
# model.add(Dropout(0.5))
model.add(Dense(len(y_train[0]), activation='softmax'))

sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

h5model = model.fit(np.array(X_train), np.array(y_train), epochs=200, batch_size=5, verbose=1)
model.save('chatbot.h5', h5model)