"""
The script is parsing the https://votetovid.ru in order to get the surface elevation.
author: Ruslan V. Akhpashev
url: https://github.com/fzybot
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

# Start URL format
# 'center' value could not be changed in future, only 'point'
center = [55.0166, 82.9544] # Novosibirsk coordinates
comma = ','
zoom = '16z'
pointer = [55.018772, 82.954974]
i = "i"
trb = 'trb'
# url = 'https://votetovid.ru/#' + str(center[0]) + comma + str(center[1]) + comma + zoom + comma \
#       + str(pointer[0]) + comma + str(pointer[1]) + i + comma + trb

# rectangle borders around the 'center'
borders = [55.009069999999994, 82.933401, 55.018151, 82.960240]
minLon = borders[0]
minLat = borders[1]
maxLon = borders[2]
maxLat = borders[3]

step = 0.001 # around 60 meters

def writeIntoFileArray(filename, lon, lat, data):
    f = open(filename, 'a')
    for i in range(len(data)):
        f.write(str(lon) + ' ' + str(lat) + ' ' + str(data) + '\n')

def writeIntoFile(filename, lon, lat, data):
    f = open(filename, 'a')
    f.write(str(lon) + ' ' + str(lat) + ' ' + str(data) + '\n')

def main(minLon_, minLat_, maxLon_, maxLat_, step):
    driver = webdriver.Chrome(ChromeDriverManager(version="91.0.4472.19").install())
    url = 'https://2gis.ru/novosibirsk/firm/141265770822730/82.950159%2C55.012845?m=82.949953%2C55.012788%2F17.83%2Fr%2F-2.44'
    driver.get(url)
    time.sleep(1)
    html_ = driver.page_source
    soup = BeautifulSoup(html_, 'lxml')
    print( soup )
    #print(soup.find_all('script')[13])
    #writeIntoFile('Novosibirsk_storeys.txt', pointer[0], pointer[1], height)


if __name__ == '__main__':
    main(minLon, minLat, maxLon, maxLat, step)


