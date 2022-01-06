import requests
import csv
from requests.structures import CaseInsensitiveDict
baseUrl = 'http://lolymidiapi.espol.edu.ec/api/lolyapi/v1'
urlRobot= 'https://bfd1-200-126-19-106.ngrok.io'
token = ''

tags = []
eventsId = []
pathBiblioteca = './biblioteca.csv'

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


def startMovementRobot(idEvento):
  try:
    url = baseUrl + '/send/' + idEvento
    resp = requests.post(url,
                         json={
                           "urlRobot": urlRobot,
                         }, headers={'Authorization': 'Bearer ' + token})
  except:
    print("Something went wrong")


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
  fillInformationfromBiblioteca(pathBiblioteca)
  print('tags: ', tags)
  print('idEvents: ', eventsId)
  idevent = searchIdEventOfBiblioteca('despedida')
  print('el id de saludo es:', idevent)
  token = getToken()
  startMovementRobot('28')
  # print(token)
