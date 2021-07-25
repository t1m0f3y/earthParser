import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Parser:
    """Here is Parser!"""
    #__slots__ = []
    def __init__(self):
        pass

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

    def __check_cells(self, lon, lat, i, j, checkI, checkJ):
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

    def plot(self, filename, x, y, z, x_name, y_name, z_name, z_lim):
        pass

    def __del__(self):
        pass

def main():
    pars = Parser()

if __name__ == '__main__':
    main()