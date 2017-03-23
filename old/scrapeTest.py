from bs4 import BeautifulSoup as bs
from contextlib import closing
from selenium import webdriver # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Firefox

url = "https://dining.purdue.edu/menus/Earhart/"

driver = webdriver.PhantomJS()
driver.set_window_size(1120, 550)

def getMeals(url):
    # use firefox to get page with javascript generated content
    with closing(webdriver.PhantomJS()) as browser:
        browser.get(url)

         # wait for the page to load
        WebDriverWait(browser, timeout=10).until(lambda x: x.find_element_by_class_name('station-item-text'))
         # store it to string variable
        page_source = browser.page_source

    page_source = (page_source.encode("utf-8"))

    with open('file.html', 'w') as file:
        file.write(page_source)

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

    print mealDict
    return mealDict

getMeals(url)
