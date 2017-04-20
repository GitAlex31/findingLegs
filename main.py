# Author : Alexandre Dossin

import graph, simplePaths, input, display
import random, math


def main():
    
    numberOfCustomers = 5
    numberOfDepots = 2
    maxDistance = 1000  # in meters
    if numberOfCustomers >= 1 and numberOfDepots >= 2:
        g = graph.buildGraph(numberOfCustomers, numberOfDepots, maxDistance)  # for testing
    else:
        raise ValueError("The network must have at least 1 customer and 2 depots.")
    #print(g)
    #allSimplePaths = simplePaths.exploreAllSimplePaths(g)
    #print([[node.getName() for node in trip] for trip in allSimplePaths])
    input.createInputFile(g, "clients.txt")
    fileName = "input0.txt"
    timeIntervals = [[0, 1440]] * numberOfDepots
    fixedCost = 10000  # if high value, the problem is the minimization of the number of vehicles
    input.createCompleteGENCOLInputFile(fileName, g, fixedCost, timeIntervals,
                                  droneSpeed=600, droneAutonomy=25, printStatistics=False)

    displayBool = False
    if displayBool:
        root = display.Tk()
        wdw = display.Window(root, g)
        root.geometry("800x600+300+100")
        root.mainloop()


if __name__ == '__main__':
    main()