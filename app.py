from bs4 import BeautifulSoup as bs
from flask import Flask
from flask_ask import Ask, statement, session, question
import datetime
import urllib2
import urllib
import re
import requests
import json

now = datetime.datetime.now()

year = now.year
month = now.month
day = now.day
hour = now.hour
minutes = now.minute

app = Flask(__name__)
ask = Ask(app, '/')

mealDict = {}
timesDict = {}
mealsList = []

def getMeals(url):
    response = urllib2.urlopen(url)
    inputJson = response.read()
    response.close()
    data = json.loads(inputJson)

    for l in data["Meals"]:
        try:
            l["Status"] != 'Closed'
        except:
            mealsList.append(l["Name"])
            mealDict[l["Name"]] = {}
            timesDict[l["Name"]] = [l["Hours"]["StartTime"], l["Hours"]["EndTime"]]
            for i in l["Stations"]:
                #print ("\n")
                #print ("%s\n" %i["Name"])
                mealDict[l["Name"]][i["Name"]] = []
                for j in i["Items"]:
                    mealDict[l["Name"]][i["Name"]].append(j["Name"])
                    #print j["Name"]

    return [mealDict,timesDict]

def time_in_range(start, end, x):
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

def currMeal():
    for item in mealsList:
        start = timesDict[item][0]
        start = datetime.datetime.strptime(start, '%H:%M:%S').time()

        end = timesDict[item][1]
        end = datetime.datetime.strptime(end, '%H:%M:%S').time()

        if time_in_range(start, end, now.time()):
            return item
    return 0

def makeURL(court):
    baseURL = "https://api.hfs.purdue.edu/menus/v2/locations/"
    url = baseURL + court + "/{:0>2}-{:0>2}-{:0>4}".format(month, day, year)
    return url

def whatsToEat(court):
    foods = []
    url = makeURL(court)
    try:
        getMeals(url)
    except urllib2.HTTPError:
        return 0
    else:
        meal = currMeal()
        if meal == 0:
            return 0
        for item in mealDict[meal]:
            for food in mealDict[meal][item]:
                foods.append(food)
        return foods

@ask.launch
def getCourt():
    welcome_message = "What dining court do you want to know about?"
    return question(welcome_message)

@ask.intent("GET_MEAL", mapping={'court': 'Court'})
def eats(court):
    foods = whatsToEat(court)

    if foods == 0:
        return statement(format("Dining court %s closed or not found.", (court)))

    else:
        return statement(format("Heres whats being served at %s: %s", (court, ",".join(foods))))

@ask.intent("IS_OPEN", mapping = {'court': 'Court'})
def isOpen(court):
    foods = whatsToEat(court)

    if foods == 0:
        return statement(format("Dining court %s closed or not found.", court))
    else:
        return statement(format("Yes! %s is open right now until %s", (court, timesDict[item][1])))

if __name__ == '__main__':
    app.run()
