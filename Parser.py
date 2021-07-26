import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Parser:
    """Here is Parser!"""
    #__slots__ = []
    def __init__(self):
        self.__plots=[]
        pass

    def addPlot(self):
        self.__plots.append([[],[],[]])

    def configPlot(self,num,list_x, list_y, list_z):
        if num < len(self.plots):
            self.plots[num][0] = list_x
            self.plots[num][1] = list_y
            self.plots[num][2] = list_z


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

    def writeInFile(fileName, *args):
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

    def plot(self, list_x, list_y, list_z, x_name, y_name, z_name, z_step, z_lim, cmap = 'viridis'):
        """Plot"""
        new_x = sorted(list_x)

        y_len = 0
        while new_x[0] == new_x[y_len]:
            y_len += 1

        x_len = int(len(list_x) / y_len)

        Z = np.zeros((x_len, y_len))
        for i in range(x_len):
            for j in range(y_len):
                Z[i][j] = list_z[i * y_len + j]

        X = np.arange(0, y_len, 1)
        Y = np.arange(0, x_len, 1)
        X, Y = np.meshgrid(X, Y)

        fig = plt.figure()
        ax = Axes3D(fig, auto_add_to_figure=False, box_aspect=(1, 1 * (x_len / y_len), z_step))
        fig.add_axes(ax)

        ploT = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cmap, antialiased=True)

        ax.set(xlim=[0, y_len], ylim=[0, x_len], zlim=[0, z_lim])

        ax.set_xlabel(x_name, labelpad=20)
        ax.set_ylabel(y_name)
        ax.set_zlabel(z_name)

        fig.colorbar(ploT, shrink=0.3, aspect=5)

        plt.show()
        pass

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

    def __del__(self):
        pass

def main():
    pars = Parser()

    lists = pars.readFromTxtFile("Novosibirsk_storeys_HD (copy).txt",0,1,2)
    pars.plot(lists[0],lists[1],lists[2],"Lon","lan","storey",1,200)

if __name__ == '__main__':
    main()