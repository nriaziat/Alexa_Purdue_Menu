from bs4 import BeautifulSoup as bs
from contextlib import closing
from flask import Flask
from flask_ask import Ask, statement, session, question
import datetime
import urllib2
from urllib import urlencode
import json

now = datetime.datetime.now()

year = now.year
month = now.month
day = now.day
hour = now.hour
minutes = now.minute

app = Flask(__name__)
ask = Ask(app, '/')


baseURL = "https://api.hfs.purdue.edu/menus/v2/locations/"
courtsURL = {"Earhart": "ERHT", "Ford": "FORD", "Hillenbrand":"HILL", "Wiley":"WILY", "Windosor":"WIND"}
mealNum = {"Earhart": 3, "Ford": 4, "Hillenbrand":3, "Wiley":3, "Windosor":4}

url = baseURL + 'Wiley' + "/{:0>2}-{:0>2}-{:0>4}".format(month, day, year)


mealQuestion = "What meal do you want to know about?"

def getMeals(url):
    response = urllib2.urlopen(url)
    inputJson = response.read()
    response.close()
    data = json.loads(inputJson, "ascii")
    for l in data["Meals"]:
        for i in l["Stations"]:
            print ("\n")
            print ("%s\n" %i["Name"])
            for j in i["Items"]:
                print j["Name"]

"""@ask.launch
def start_skill():
    welcome_message = 'Hello, what dining court would you like to know about?'
    return question(welcome_message)

@ask.intent("GET_MEAL", mapping={'court': 'Court'})
def function(court):

    url = baseURL + courtsURL(court) + "/%02d-%02d-%04d".format(month, day, year)
    mealDict = getMeals(url)
    stationList = mealDict[1]
    mealDict = mealDict[0]

    return statement('%s is serving %s for %s', %(court, serving, meal))

if __name__ == '__main__':
    app.run()

"""

getMeals(url)
