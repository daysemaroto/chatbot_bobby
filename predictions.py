#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# get_ipython().system('pip install tensorflow keras nltk spacy-stanza')


# In[19]:


import pickle
import numpy as np
from keras.models import load_model
model = load_model('chatbot_model.h5')
# model = load_model('model_checkpoint.h5')

import json
import random

from utils import *


# In[15]:

with open('intents.json', encoding='utf-8') as fh:
    intents = json.load(fh)
#intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


# In[ ]:


classes


# In[13]:


def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = tokenize(final_sentence(sentence))
    #print(sentence_words)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    pattern=''
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                pattern = w
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print(f'found in bag: {w}')
    #print(np.array(bag))
    return(np.array(bag), pattern)
def predict_class(sentence, model):
    # filter out predictions below a threshold
    p, pattern = bow(sentence, words)
    return_list = []
    if np.any(p):
        res = model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.0
        results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        for r in results:
            return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    else:
        return_list.append({"intent": 'sin respuesta', "probability": '90.0'})
    #print(return_list)
    return return_list, pattern


# In[11]:


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result,tag
def chatbot_response(text):
    ints, pattern = predict_class(text.lower(), model)
    result,tag = getResponse(ints, intents)
    # print("esta es la respuesta: ", result)
    print('este es el tag: ', tag)
    return result,tag, pattern


# In[16]:


#chatbot_response("alo")


# In[3]:


#chatbot_response("HOLA")


# In[10]:


#chatbot_response("adios")


# In[11]:


#chatbot_response("QUIERO COMER ATUN")


# In[12]:


#chatbot_response("QUIERO COMER DULCES")


# In[13]:


#chatbot_response("qué haces")


# In[14]:


#chatbot_response("QUIERO COMER")


# In[17]:


#chatbot_response("QUIERO COMER CERDO")


# In[ ]:




