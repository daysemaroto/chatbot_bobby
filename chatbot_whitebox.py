#!/usr/bin/env python
# coding: utf-8

# In[1]:


# get_ipython().system('pip install tensorflow keras nltk spacy-stanza')


# In[2]:


import tensorflow as tf
import json
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
import random
from keras.layers.normalization.batch_normalization import BatchNormalization


from utils import *


# In[3]:


words=[]
classes = []
documents = []
data_file = open('intents.json').read()
intents = json.loads(data_file)


# In[4]:


#tokenizing
for intent in intents['intents']:
    for pattern in intent['patterns']:
        #tokenizing
        w= tokenize(pattern)
        words.extend(w)
        #add documents in the corpus
        documents.append((w, intent['tag']))

        # add to our classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])


# In[5]:


classes


# In[6]:


fulltext = ' '.join(words)
# lemmatize, lower each word and remove duplicates
lemmas = lemmatize_without_stop(fulltext)
lemmas = sorted(list(set(lemmas)))
# sort classes
classes = sorted(list(set(classes)))

#removing accent and signs
lemmas = remove_accent_punct(lemmas)


# In[7]:


# documents = combination between patterns and intents
print (len(documents), "documents")
# classes = intents
print (len(classes), "classes", classes)
# words = all words, vocabulary
print (len(lemmas), "unique lemmatized words", lemmas)


# In[8]:


pickle.dump(lemmas,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))


# ## Exploring

# In[9]:


len(lemmas)


# In[10]:


documents[21]


# # TRAINING

# In[11]:


# create our training data
training = []
# create an empty array for our output
output_empty = [0] * len(classes)
# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # lemmatize each word - create base word, in attempt to represent related words
    pattern_words = lemmatize_with_stop(' '.join(pattern_words))
    if (pattern_words == 'frutonecer'):
        pattern_words == 'frutoseco'
    pattern_words  = remove_accent_punct(pattern_words)
    
    # create our bag of words array with 1, if word match found in current pattern
    for w in lemmas:
        bag.append(1) if w in pattern_words else bag.append(0)
    # output is a '0' for each tag and '1' for current tag (for each pattern)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])
# shuffle our features and turn into np.array
random.shuffle(training)
training = np.array(training)

print("Training data created")


# In[12]:


training[4:5,:]


# In[13]:


# create train and test lists. X - patterns, Y - intents
datafortrain = int(len(training)*0.9)

train_x = list(training[:datafortrain,0])
train_y = list(training[:datafortrain,1])

val_x = list(training[datafortrain:,0])
val_y = list(training[datafortrain:,1])


# In[14]:


path_checkpoint = "model_checkpoint.h5"
my_callbacks = [
    tf.keras.callbacks.EarlyStopping(monitor='loss',min_delta=0.000000000001,patience=30),
    tf.keras.callbacks.ModelCheckpoint(monitor="val_loss",
    filepath=path_checkpoint,
    verbose=1,
    save_weights_only=False,
    save_best_only=True,),
    tf.keras.callbacks.TensorBoard(log_dir='./logs'),
]


# In[17]:


#Batch normalization
model = Sequential()
model.add(Dense(256, input_shape=(len(train_x[0]),), activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(128, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))
# Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
sgd = SGD(lr=0.0001, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
#fitting and saving the model 

hist = model.fit(np.array(train_x), np.array(train_y), epochs=10000, batch_size=4, validation_data=(val_x, val_y), verbose=True, callbacks = my_callbacks)
model.save('chatbot_model.h5', hist)

print("model created")


# In[18]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

plt.rcParams["axes.grid"] = False
plt.rcParams.update({'font.size': 20})
plt.style.use("seaborn-ticks")

plt.plot(hist.history['accuracy'])
plt.plot(hist.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Training Acc', 'Test Acc'], loc='upper left')
plt.show()


# In[ ]:




