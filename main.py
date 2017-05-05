# Author : Alexandre Dossin

import graph, simplePaths, input, display
import time

def main():

    numberOfCustomers = 15
    numberOfDepots = 2
    maxDistance = 1000  # in meters
    if numberOfCustomers >= 1 and numberOfDepots >= 2:
        g = graph.buildGraph(numberOfCustomers, numberOfDepots, maxDistance)  # for testing
    else:
        raise ValueError("The network must have at least 1 customer and 2 depots.")
    #print(g)
    simplePathsTest = simplePaths.exploreSimplePaths(g, 0, 17)
    print([[node.getName() for node in trip] for trip in simplePathsTest])
    print(len(simplePathsTest))
    #filteredSimplePaths = simplePaths.filterSimplePaths(g, simplePathsTest, droneSpeed=600)
    #print([[node.getName() for node in path] for path in filteredSimplePaths])
    #allSimplePaths = simplePaths.exploreAllSimplePaths(g, printStatistics=True)
    #print([[node.getName() for node in trip] for trip in allSimplePaths])
    simplePathsTest = simplePaths.exploreSimplePathsNonRecursive(g, 0, 17)
    print(len(simplePathsTest))
    print([[node.getName() for node in trip] for trip in simplePathsTest])


    """input.createInputFile(g, "clients.txt")
    fileName = "input0.txt"
    timeIntervals = [[0, 86400]] * numberOfDepots  # for the moment the time windows are not restrictive
    fixedCost = 10000  # if high value, the problem is the minimization of the number of vehicles
    input.createCompleteGENCOLInputFile(fileName, g, fixedCost, timeIntervals,
                                  droneSpeed=600, droneAutonomy=25, printStatistics=True)"""

    displayBool = False
    if displayBool:
        root = display.Tk()
        wdw = display.Window(root, g, "sol.txt")
        root.geometry("800x600+300+100")
        root.mainloop()


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("\n Time used for main function : --- %s seconds ---" % (time.time() - start_time))