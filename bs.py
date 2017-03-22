from bs4 import BeautifulSoup as bs

mealDict = {}
stationList = []

with open("Menus - Purdue University.html", 'r') as file:
    soup = bs(file, "html5lib")

for node in soup.findAll("span", {'class': 'station-item-text'}):
    meal = (''.join(node.findAll(text=True))).encode("utf-8")

    station =  node.parent.parent.parent.parent.find('div', {'class': 'station-name'}).text
    station = station.encode("utf-8")
    stationList.append(station)

    try:
        mealDict[station]
    except KeyError:
        mealDict[station] = [meal]
    else:
        mealDict[station].append(meal)

print mealDict
