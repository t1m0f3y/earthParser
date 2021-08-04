import json
import random

import numpy as np
import matplotlib.pyplot as plt
import math
import re
import time
#import concurrent.futures
import threading
from mpl_toolkits.mplot3d import Axes3D

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Parser:
    """Here is Parser!"""
# -------------------------PLOT----------------------------------#
    __slots__ = ['__plots', '__borders', '__pointer', '__step', '__threadsCount']
    def __init__(self):
        self.__plots = {}
        self.__borders = []
        self.__pointer = [0.0, 0.0]
        self.__step = 1
        self.__threadsCount = 1

    def addPlot(self,name):
        self.__plots[name] = {
            "axis":{
            "x":{"name":"X","value":0},
            "y":{"name":"Y","value":0},
            "z":{"name":"Z","value":0, "step":1, "limit":200}
        }}

    def getPlotsName(self):
        return self.__plots.keys()

    def delPlot(self,name):
        del(self.__plots[name])

    def getPlotSettings(self,num):
        return self.__plots[num]

    def configPlot(self, num, plot):
        self.__plots[num] = plot

    def setBorders(self,borders):
        self.__borders = borders

    def getBorders(self):
        return self.__borders

    def readFromTxtFile(self,fileName, *args):
        """Read .txt file's columns and convert they to one list of lists"""
        f = open(fileName, 'r')
        if f:
            data = f.readlines()

            lists=[[]for i in args]
            for n in args:
                for line in range(0, len(data)):
                    lists[args.index(n)].append(data[line].split()[n])
        return (lists)

    def writeInFile(self, fileName, *args):
        """Write lists in .txt file"""
        f = open(fileName, 'w')
        length = len(args[0])
        for i in range(length):
            line = ''
            for n in args:
                line += str(n[i]) + ' '
            line += '\n'
            f.write(line)
        f.close()

    def writeInFileCpp(self, fileName, List):
        """Write lists in .txt file"""
        f = open(fileName, 'w')
        length = len(List[0])
        oneLength = len(List)
        string=''
        string += 'const float storeysHeights[' + str(length) + ']' + '[' + str(oneLength) + ']' + '={\n'
        for i in range(length):
            string += '{'
            for n in range(oneLength):
                string += str(List[n][i])
                if(n!=oneLength-1):
                    string+=','

            string+='}'
            if (i != length - 1):
                string+=','
            string+='\n'
        string+='};'
        f.write(string)
        f.close()


    def __checkCells(self, lon, lat, i, j, checkI, checkJ):
        if (checkI + i) < 0:
            checkI = 0
        else:
            if (checkI + i) >= lon:
                checkI = 0

        if (checkJ + j) < 0:
            checkJ = 0
        else:
            if (checkJ + j) >= lat:
                checkJ = 0

        return (checkI, checkJ)

    def plot(self, list):
        """Plot"""
        for name in list:
            new_x = sorted(self.__plots[name]["axis"]["x"]["value"])
            y_len = 0
            while new_x[0] == new_x[y_len]:
                y_len += 1

            x_len = int(len(self.__plots[name]["axis"]["x"]["value"]) / y_len)
            print(x_len)
            print(y_len)
            Z = np.zeros((x_len, y_len))
            for i in range(x_len):
                for j in range(y_len):
                    Z[i][j] = self.__plots[name]["axis"]["z"]["value"][i * y_len + j]

            #Z2 = np.kron(Z,np.ones((2,2)))

            X = np.arange(0, y_len, 1)
            Y = np.arange(0, x_len, 1)
            X, Y = np.meshgrid(X, Y)

            '''
            scaledHeight=[0 for i in range(x_len*y_len*4)]
            scaledX = [0 for i in range(x_len*y_len*4)]
            scaledY = [0 for i in range(x_len * y_len * 4)]
            print(len(scaledHeight))

            print(len(scaledX))
            print(len(scaledY))
            print(len(scaledHeight))
            '''

            #self.writeInFile("nskStoreysHeightsScaled.txt",scaledX,scaledY,scaledHeight)

            fig = plt.figure()

            ax = Axes3D(fig, auto_add_to_figure=False, box_aspect=(1, 1 * (x_len / y_len), self.__plots[name]["axis"]["z"]["step"]),title=name)
            fig.add_axes(ax)

            ploT = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', antialiased=False)

            ax.set(xlim=[0, y_len], ylim=[0, x_len], zlim=[0, self.__plots[name]["axis"]["z"]["limit"]])

            ax.set_xlabel(self.__plots[name]["axis"]["x"]["name"], labelpad=20)
            ax.set_ylabel(self.__plots[name]["axis"]["y"]["name"])
            ax.set_zlabel(self.__plots[name]["axis"]["z"]["name"])

            fig.colorbar(ploT, shrink=0.3, aspect=5)

        plt.show()

    def scale(self, List, scale):
        newX = sorted(List[0])

        yLen = 0
        while newX[0] == newX[yLen]:
            yLen += 1

        xLen = int(len(List[0]) / yLen)

        scaledYLen = yLen * scale
        scaledXLen = xLen * scale

        scaledX = [0 for i in range(scaledXLen * scaledYLen)]
        scaledY = [0 for i in range(scaledXLen * scaledYLen)]


        print(scaledXLen)
        print(scaledYLen)

        i = 0
        for scaledI in range(0, len(scaledX), scale ** 3):
            for a in range(0, 3, 2):
                for step1 in range(0, scale ** 3, scale ** 2):
                    for step2 in range(0, scale, 1):
                        scaledY[scaledI + step1 + step2 + a] = List[1][i + int(a / 2)]
                        scaledX[scaledI + step1 + step2 + a] = List[0][i + int(a / 2)]
            i += 2

        newList=[]
        newList.append(scaledX)
        newList.append(scaledY)
        for num in range(2,len(List),1):

            scaledZ = [0 for i in range(scaledXLen * scaledYLen)]

            Z = np.zeros((xLen, yLen))
            for i in range(xLen):
                for j in range(yLen):
                    Z[i][j] = List[num][i * yLen + j]

            Z2 = np.kron(Z,np.ones((2,2)))

            for i in range(scaledXLen):
                for j in range(scaledYLen):
                    scaledZ[i*scaledYLen+j] = Z2[i][j]
            newList.append(scaledZ)


        self.writeInFileCpp('scaleTest.cpp',newList)


    def getBuildingsBoundaries(self, lat, lon, storey):
        latC = 0
        while lat[0] == lat[latC]:
            latC += 1

        lonC = int(len(lon) / latC)

        map = [[0 for j in range(latC)] for i in range(lonC)]

        Z = np.zeros((lonC, latC))

        for i in range(lonC):
            for j in range(latC):
                map[i][j] = int(storey[i * latC + j])

        buildingID = 2
        for i in range(0, lonC, 1):
            for j in range(0, latC, 1):
                if map[i][j] == 0:
                    Z[i][j] = 1

        for i in range(0, lonC, 1):
            for j in range(0, latC, 1):
                if Z[i][j] == 0:
                    self.__check(i, j, i, j, map, Z, lonC, latC, buildingID)
                    buildingID += 1

        buildings = [0 for i in range(len(lat))]

        for i in range(lonC):
            for j in range(latC):
                buildings[i * latC + j] = int(Z[i][j])

        return (buildings)

    def __check(self, origin_i, origin_j, i, j, map, mapA, lonC, latC, bulID):
        for check_i in range(-1, 2):
            for check_j in range(-1, 2):
                check_i, check_j = self.__checkCells(lonC, latC, i, j, check_i, check_j)
                if i == check_i and j == check_j:
                    continue
                if map[origin_i][origin_j] == map[i + check_i][j + check_j]:
                    if mapA[i + check_i][j + check_j] == 0:
                        mapA[i + check_i][j + check_j] = bulID
                        self.__check(origin_i, origin_j, i + check_i, j + check_j, map, mapA, lonC, latC, bulID)
                    else:
                        continue
                else:
                    continue

