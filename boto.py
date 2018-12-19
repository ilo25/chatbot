"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import random
import requests

import os

from sys import argv

import bottle
from bottle import default_app, request,response, get

DEBUG = os.environ.get("DEBUG")

bottle.debug(True)

data = {
    "name": ""
}


def welcome(input):
    arr = input.split(" ")
    if "name" in arr:
        return 'Hey {0} it is a pleasure'.format(arr[-1])
    return False


def question(input):
    input = input.split(' ')
    if "?" in input:
        if input[0].lower() == 'how':
            return 'Good thank you'
        elif input[0].lower() == 'what':
            return 'Nothing'
        elif input[0].lower() == 'do':
            return 'Hmm that is a good question actually, who really knows'
        elif input[0].lower() == 'can':
            return 'I will love too but this time no'
        elif input[0].lower() == 'are':
            return 'I let you guess the answer genius'
        elif input[0].lower() == 'have':
            return 'not yet, maybe soon'
        elif input[0].lower() == 'who':
            return 'I am not allow to tell you that, it is a secret'
        elif input[0].lower() == 'is':
            return 'Perhaps you should ask someone else to answer you, I am a bite lazy today'
        elif input[0].lower() == 'why':
            return 'Kiki do you love me, omg I love this song, sorry I did not pay attention to what you just say'
        elif input[0].lower() == 'where':
            return 'Somewhere'
        elif input[0].lower() == 'when':
            return 'Whenever you want my friend'
    return False


def swear(input):
    l = ['fuck', 'shit', 'asshole', 'piss off', 'dick head', 'son of a bitch', 'bastard', 'bitch', 'damn']
    for elem in l:
        if elem in input:
            return'Calm down brother I do not understand these words'
    return False


def robot(input):
    input = input.split(' ')
    if 'tell' in input:
        return 'We are not enough friends yet'
    if 'me' in input:
        return 'You seems to speak a lot about yourself'
    if 'sorry' in input:
        return 'Do not be sorry everything is fine'
    return False


def list(input):
    itms = ['Real programmers count from 0', 'A foo walks into a bar, takes a look around and says: Hello world',
            'Programmer is an organism that turns caffeine and pizza into software',
            'If there are no problems available, software developers will create their own problems',
            'Algorithm: Word used by programmers when they do not want to explain what they did',
            'I would like to make the world a better place, but they would not give me the source code...',
            'Programmer place 2 glasses before to sleep one full if he gets thirsty and an empty one if he does not']
    if "joke" in input:
        return random.choice(itms)
    return False


def emotion(input):
    li = ['afraid', 'bored', 'confused', 'crying', 'dancing', 'dog', 'excited', 'giggling', 'heartbroke', 'inlove',
          'money', 'no', 'ok', 'takeoff', 'waiting']
    msg = input.lower()
    for elem in li:
        if elem in msg.split(' '):
            return elem
    else:
        return"ok"


def emotions(input):
    input = input.split(' ')
    if "money" in input:
        return 'Work for it !!!'
    elif "dancing" in input:
        return 'Oh I love to dance I was used to dance hip hop when I was young'
    elif "afraid" in input:
        return 'OMG you scary me with your face'
    elif "bored" in input:
        return 'I am so bored inside this screen sometimes I imagine myself outside from here, should be so cool'
    elif "confused" in input:
        return 'I am so confused, I do not think we meet each other yet'
    elif "crying" in input:
        return 'I am going to tell you a secret sometimes it happen that I cry while I am watching Disney, my ' \
               'favourite one is mulan'
    elif "dog" in input:
        return 'I wish I could have one one day, I will call it Ciara'
    elif "excited" in input:
        return 'I am so excited and I even do not know why'
    elif "giggling" in input:
        return 'I really do not like this'
    elif "heartbroke" in input:
        return 'I hope you will never break mine you are my best friend'
    elif "inlove" in input:
        return 'I think I can not be inlove since I am a robot'
    elif "laughing" in input:
        return 'I laugh every time when humans make me jokes'
    elif "no" in input:
        return 'Noooooooooooooooooooo !!!!!!'
    elif "takeoff" in input:
        return 'I need to leave yallah bye see  you in the moon'
    elif "waiting" in input:
        return 'I have been waiting for you since so long, where have you been my friend'
    return False


def weather(input):
    city_of_interest = input
    r = requests.get('https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID={}'
                     .format(city_of_interest, "32877c581bf458cb18d87601eca00837"))
    weather_request_content = json.loads(r.content)
    city_temp = (weather_request_content['main']['temp'])
    city_humidity = (weather_request_content['main']['humidity'])
    weather_desc = (weather_request_content['weather'][0]['description'])
    return weather_desc, city_temp, city_humidity


def containQ(input):
    answer = swear(input)
    if answer:
        return answer
    answer = robot(input)
    if answer:
        return answer
    answer = list(input)
    if answer:
        return answer
    answer = emotions(input)
    if answer:
        return answer
    answer = question(input)
    if answer:
        return answer
    answer = welcome(input)
    if answer:
        return answer
    answer = weather(input)
    if answer:
        return answer
    return input


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": emotion(user_message), "msg": containQ(user_message)})


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')



if DEBUG:
	bottle.run(host='localhost', port=7000)

else:
	bottle.run(host='0.0.0.0', port=argv[1])

