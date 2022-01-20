import os
import sys

import speech_recognition as sr
import pyttsx3
import requests
import csv
from predictions import *
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

baseUrl = os.getenv('BASE_URL')
token = ''
urlRobot = os.getenv('URL_ROBOT')
pathBiblioteca = os.getenv('PATH_BIBLIOTECA')
robotName = os.getenv('ROBOT_NAME')
idEventoStop = os.getenv('ID_EVENT_STOP')

voz = os.getenv('VOZ_OS')
username = os.getenv('USERNAME_PROYECT')
password = os.getenv('PASSWORD_PROYECT')

engine = pyttsx3.init()
engine.setProperty('voice', voz)
# engine.setProperty('voice', voices[1].id)

tags = []
eventsId = []

def getToken():
  try:
    url = baseUrl + '/auth/login'
    resp = requests.post(url,
                         json={
                           "username": username,
                           "password": password
                         })
  except:
    print("Something went wrong")
    return "None"
  return resp.headers.get('Authorization').split(' ')[1]


def speak(audioResponse, tagResponse, patternCaptado):
  if (tagResponse == 'alimentos_sanos' or tagResponse == 'alimentos_no_sanos'):
    audioResponse = 'pertenece a la categoria de '+ patternCaptado +'. '+ audioResponse
  print("esta es la respuesta: ", audioResponse)
  engine.say(audioResponse)
  engine.runAndWait()
  stopMovementRobot()

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
    return query.lower()

def startMovementRobot(idEvento):
  try:
    url = baseUrl + '/send/' + idEvento
    resp = requests.post(url,
                         json={
                           "urlRobot": urlRobot,
                         }, headers={'Authorization': 'Bearer ' + token})
    print('response start movement: ', resp)
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
    if query == "hola "+robotName:
      result, tag, pattern = chatbot_response(query)
      idEvent = searchIdEventOfBiblioteca(tag)
      startMovementRobot(idEvent)
      speak(result, tag, pattern)
      while True:
        query = takeCommand().lower()
        result, tag, pattern = chatbot_response(query)
        if(tag=='despedida' ):
          idEvent = searchIdEventOfBiblioteca(tag)
          startMovementRobot(idEvent)
          speak(result, tag, pattern)
          sys.exit(0)
        else:
          idEvent = searchIdEventOfBiblioteca(tag)
          startMovementRobot(idEvent)
          speak(result, tag, pattern)


