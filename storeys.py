"""
The script is parsing the https://2gis.ru in order to find out the number of storeys
author: Ruslan V. Akhpashev, Timofey M. Leonenko
url: https://github.com/fzybot
"""

from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import re
import random
import math
import cmath

#from bs4 import BeautifulSoup

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
#borders = [55.009069999999994, 82.933401, 55.018151, 82.960240] - goal

borders = [55.015798, 82.940781, 55.016179, 82.94556]
minLon = borders[0]
minLat = borders[1]
maxLon = borders[2]
maxLat = borders[3]

#step = 0.0001 # around 60 meters
step = 0.0003

def writeIntoFileArray(filename, lon, lat, data):
    f = open(filename, 'a')
    for i in range(len(data)):
        f.write(str(lon) + ' ' + str(lat) + ' ' + str(data) + '\n')

def writeIntoFile(filename, lon, lat, data):
    f = open(filename, 'a')
    f.write(str(lon) + ' ' + str(lat) + ' ' + str(data) + '\n')

def main(minLon_, minLat_, maxLon_, maxLat_, step):
    driver = webdriver.Firefox(executable_path="/opt/WebDriver/bin/geckodriver")


    #url = 'https://2gis.ru/novosibirsk/firm/70000001050285238/82.924014%2C55.047909?m=82.924357%2C55.044725%2F16'

    print("number of steps Lon: ", round((maxLon_ - minLon_) / step))
    print("number of steps Lan: ", round((maxLat_ - minLat_) / step))

    print(6371000 * (math.cos(minLon) + math.sin(minLat)))

    print(6371000 * (math.cos(maxLon) + math.sin(maxLat)))



"""
    while pointer[0] <= maxLon and pointer[1] <= maxLat:
        url = 'https://2gis.ru/novosibirsk/geo/' + str(pointer[1]) + '%2C' + str(pointer[0]) + "?m=" + str(pointer[1]) + '%2C' + str(pointer[0]) + "%2F16"
        driver.get(url)
        time.sleep(random.randint(1, 5))
        element = driver.find_element_by_xpath("/html/body/div/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div/div/div/div[1]/div/div[2]/div[2]")
        if "NoSuchElementException" not in driver.page_source:
            height = re.search("\d{1,2} этаж\w*", element.text)
            if height:
                test = str(height).find("'")
                text = str(height)[test + 1:test + 3]
            else:
                text = "0"
        writeIntoFile('Novosibirsk_storeys.txt', pointer[0], pointer[1], text)

        pointer[1]+=step
        if(pointer[1] > maxLat):
            pointer[1]=minLat
            pointer[0]+=step

"""
"""
    while pointer[0] <= maxLon :
        while pointer[1] <= maxLat:
            url = 'https://2gis.ru/novosibirsk/geo/' + str(pointer[1]) + '%2C' + str(pointer[0]) + "?m=" + str(pointer[1]) + '%2C' + str(pointer[0]) + "%2F16"
            driver.get(url)
            time.sleep(random.randint(1, 5))
            element = driver.find_element_by_xpath("/html/body/div/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div/div/div/div[1]/div/div[2]/div[2]")
            if "NoSuchElementException" not in driver.page_source:
                height = re.search("\d{1,2} этаж\w*", element.text)
                if height:
                    test = str(height).find("'")
                    text = str(height)[test + 1:test + 3]
                else:
                    text = "0"
            writeIntoFile('Novosibirsk_storeys.txt', pointer[0], pointer[1], text)

            pointer[1]+=step
        pointer[0]+=step
        pointer[1]=minLat
"""
"""
    for k in range(round((maxLon_ - minLon_) / step)):
        pointer[1] = minLat_
        for j in range(round((maxLat_ - minLat_) / step)):
            pointer[1] += step
            url = 'https://2gis.ru/novosibirsk/geo/' + str(pointer[1]) + '%2C' + str(pointer[0]) + "?m=" + str(pointer[1]) + '%2C' + str(pointer[0]) + "%2F16"
            driver.get(url)
            time.sleep(random.randint(1, 5))
            element = driver.find_element_by_xpath("/html/body/div/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div/div/div/div[1]/div/div[2]/div[2]")
            if "NoSuchElementException" not in driver.page_source:
                height = re.search("\d{1,2} этаж\w*", element.text)
                if height:
                    test = str(height).find("'")
                    text = str(height)[test + 1:test + 3]
                else:
                    text = "0"
            writeIntoFile('Novosibirsk_storeys.txt', pointer[0], pointer[1], text)
        pointer[0] += step
"""
if __name__ == '__main__':
    main(minLon, minLat, maxLon, maxLat, step)


