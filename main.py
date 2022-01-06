import os

import speech_recognition as sr
import pyttsx3
import requests
import csv
# import speech

from predictions import *

# baseUrl= 'http://localhost:8091/lolyapi/v1/users'
baseUrl = 'http://lolymidiapi.espol.edu.ec/api/lolyapi/v1'
token = ''
urlRobot= 'https://634a-200-126-19-106.ngrok.io'

tags = []
eventsId = []
pathBiblioteca = './biblioteca.csv'

robotName = 'BOBBY'
idEventoStop = '28'

# engine = pyttsx3.init('sapi5')
# engine = pyttsx3.init('dummy')
engine = pyttsx3.init()
engine.setProperty('voice', 'spanish-latin-am')
voices = engine.getProperty('voices')

for voice in voices:
    print(voice)

engine.setProperty('voice', voices[1].id)



def getToken():
  try:
    url = baseUrl + '/auth/login'
    resp = requests.post(url,
                         json={
                           "username": "dmaroto",
                           "password": "ingles+4"
                         })
  except:
    print("Something went wrong")
    return "None"
  return resp.headers.get('Authorization').split(' ')[1]


def speak(audio):
  print('this is the audio que speak capta:', audio)
  audio = audio + 'palabraex'
  # print('entre a funcion de hablar')
  engine.say(audio)
  engine.runAndWait()
  # engine.stop()
  print('voy a detener el robot')
  stopMovementRobot()

  # speech.say(audio, 'es_ES')

def takeCommand():
  # transform the audio of the microphone to text (recognize voice)
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print('Escuchando...')
    audio = r.listen(source)

    try:
      print('Reconociendo...')
      query = r.recognize_google(audio, language='es')
      print('Has dicho: {}'.format(query))
    except sr.UnknownValueError:
      print("Google Speech Recognition no pudo entender el audio")
      return "None"
    except sr.RequestError as e:
      print("No se pudieron solicitar los resultados del servicio de reconocimiento de voz de Google; {0}".format(e))
      return "None"
    return query

def startMovementRobot(idEvento):
  try:
    url = baseUrl + '/send/' + idEvento
    resp = requests.post(url,
                         json={
                           "urlRobot": urlRobot,
                         }, headers={'Authorization': 'Bearer ' + token})
    print('response: ', resp)
  except:
    print("Something went wrong startMovementRobot with the event: " + idEvento)

# def calculateTimeAudioResponse(audio):

def stopMovementRobot():
  try:
    url = baseUrl + '/send/' + idEventoStop
    resp = requests.post(url,
                         json={
                           "urlRobot": urlRobot,
                         }, headers={'Authorization': 'Bearer ' + token})
  except:
    print("Something went wrong in stopMovementRobot")

def fillInformationfromBiblioteca(path):
  with open(path, newline='') as File:
    reader = csv.reader(File)
    for row in reader:
      tag,idEvent = row[0].split(";")
      tags.append(tag)
      eventsId.append(idEvent)


def searchIdEventOfBiblioteca(tagIntent):
    index = tags.index(tagIntent)
    id = eventsId[index]
    return id



if __name__ == '__main__':
  token = getToken()
  fillInformationfromBiblioteca(pathBiblioteca)
  clear = lambda: os.system('cls')
  while True:
    query = takeCommand().lower()
    result, tag = chatbot_response(query)
    idEvent = searchIdEventOfBiblioteca(tag)
    startMovementRobot(idEvent)
    speak(result)


