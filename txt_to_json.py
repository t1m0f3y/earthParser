import copy
import ctypes.wintypes
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


def read_from_file(fileName):
    f = open(fileName,'r')

    if f:
        data = f.readlines()


    lat = []
    lon = []
    storey = []


    for i in range(0,len(data)):
        lat.append(data[i].split()[0])
        lon.append(data[i].split()[1])
        storey.append(data[i].split()[2])

    return (lat,lon,storey)

def check_cells(lon, lat, i, j, check_i, check_j):
    if (check_i+i) < 0 or (check_i+i) >= lon or (check_j+j) < 0 or (check_j+j) >= lat:
        return(0,0)

    return(check_i,check_j)


def main():
    lat,lon,storey = read_from_file('Novosibirsk_storeys.txt')

    x=lat[0]

    latC = 0
    while lat[0] == lat[latC]:
        latC += 1

    j=0
    i=0

    lonC = int(len(lon)/latC)

    map = [[0 for j in range(latC)] for i in range(lonC)]

    print(len(storey))

    #mapA = copy.deepcopy(map)

    Z = np.zeros((latC,lonC))

    for i in range(lonC):
        for j in range(latC):
            map[i][j]=storey[i*latC+j]
            Z[j][i]=storey[i*latC+j]


    X = np.arange(0, lonC, 1)
    Y = np.arange(0, latC, 1)
    X, Y = np.meshgrid(X, Y)

    fig = plt.figure()
    ax = Axes3D(fig,auto_add_to_figure=False, box_aspect=(1*(lonC/latC),1,0.1))

    fig.add_axes(ax)

    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.viridis, antialiased=False, edgecolor ='none',linewidth=20)
    ax.set(xlim=[0,lonC],ylim=[0,latC], zlim = [0,200])

    ax.set_xlabel("LAT")
    ax.set_ylabel("LON",labelpad=20)
    ax.set_zlabel("STOREY")

    plt.show()


#test1
"""
    # setup the figure and axes
    fig = plt.figure()
    ax = Axes3D(fig,auto_add_to_figure=False)
    fig.add_axes(ax)

    # fake data
    X = np.arange(0, lonC, 1)
    Y = np.arange(0, latC, 1)
    X, Y = np.meshgrid(X, Y)

    width = depth = 1

    ax.bar3d(X, Y, Z, width, depth, top, shade=True)
    ax.set_title('Shaded')
    plt.show()

"""

#test2
"""
    buildingID=1

    stop=False

    while not stop:
        stop=True
        for i in range(0,lonC):
            for j in range(0,latC):
                for check_i in range(-1,2):
                    for check_j in range(-1,2):
                        check_i , check_j = check_cells(lonC,latC,i,j,check_i,check_j)
                        if map[i][j]==map[i+check_i][j+check_j] and mapA[i][j]==0 and map[i][j] is not map[i+check_i][j+check_j]:
                            mapA[i][j]=buildingID

                        if mapA[i][j] == 0:
                            stop = False
                            buildingID += 1

        for i in range(lonC):
            print(mapA[i])
        print("--------------------------------------------")

                    #print("i = " + str(i))
                    #print("j = " + str(j))
                    #print("buildingID = " + str(buildingID))

    for i in range(lonC):
        print(mapA[i])

    print("-----")
    for i in range(lonC):
        print(map[i])
"""


if __name__ == '__main__':
    main()