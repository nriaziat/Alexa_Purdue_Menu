from flask import Flask
from flask_ask import Ask, statement, session, question

app = Flask(__name__)
ask = Ask(app, '/')

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
    URL = baseURL + courtsURL(court)
    html = sess.get(URL)

    return statement('%s is serving %s for %s', %(court, serving, meal))

if __name__ == '__main__':
    app.run()
