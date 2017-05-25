# Author : Alexandre Dossin

import graph, simplePaths, inputWithLegs, inputWithoutLegs, display
import time

def main():

    numberOfCustomers = 10
    numberOfDepots = 2
    maxDistance = 1000  # in meters
    if numberOfCustomers >= 1 and numberOfDepots >= 2:
        g = graph.buildGraph(numberOfCustomers, numberOfDepots, maxDistance)  # for testing
    else:
        raise ValueError("The network must have at least 1 customer and 2 depots.")

    #print(g)
    #allSimplePathsNonRecursive = simplePaths.exploreAllSimplePaths(g, recursiveAlgorithm=False, printStatistics=True)
    #allSimplePathsRecursive = simplePaths.exploreAllSimplePaths(g, recursiveAlgorithm=True, printStatistics=True)
    #print([[node.getName() for node in trip] for trip in allSimplePathsRecursive])
    #print([[node.getName() for node in trip] for trip in allSimplePathsNonRecursive])

    timeWindows = simplePaths.buildTimeWindows(numberOfDepots, tightTW=True)
    generateInputFileWithLegs = True
    #timeWindows = [[0, 86400]] * numberOfDepots  # for the moment the time windows are not restrictive
    fixedCost = 10000  # if high value, the problem is the minimization of the number of vehicles
    if generateInputFileWithLegs:
        fileName = "input{}_{}_{}.txt".format(numberOfCustomers, numberOfDepots, "tight5")
        # input.createInputFile(g, "clients.txt", recursiveAlgorithm=False, printStatistics=False)
        inputWithLegs.createCompleteGENCOLInputFile(fileName, g, fixedCost, timeWindows,
                                            droneSpeed=600, droneAutonomy=25, recursiveAlgorithm=False, printStatistics=True)
    else:
        fileName = "input{}_{}_{}_p.txt".format(numberOfCustomers, numberOfDepots, "tight5")
        inputWithoutLegs.createCompleteGENCOLInputFile(fileName, g, fixedCost, timeWindows, serviceTime=5,
                                                       droneSpeed=600, droneAutonomy=25)

    displayRoutes = False
    if displayRoutes:
        root = display.Tk()
        wdw = display.Window(root, g, "sol.txt")
        root.geometry("800x600+300+100")
        root.mainloop()


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("\n Time used for main function : --- %s seconds ---" % (time.time() - start_time))