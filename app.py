from BeautifulSoup import BeautifulSoup as bs
from flask import Flask
from flask_ask import Ask, statement, session, question
import urlparse
from urllib2 import urlopen
from urllib import urlretrieve
import os
import sys

app = Flask(__name__)
ask = Ask(app, '/')
sess = requests.Session()

baseURL = "http://www.housing.purdue.edu/Menus/"
courtsURL = {"Earhart": "ERHT", "Ford": "FORD", "Hillenbrand":"HILL", "Wiley":"WILY", "Windosor":"WIND"}
mealNum = {"Earhart": 3, "Ford": 4, "Hillenbrand":3, "Wiley":3, "Windosor":4}

mealQuestion = "What meal do you want to know about?"

@ask.launch
def start_skill():
    welcome_message = 'Hello, what dining court would you like to know about?'
    return question(welcome_message)

@ask.intent("GET_MEAL", mapping={'court': 'Court'}, mapping={'meal': 'Meal'})
def function(court, meal):
    numMeals = mealNum(court)
    url = baseURL + courtsURL(court)
    soup = bs(urlopen(url))
    parsed = list(urlparse.urlparse(url))
    
    return statement('%s is serving %s for %s', %(court, serving, meal))

if __name__ == '__main__':
    app.run()
