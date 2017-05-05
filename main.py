# Author : Alexandre Dossin

import graph, simplePaths, input, display
import time

def main():

    numberOfCustomers = 40
    numberOfDepots = 2
    maxDistance = 1000  # in meters
    if numberOfCustomers >= 1 and numberOfDepots >= 2:
        g = graph.buildGraph(numberOfCustomers, numberOfDepots, maxDistance)  # for testing
    else:
        raise ValueError("The network must have at least 1 customer and 2 depots.")
    #print(g)
    #simplePathsTest = simplePaths.exploreSimplePaths(g, 3, 0)
    #simplePathsTest = simplePaths.filterSimplePaths(g,simplePathsTest)
    #print([[node.getName() for node in trip] for trip in simplePathsTest])
    #print(len(simplePathsTest))
    #simplePathsTest2 = simplePaths.exploreSimplePathsNonRecursive(g, 3, 0)
    #print([[node.getName() for node in trip] for trip in simplePathsTest2])

    #print(graph.Path([g.getNode(3), g.getNode(1), g.getNode(2), g.getNode(0)]).computeLength(600))
    #print(graph.Path([g.getNode(3), g.getNode(2), g.getNode(1), g.getNode(0)]).computeLength(600))

    #for path in simplePathsTest:
    #    if path not in simplePathsTest2:
            #print(path)
    #        pass

    #simplePathsTest = simplePaths.filterSimplePaths(g, simplePathsTest)
    #print([[node.getName() for node in trip] for trip in simplePathsTest])
    #print(len(simplePathsTest))
    #filteredSimplePaths = simplePaths.filterSimplePaths(g, simplePathsTest, droneSpeed=600)
    #print([[node.getName() for node in path] for path in filteredSimplePaths])

    #allSimplePathsRecursive = simplePaths.exploreAllSimplePaths(g, recursiveAlgorithm=True, printStatistics=True)
    #print([[node.getName() for node in trip] for trip in allSimplePathsRecursive])
    allSimplePathsNonRecursive = simplePaths.exploreAllSimplePaths(g, recursiveAlgorithm=False, printStatistics=True)
    #print([[node.getName() for node in trip] for trip in allSimplePathsNonRecursive])
    #for path in allSimplePathsRecursive:
        #if path not in allSimplePathsNonRecursive and len(path) >= 5:
            #print([node.getName() for node in path])

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