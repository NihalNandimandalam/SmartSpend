# from tkinter import *
# root = Tk()
# root.title("SmartSpend Bot")
# def send():
#     send = "Customer -> "+e.get()
#     txt.insert(END, "\n"+send)
#     user = e.get().lower()
#     if(user == "hello"):
#         txt.insert(END, "\n" + "Bot -> Hi")
#     elif(user == "hi" or user == "hii" or user == "hiiii"):
#         txt.insert(END, "\n" + "Bot -> Hello")
#     elif(e.get() == "how are you"):
#         txt.insert(END, "\n" + "Bot -> fine! and you")
#     elif(user == "fine" or user == "i am good" or user == "i am doing good"):
#         txt.insert(END, "\n" + "Bot -> Great! how can I help you.")
#     else:
#         txt.insert(END, "\n" + "Bot -> Sorry! I dind't get you")
#     e.delete(0, END)
# txt = Text(root)
# txt.grid(row=0, column=0, columnspan=2)
# e = Entry(root, width=100)
# e.grid(row=1, column=0)
# send = Button(root, text="Send", command=send).grid(row=1, column=1)
# root.mainloop()

#############################

# import random
# import json
# import pickle
# import numpy as np

# import nltk
# from nltk.stem import WordNetLemmatizer

# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Activation, Dropout
# from tensorflow.keras.optimizers import SGD

# lemmatiser = WordNetLemmatizer()

# intents = json.loads(open('TextToTextBot/intents.json').read())

# words = []
# classes = []
# documents = []
# ignore_char = ['?', '!', '.', ',']

# for intent in intents['intents']:
#     for pattern in intent['patterns']:
#         word_list = nltk.word_tokenize(pattern)
#         words.extend(word_list)
#         documents.append((word_list, intent['tag']))
#         if intent['tag'] not in classes:
#             classes.append(intent['tag'])

# # print(documents)

# words = [lemmatiser.lemmatize(word) for word in words if word not in ignore_char]
# words = sorted(set(words))
# classes = sorted(set(classes))

# pickle.dump(words, open('TextToTextBot/words.pkl', 'wb'))
# pickle.dump(classes, open('TextToTextBot/classes.pkl', 'wb'))

# # print(words)

# train = []
# # max_length = max(len(sublist) for sublist in train)
# # for i in range(len(train)):
# #     train[i] += [0] * (max_length - len(train[i]))
# output = [0] * len(classes)

# for document in documents:
#     bag = []
#     word_patterns = document[0]
#     word_patterns = [lemmatiser.lemmatize(word.lower()) for word in word_patterns]
#     for word in words:
#         bag.append(1) if word in word_patterns else bag.append(0)

#     output_row = list(output)
#     output_row[classes.index(document[1])] = 1
#     train.append([bag, output_row])

# random.shuffle(train)
# train = np.array(train)

# train_x = list(train[:, 0])
# train_y = list(train[:, 1])

# model = Sequential()
# model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
# model.add(Dropout(0.5))
# model.add(Dense(64, Activation='relu'))
# model.add(Dropout(0.5))
# model.add(Dense(len(train_y[0]), activation='softmax'))

# sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
# model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# h5model = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
# model.save('chatbot.h5', h5model)
# print("done")

#############################

import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()

words = []
classes = []
documents = []
ignore_char = ['?', '!', '.', ',']

data_file = open('TextToTextBot/intents.json').read()
intents = json.loads(data_file)

for intent in intents['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_char]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

pickle.dump(words, open('TextToTextBot/words.pkl', 'wb'))
pickle.dump(classes, open('TextToTextBot/classes.pkl', 'wb'))

train = []
output = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if w in word_patterns else bag.append(0)

    output_row = list(output)
    output_row[classes.index(document[1])] = 1
    train.append([bag, output_row])

random.shuffle(train)
train = np.array(train)

train_x = list(train[:, 0])
train_y = list(train[:, 1])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

h5model = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('chatbot.h5', h5model)
print("Done")
