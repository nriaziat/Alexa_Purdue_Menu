from contextlib import closing
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
url = "https://dining.purdue.edu/menus/Earhart/"
# use firefox to get page with javascript generated content
with closing(Firefox()) as browser:
     browser.get(url)
     # wait for the page to load
     WebDriverWait(browser, timeout=10).until(
         lambda x: x.find_element_by_id('location-tab-empty'))
     # store it to string variable
     page_source = browser.page_source

with open("file.html", 'w') as file:
    file.write(page_source.encode("utf-8"))
