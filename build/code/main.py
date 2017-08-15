# Author : Alexandre Dossin

import graph, simplePaths, inputWithLegs, inputWithoutLegs
import time, pickle, random
import sys

def main():

    sys.stdout = open('stdout.txt', 'w')  # writes the standard output to a stdout.txt instead of the standard output
    droneAutonomyList = [60]  # considered fixed

    # numberOfCustomersList = [10, 15, 20, 25, 30, 35]
    # numberOfDepotsList = [3, 4, 5]
    # timeWindowsList = ["tight15", "tight30", "tight45", "tight60"]
    # serviceTimeList = [45, 30, 20, 15]

    numberOfCustomersList = [30, 35]
    numberOfDepotsList = [2]
    timeWindowsList = ["tight45"]
    serviceTimeList = [15]

    for numberOfDepotsItr in numberOfDepotsList:
        for droneAutonomyItr in droneAutonomyList:
            for timeWindowsTypeItr in timeWindowsList:
                print("Time windows type : {}\n".format(timeWindowsTypeItr))
                for serviceTimeItr in serviceTimeList:
                    for numberOfCustomersItr in numberOfCustomersList:
                        #print("Service time : {}".format(serviceTimeItr))

                        random.seed(123)  # useful for debugging purposes - leave as "123"
                        maxDistance = 5000  # in meters
                        numberOfCustomers = numberOfCustomersItr
                        numberOfDepots = numberOfDepotsItr
                        droneAutonomy = droneAutonomyItr  # in minutes
                        timeWindowsType = timeWindowsTypeItr  # user-defined time windows in minutes
                        droneSpeed = 666  # in meters per minute (666 m/min -> 40 km/h)

                        if "tight" in timeWindowsType:
                            timeWindows = simplePaths.buildTimeWindows(numberOfDepots, tightTW=True,
                                                                       TWspacing=int(timeWindowsType[5:]))
                        elif timeWindowsType == "random":
                            timeWindows = simplePaths.buildTimeWindows(numberOfDepots, randomTW=True)
                        elif timeWindowsType == "separated":
                            timeWindows = simplePaths.buildTimeWindows(numberOfDepots, separatedTW=True)
                        else:
                            raise ValueError("Time windows not specified.")

                        if numberOfCustomers >= 1 and numberOfDepots >= 1:
                            # building a random graph with specified parameters
                            g = graph.buildGraph(numberOfCustomers, numberOfDepots, maxDistance, timeWindows, serviceTimeItr)
                            # pickle.dump(g, open("../temp/graph{}_{}_{}_{}_s{}.p".format(numberOfCustomers,
                            #                                                             numberOfDepots, maxDistance,
                            #                                                             timeWindowsType,
                            #                                                             serviceTimeItr), "wb"))
                            # we save the produced graph in a binary file useful for the display functionality
                            pickle.dump(g, open("../temp/graph{}_{}_{}.p".format(numberOfCustomers, numberOfDepots,
                                                                                 maxDistance), "wb"))
                        else:
                            raise ValueError("The network must have at least 1 customer and 1 depot.")

                        #print(g)

                        #allSimplePathsNonRecursive = simplePaths.exploreAllSimplePaths(g, recursiveAlgorithm=False, printStatistics=True)[0]
                        #allSimplePathsNonRecursiveLeg = simplePaths.exploreAllSimplePaths(g, recursiveAlgorithm=False, printStatistics=True)[1]
                        #allSimplePathsRecursive = simplePaths.exploreAllSimplePaths(g, recursiveAlgorithm=True, printStatistics=True)
                        #print([[node.getName() for node in trip] for trip in allSimplePathsRecursive])
                        #print([[node.getName() for node in trip] for trip in allSimplePathsNonRecursive])
                        #print([[node.getName() for node in trip.nodesList] for trip in allSimplePathsNonRecursiveLeg])

                        generateInputFileForVrpGencol = True  # boolean used to decide if the input files are generated for GENCOL or VrpGencol
                        generateInputFileWithLegs = True  # boolean used to decide if the input files are generated with the the legs enumeration or not
                        antiSymmetryBool = True  # boolean used to decide if the input file is generated with the anti symmetry nodes and arcs
                        #timeWindows = [[0, 86400]] * numberOfDepots  # for the moment the time windows are not restrictive
                        fixedCost = 10000  # if high value, the problem is the minimization of the number of vehicles
                        if generateInputFileWithLegs:
                            if generateInputFileForVrpGencol:
                                if not antiSymmetryBool:
                                    fileName = "problemVrp{}_{}_{}_s{}_a{}.out".format(numberOfCustomers,
                                                                                       numberOfDepots, timeWindowsType,
                                                                                       serviceTimeItr, droneAutonomy)
                                else:
                                    fileName = "problemVrp{}_{}_{}_s{}_a{}_as.out".format(numberOfCustomers,
                                                                                       numberOfDepots, timeWindowsType,
                                                                                       serviceTimeItr, droneAutonomy)
                            else:
                                #fileName = "problem{}_{}_{}.out".format(numberOfCustomers, numberOfDepots, timeWindowsType)
                                pass

                            if generateInputFileForVrpGencol:
                                inputWithLegs.createCompleteVrpGENCOLInputFile(fileName, g, fixedCost, timeWindows,
                                                                               droneSpeed=droneSpeed,
                                                                               droneAutonomy=droneAutonomy,
                                                                               recursiveAlgorithm=False,
                                                                               printStatistics=True,
                                                                               antiSymmetry=antiSymmetryBool)
                            else:
                                #inputWithLegs.createCompleteGENCOLInputFile(fileName, g, fixedCost, timeWindows,
                                # droneSpeed=droneSpeed, droneAutonomy=droneAutonomy,
                                # recursiveAlgorithm=False, printStatistics=True)
                                pass
                        else:
                            if generateInputFileForVrpGencol:
                                fileName = "problemVrp{}_{}_{}_s{}_a{}_p.out".format(numberOfCustomers, numberOfDepots,
                                                                                      timeWindowsType, serviceTimeItr,
                                                                                      droneAutonomy)
                            else:
                                #fileName = "problem{}_{}_{}_{}_p.out".format(numberOfCustomers, numberOfDepots, timeWindowsType, droneAutonomy)
                                pass

                            if generateInputFileForVrpGencol:
                                inputWithoutLegs.createCompleteVrpGENCOLInputFile(fileName, g, fixedCost, timeWindows,
                                                                                  serviceTime=serviceTimeItr,
                                                                                  droneSpeed=droneSpeed,
                                                                                  droneAutonomy=droneAutonomy)
                            else:
                                inputWithoutLegs.createCompleteGENCOLInputFile(fileName, g, fixedCost, timeWindows,
                                                                               serviceTime=serviceTimeItr,
                                                                               droneSpeed=droneSpeed,
                                                                               droneAutonomy=droneAutonomy)
                        sys.stdout.flush()  # resets the buffer of stdout


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("\n Time used for main function : --- %s seconds ---" % (time.time() - start_time))