# -------------------------PARSER----------------------------------#
    def parse(self, filename):
        minLat = self.__borders[0]
        minLon = self.__borders[1]
        maxLat = self.__borders[2]
        maxLon = self.__borders[3]

        self.__pointer[1] = minLon
        self.__pointer[0] = minLat

        driver = webdriver.Firefox(executable_path="/opt/WebDriver/bin/geckodriver")

        latStep = self.__step / 111000  # [degrees]
        lonStep = self.__step / (111300 * math.cos(math.radians(self.__pointer[0])))  # [degrees]

        count = 0
        while self.__pointer[1] <= maxLon and self.__pointer[0] <= maxLat:
            url = 'https://2gis.ru/novosibirsk/geo/' + str(self.__pointer[1]) + '%2C' + str(self.__pointer[0]) + "?m=" + str(
                self.__pointer[1]) + '%2C' + str(self.__pointer[0]) + "%2F16"
            try:
                driver.get(url)
                time.sleep(1)
                element = driver.find_element_by_xpath(
                    "/html/body/div/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div/div/div/div[1]/div/div[2]")

                height = re.findall("\d{1,2} этаж\w*", element.text)
            except:
                try:
                    driver.close()
                except:
                    pass
                driver = webdriver.Firefox(executable_path="/opt/WebDriver/bin/geckodriver")
                continue

            if height:
                if len(height) == 1:
                    height = height.pop(0)
                else:
                    height = height.pop(len(height) - 1)

                test = str(height).find("'")
                text = str(height)[test + 1:test + 3]
            else:
                text = "0"

            self.__writeIntoFile(filename, self.__pointer[0], self.__pointer[1], text)

            self.__pointer[1] += lonStep
            if self.__pointer[1] > maxLon:
                self.__pointer[1] = minLon
                self.__pointer[0] += latStep
                lonStep = self.__step / (111300 * math.cos(math.radians(self.__pointer[0])))

        driver.close()

    def parseThreading(self, filename):
        minLat = self.__borders[0]
        minLon = self.__borders[1]
        maxLat = self.__borders[2]
        maxLon = self.__borders[3]

        self.__pointer[1] = minLon
        self.__pointer[0] = minLat

        #driver = webdriver.Firefox(executable_path="/opt/WebDriver/bin/geckodriver")

        latStep = self.__step / 111000  # [degrees]
        lonStep = self.__step / (111300 * math.cos(math.radians(self.__pointer[0])))  # [degrees]
        map=[]
        latList=[]
        lonList = []
        while self.__pointer[1] <= maxLon and self.__pointer[0] <= maxLat:
            lonList.append(self.__pointer[1])
            self.__pointer[1] += lonStep
            if self.__pointer[1] > maxLon:
                self.__pointer[1] = minLon
                latList.append(self.__pointer[0])
                self.__pointer[0] += latStep
                map.append(lonList[:])
                lonList.clear()
                lonStep = self.__step / (111300 * math.cos(math.radians(self.__pointer[0])))

        threads = []
        for start in range(self.__threadsCount):
            t = threading.Thread(target=self.__run,args=[latList,map,start, filename])
            t.start()

        for thread in threads:
            thread.join()

    def __run(self, mapLat, map, start, filename):
        #time.sleep(random.randint(0, 3))
        driver = webdriver.Firefox(executable_path="/opt/WebDriver/bin/geckodriver")
        for i in range(start,len(map),self.__threadsCount):
            for j in range(len(map[i])):
                #time.sleep(1)
                lon=map[i][j]
                lat=mapLat[i]
                url = 'view-source:https://2gis.ru/novosibirsk/geo/' + str(lon) + '%2C' + str(lat) + "?m=" + str(lon) + '%2C' + str(lat) + "%2F16"
                try:
                    driver.get(url)
                    #time.sleep(1)
                    element = driver.find_element_by_xpath("/html/body")                           #/div/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div/div/div/div[1]/div/div[2]")

                    height = re.findall("\d{1,2} этаж\w*", element.text)#element.text)
                except:
                    try:
                        driver.close()
                    except:
                        pass
                    driver = webdriver.Firefox(executable_path="/opt/WebDriver/bin/geckodriver")
                    #i-=1
                    j-=1
                    continue
                #print(height)
                #print(element.text)
                if height:
                    if len(height) == 1:
                        height = height.pop(0)
                    else:
                        height = height.pop(1)

                    test = str(height).find("'")
                    text = str(height)[test + 1:test + 3]
                else:
                    text = "0"

                self.__writeIntoFile(filename, lat, lon , text)

    def __writeIntoFile(self, filename, lon, lat, data):
        f = open(filename, 'a')
        f.write(str(lon) + ' ' + str(lat) + ' ' + str(data) + '\n')

    def __del__(self):
        pass

def main():
    parser = Parser()
    #parser.setBorders([55.0092411711711, 82.933401, 55.018151, 82.960240])
    #parser.parseThreading('Novosibirsk_storeys_HD_ThreadingFin.txt')

    parser.addPlot('plot1')
    settings = parser.getPlotSettings('plot1')

    args = parser.readFromTxtFile('Novosibirsk_storeys_heights.txt',0,1,2,3,4)

    #settings['axis']['x']['value'] = args[0][:]
    #settings['axis']['y']['value'] = args[1][:]
    #settings['axis']['z']['value'] = args[2][:]

    parser.scale(args,2)
    #parser.plot(['plot1'])

if __name__ == '__main__':
    main()