from bs4 import BeautifulSoup as bs
from contextlib import closing
from selenium.webdriver import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from flask import Flask
from flask_ask import Ask, statement, session, question

app = Flask(__name__)
ask = Ask(app, '/')
sess = requests.Session()
driver = webdriver.PhantomJS()
baseURL = "http://www.housing.purdue.edu/Menus/"
courtsURL = {"Earhart": "ERHT", "Ford": "FORD", "Hillenbrand":"HILL", "Wiley":"WILY", "Windosor":"WIND"}
mealNum = {"Earhart": 3, "Ford": 4, "Hillenbrand":3, "Wiley":3, "Windosor":4}

mealQuestion = "What meal do you want to know about?"

def getMeals(url):
    # use firefox to get page with javascript generated content
    with closing(webdriver.PhantomJS()) as browser:
        browser.get(url)

         # wait for the page to load
        WebDriverWait(browser, timeout=10).until(lambda x: x.find_element_by_class_name('station-item-text'))
         # store it to string variable
        page_source = browser.page_source

    page_source = (page_source.encode("utf-8"))

    mealDict = {}
    stationList = []

    soup = bs(page_source, "html5lib")

    for node in soup.findAll("span", {'class': 'station-item-text'}):
        meal = (''.join(node.findAll(text=True))).encode("utf-8")
        #print meal
        station =  node.parent.parent.parent.parent.find('div', {'class': 'station-name'}).text
        station = station.encode("utf-8")
        #print station
        stationList.append(station)

        try:
            mealDict[station]
        except KeyError:
            mealDict[station] = [meal]
        else:
            mealDict[station].append(meal)

    #print mealDict
    return mealDict

@ask.launch
def start_skill():
    welcome_message = 'Hello, what dining court would you like to know about?'
    return question(welcome_message)

@ask.intent("GET_MEAL", mapping={'court': 'Court'})
def function(court):

    url = baseURL + courtsURL(court)
    mealDict = getMeals(url)
    stationList = mealDict[1]
    mealDict = mealDict[0]

    return statement('%s is serving %s for %s', %(court, serving, meal))

if __name__ == '__main__':
    app.run()
