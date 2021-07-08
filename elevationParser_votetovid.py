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
borders = [54.932657999999925, 82.686262, 55.130431, 83.148554]
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
    pointer[0] = minLon_
    for k in range(round((maxLon_ - minLon_) / step)):
        pointer[0] += step
        pointer[1] = minLat_
        for j in range(round((maxLat_ - minLat_) / step)):
            pointer[1] += step
            url = 'https://votetovid.ru/#' + str(center[0]) + comma + str(center[1]) + comma + zoom + comma \
                  + str(pointer[0]) + comma + str(pointer[1]) + i + comma + trb
            driver.get(url)
            time.sleep(1)
            html_ = driver.page_source
            # for this part of the code you will need to install lxml module: pip install lxml
            soup = BeautifulSoup(html_, 'lxml')
            span_txHgt = soup.find_all('span')[0]
            print(pointer[0], pointer[1], span_txHgt.text)
            writeIntoFile('Novosibirsk.txt', pointer[0], pointer[1], span_txHgt.text)


if __name__ == '__main__':
    main(minLon, minLat, maxLon, maxLat, step)


