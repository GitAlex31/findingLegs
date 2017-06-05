# Author : Alexandre Dossin

import graph, simplePaths, inputWithLegs, inputWithoutLegs, display
import time, pickle

def main():

    numberOfCustomers = 3
    numberOfDepots = 2
    maxDistance = 1000  # in meters
    if numberOfCustomers >= 1 and numberOfDepots >= 2:
        g = graph.buildGraph(numberOfCustomers, numberOfDepots, maxDistance)  # building a random graph
        pickle.dump(g, open("../temp/graph.p", "wb"))
    else:
        raise ValueError("The network must have at least 1 customer and 2 depots.")

    #print(g)

    # allSimplePathsNonRecursive = simplePaths.exploreAllSimplePaths(g, recursiveAlgorithm=False, printStatistics=True)
    # allSimplePathsRecursive = simplePaths.exploreAllSimplePaths(g, recursiveAlgorithm=True, printStatistics=True)
    # print([[node.getName() for node in trip] for trip in allSimplePathsRecursive])
    # print([[node.getName() for node in trip] for trip in allSimplePathsNonRecursive])

    timeWindows = simplePaths.buildTimeWindows(numberOfDepots, tightTW=True)
    generateInputFileWithLegs = True  # boolean used to decide if the input files are generated with the the legs enumeration or not
    generateInputFileForVrpGencol = True  # boolean used to decide if the input files are generated for GENCOL or VrpGencol
    #timeWindows = [[0, 86400]] * numberOfDepots  # for the moment the time windows are not restrictive
    fixedCost = 10000  # if high value, the problem is the minimization of the number of vehicles
    if generateInputFileWithLegs:
        if generateInputFileForVrpGencol:
            fileName = "inputVrp{}_{}_{}.txt".format(numberOfCustomers, numberOfDepots, "tight5")
        else:
            fileName = "input{}_{}_{}.txt".format(numberOfCustomers, numberOfDepots, "tight5")

        # if uncommented, returns an informative text file on the generated legs (can be long)
        #input.createInputFile(g, "clients.txt", recursiveAlgorithm=False, printStatistics=False)

        if generateInputFileForVrpGencol:
            inputWithLegs.createCompleteVrpGENCOLInputFile(fileName, g, fixedCost, timeWindows, droneSpeed=600, droneAutonomy=25, recursiveAlgorithm=False, printStatistics=True)
        else:
            inputWithLegs.createCompleteGENCOLInputFile(fileName, g, fixedCost, timeWindows, droneSpeed=600, droneAutonomy=25, recursiveAlgorithm=False, printStatistics=True)
    else:
        if generateInputFileForVrpGencol:
            fileName = "inputVrp{}_{}_{}_p.txt".format(numberOfCustomers, numberOfDepots, "tight5")
        else:
            fileName = "input{}_{}_{}_p.txt".format(numberOfCustomers, numberOfDepots, "tight5")

        if generateInputFileForVrpGencol:
            inputWithoutLegs.createCompleteVrpGENCOLInputFile(fileName, g, fixedCost, timeWindows, serviceTime=5, droneSpeed=600, droneAutonomy=25)
        else:
            inputWithoutLegs.createCompleteGENCOLInputFile(fileName, g, fixedCost, timeWindows, serviceTime=5, droneSpeed=600, droneAutonomy=25)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("\n Time used for main function : --- %s seconds ---" % (time.time() - start_time))