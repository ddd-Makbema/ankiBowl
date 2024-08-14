import json
import urllib.request
import re

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

def addCard(question, answer):
    invoke('addNote', note = {"deckName":"ankiConnect", "modelName":"Basic", "fields":{"Front": question, "Back": answer}})

running = True

while running:
    answer = input("Input the answer or type exit: ")
    if answer == "exit":
        break
    questions = input("Input the full question: ")
    questions = questions.strip("For 10 points,")
    questions = questions.strip("for 10 points,")
    questions = re.split(r'[.;]', questions)
    
    print(questions[:-1])
    for question in questions[:-1]:
        addCard(question, answer)
