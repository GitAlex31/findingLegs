# Author : Alexandre Dossin

import graph, simplePaths, inputWithLegs, inputWithoutLegs, display
import time, pickle, random

def main():

    numberOfCustomers = 7
    numberOfDepots = 2
    maxDistance = 1000  # in meters
    random.seed(123)  # useful for debugging purposes
    timeWindows = simplePaths.buildTimeWindows(numberOfDepots, tightTW=True)
    if numberOfCustomers >= 1 and numberOfDepots >= 1:
        g = graph.buildGraph(numberOfCustomers, numberOfDepots, maxDistance, timeWindows)  # building a random graph
        pickle.dump(g, open("../temp/graph.p", "wb"))
    else:
        raise ValueError("The network must have at least 1 customer and 1 depot.")

    #print(g)

    # allSimplePathsNonRecursive = simplePaths.exploreAllSimplePaths(g, recursiveAlgorithm=False, printStatistics=True)[0]
    # allSimplePathsNonRecursiveLeg = simplePaths.exploreAllSimplePaths(g, recursiveAlgorithm=False, printStatistics=True)[1]
    # allSimplePathsRecursive = simplePaths.exploreAllSimplePaths(g, recursiveAlgorithm=True, printStatistics=True)
    # print([[node.getName() for node in trip] for trip in allSimplePathsRecursive])
    # print([[node.getName() for node in trip] for trip in allSimplePathsNonRecursive])
    # print([[node.getName() for node in trip.nodesList] for trip in allSimplePathsNonRecursiveLeg])

    generateInputFileForVrpGencol = True  # boolean used to decide if the input files are generated for GENCOL or VrpGencol
    generateInputFileWithLegs = True
    if generateInputFileWithLegs:  # boolean used to decide if the input files are generated with the the legs enumeration or not
        antiSymmetryBool = True  # boolean used to decide if the input file is generated with the anti symmetry nodes and arcs
    #timeWindows = [[0, 86400]] * numberOfDepots  # for the moment the time windows are not restrictive
    fixedCost = 10000  # if high value, the problem is the minimization of the number of vehicles
    if generateInputFileWithLegs:
        if generateInputFileForVrpGencol:
            if not antiSymmetryBool:
                fileName = "problemVrp{}_{}_{}.out".format(numberOfCustomers, numberOfDepots, "tight15")
            else:
                fileName = "problemVrp{}_{}_{}_as.out".format(numberOfCustomers, numberOfDepots, "tight15")
        else:
            fileName = "problem{}_{}_{}.out".format(numberOfCustomers, numberOfDepots, "tight15")

        # if uncommented, returns an informative text file on the generated legs (can take time)
        #input.createInputFile(g, "clients.txt", recursiveAlgorithm=False, printStatistics=False)

        if generateInputFileForVrpGencol:
            inputWithLegs.createCompleteVrpGENCOLInputFile(fileName, g, fixedCost, timeWindows, droneSpeed=600, droneAutonomy=25, recursiveAlgorithm=False, printStatistics=True, antiSymmetry=antiSymmetryBool)
        else:
            inputWithLegs.createCompleteGENCOLInputFile(fileName, g, fixedCost, timeWindows, droneSpeed=600, droneAutonomy=25, recursiveAlgorithm=False, printStatistics=True)
    else:
        if generateInputFileForVrpGencol:
            fileName = "problemVrp{}_{}_{}_p.out".format(numberOfCustomers, numberOfDepots, "tight15")
        else:
            fileName = "problem{}_{}_{}_p.out".format(numberOfCustomers, numberOfDepots, "tight15")

        if generateInputFileForVrpGencol:
            inputWithoutLegs.createCompleteVrpGENCOLInputFile(fileName, g, fixedCost, timeWindows, serviceTime=5, droneSpeed=600, droneAutonomy=25)
        else:
            inputWithoutLegs.createCompleteGENCOLInputFile(fileName, g, fixedCost, timeWindows, serviceTime=5, droneSpeed=600, droneAutonomy=25)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("\n Time used for main function : --- %s seconds ---" % (time.time() - start_time))