# Author : Alexandre Dossin

import simplePaths
import graph

def createSummaryFile(g, fileName, droneSpeed=600, droneAutonomy=25, recursiveAlgorithm=True, printStatistics=False):
    """Returns a text file that contains the list of legs with all the neecessary information.
    A leg is represented by a unique id, its time of travel, origin and a destination depots, and the
    list of its visited customers or sites.
    Beware : the returned text is only informative but not used by GENCOL or other program in any way."""

    simplePathsList, simplePathsListLeg = simplePaths.exploreAllSimplePaths(g, droneSpeed, droneAutonomy, recursiveAlgorithm, printStatistics)

    fileName = "../output/" + fileName  # builds the input file into the right directory
    myFile = open(fileName, "w")
    myFile.write("Number of customers: {}   Number of Depots: {}    Drone Autonomy: {} min  Drone Speed:{} m/min"
                 .format(len(g.getCustomers()), int(len(g.getDepots()) / 2), droneAutonomy, droneSpeed))
    myFile.write('\n \n')

    # description of the columns
    myFile.write("leg_id    time    originDepot destinationDepot    visitedNodes")
    myFile.write('\n')

    # filling the file with legs
    for i, leg in enumerate(simplePathsList):
        leg_id = i

        if leg[0] in g.getOtherDepots():  # associate a real depot to the virtual one
            dep = g.getRealDepots()[g.getOtherDepots().index(leg[0])]
        else:
            dep = leg[0]

        if leg[-1] in g.getOtherDepots():
            dest = g.getRealDepots()[g.getOtherDepots().index(leg[-1])]
        else:
            dest = leg[-1]

        legObject = graph.Path(leg)  # more OOP way

        time = legObject.computeLength(droneSpeed)

        visitedNodesStr = str()
        if len(leg) > 2:
            visitedNodesStr = " ".join([node.getName() for node in leg[1:-1]])


        myFile.write(str(leg_id) + '        ' + str(round(time, 1)) + '         ' + str(dep.getName())
                     + '           ' + str(dest.getName()) + '                   '
                     '[' + visitedNodesStr + ']')
        myFile.write('\n')
    pass

def createGENCOLInputFile(fileName):
    myFile = open(fileName, 'w')
    pass

def createGENCOLInputFileResources(fileName, antiSymmetryArcs=False):
    myFile = open(fileName, 'a')
    if not antiSymmetryArcs:
        myFile.write("Resources={\nTime Strong;\n};\n\n")
    if antiSymmetryArcs:
        myFile.write("Resources={\nTime Strong;\n")
        myFile.write("antiSymmetry Strong;\n};\n\n")
    pass


def createGENCOLInputFileRows(fileName, g):
    myFile = open(fileName, 'a')
    myFile.write("Rows={\n")
    for customer in range(1, len(g.getCustomers()) + 1):
        myFile.write("RowD{} = 1 TaskStrong;\n".format(str(customer)))
    myFile.write("RowVeh = 0;\n};\n\n")
    pass

def createGENCOLInputFileTasks(fileName, g):
    myFile = open(fileName, 'a')
    myFile.write("Tasks={\n")
    for customer in range(1, len(g.getCustomers()) + 1):
        myFile.write("D{} RowD{} Strong;\n".format(str(customer), str(customer)))
    myFile.write("};\n\n")
    pass

def createGENCOLInputFileColumns(fileName, fixedCost):
    myFile = open(fileName, 'a')
    myFile.write("Columns={\n")
    myFile.write("Vehicles {} Int(RowVeh 1);\n".format(int(fixedCost)))
    myFile.write("};\n\n")
    pass

def createGENCOLInputFileNodes(fileName, g, timeIntervals):
    myFile = open(fileName, 'a')
    myFile.write("Nodes={\n")
    myFile.write("Source [0 0];\n")

    for i, depot in enumerate(g.getRealDepots()):
        myFile.write("N{} [{} {}]; \n".format(str(depot.getName()) + "arr", timeIntervals[i][0], timeIntervals[i][1]))#, str(depot.getName())))
        myFile.write("N{} [{} {}]; \n".format(str(depot.getName()) + "dep", timeIntervals[i][0], timeIntervals[i][1]))#, str(depot.getName())))

    myFile.write("Destination [0 86400];\n")
    myFile.write("};\n\n")
    pass


def createGENCOLInputFileNodesAndArcs(fileName, g, droneSpeed=600, droneAutonomy=25, recursiveAlgorithm=False,
                                      printStatistics=False, VrpGencolFormatting=False, antiSymmetry=False, timeIntervals=None):

    simplePathsList, simplePathsListLeg = simplePaths.exploreAllSimplePaths(g, droneSpeed, droneAutonomy, recursiveAlgorithm, printStatistics)

    antiSymmetryNodeIdx = 0

    myFile = open(fileName, 'a')

    if antiSymmetry:  # we decide whether or not we write the nodes for symmetry breaking
        myFile.write("Nodes={\n")
        myFile.write("Source [0 0] [0 0];\n")

        for i, depot in enumerate(g.getRealDepots()):  # first we create the "normal" nodes
            myFile.write(
                "N{} [{} {}] [0 9999] <A{}>; \n".format(str(depot.getName()) + "arr", timeIntervals[i][0], timeIntervals[i][1], str(depot.getName())))
            myFile.write(
                "N{} [{} {}] [0 9999] <D{}>; \n".format(str(depot.getName()) + "dep", timeIntervals[i][0], timeIntervals[i][1], str(depot.getName())))

        myFile.write("Destination [0 86400] [0 9999];\n")

        for i, leg in enumerate(simplePathsListLeg):  # then the nodes used to break the symmetry
            if leg.nodesList[0] in g.getOtherDepots():
                associatedDepot = g.getRealDepots()[g.getOtherDepots().index(leg.nodesList[0])]
                lowerTW_0 = timeIntervals[g.getRealDepots().index(associatedDepot)][0]
                upperTW_0 = timeIntervals[g.getRealDepots().index(associatedDepot)][1]
            else:
                lowerTW_0 = timeIntervals[g.getRealDepots().index(leg.nodesList[0])][0]
                upperTW_0 = timeIntervals[g.getRealDepots().index(leg.nodesList[0])][1]

            lowerTW_m1 = timeIntervals[g.getRealDepots().index(leg.nodesList[-1])][0]
            upperTW_m1 = timeIntervals[g.getRealDepots().index(leg.nodesList[-1])][1]

            if leg.nodesList[0] in g.getOtherDepots():  # symmetry breaking is only useful for legs with the same beginning and ending nodes
                myFile.write("A{0} [{1} {2}] [{3} {3}];\n"
                             .format(str(i+1), min(lowerTW_0, lowerTW_m1), max(upperTW_0, upperTW_m1),  str(leg.identity)))

        myFile.write("};\n\n")

    myFile.write("Arcs={\n")

    for leg in simplePathsList:

        if leg[0] in g.getOtherDepots():  # associate a real depot to the virtual one
            dep = g.getRealDepots()[g.getOtherDepots().index(leg[0])]
        else:
            dep = leg[0]

        if leg[-1] in g.getOtherDepots():
            dest = g.getRealDepots()[g.getOtherDepots().index(leg[-1])]
        else:
            dest = leg[-1]

        legObject = graph.Path(leg)  # more OOP way

        time = legObject.computeLength(droneSpeed)

        visitedNodesStr = str()
        if len(leg) > 2:
            visitedNodesStr = "D" + " D".join([node.getName() for node in leg[1:-1]])

        if VrpGencolFormatting:
            if not antiSymmetry:
                myFile.write("N{} N{} {} as [{}] {};\n".format(dep.getName() + "dep", dest.getName() + "arr", time, time,
                                                            visitedNodesStr))
            else:
                antiSymmetryNodeIdx += 1
                if dep.getName() == dest.getName():
                    myFile.write("N{} A{} {} as [{} 0] {};\n".format(dep.getName() + "dep", antiSymmetryNodeIdx, time, time,
                                                          visitedNodesStr))
                    myFile.write("A{} N{} 0 as [0 0];\n".format(antiSymmetryNodeIdx, dest.getName() + "arr"))
                else:
                    myFile.write("N{} N{} {} as [{} -9999] {};\n".format(dep.getName() + "dep", dest.getName() + "arr", time, time,
                                                             visitedNodesStr))
        else:
            myFile.write("N{} N{} {} [{}] {};\n".format(dep.getName() + "dep", dest.getName() + "arr", time, time, visitedNodesStr))

    # we then add the arcs needed for the modelling of the departure and come-back to the central depot
    if VrpGencolFormatting:
        # first we do that for the Source
        if not antiSymmetry:
            myFile.write("Source N0dep 0 as [0] (RowVeh -1);\n")
            # then for the Destination
            myFile.write("N0arr Destination 0 as [0];\n")
        else:
            myFile.write("Source N0dep 0 as [0 0] (RowVeh -1);\n")
            myFile.write("N0arr Destination 0 as [0 0];\n")
    else:
        myFile.write("Source N0dep 0 [0] (RowVeh -1);\n")
        myFile.write("N0arr Destination 0 [0];\n")

    for depot in g.getRealDepots()[1:]:  # we exclude the source depot whose arc has already been written
        time = int(depot.computeDistance(g.getNode(0)) / droneSpeed * 60)  # computation of the time in seconds
        if VrpGencolFormatting:
            if not antiSymmetry:
                myFile.write("N{0}arr Destination {1} as [{1}];\n".format(depot.getName(), time))
            else:
                myFile.write("N{0}arr Destination {1} as [{1} 0];\n".format(depot.getName(), time))
        else:
            myFile.write("N{0}arr Destination {1} [{1}];\n".format(depot.getName(), time))

    # finally we add the arc corresponding to the battery charging that we initialize to zero for the moment
    for depot in g.getRealDepots():
        if VrpGencolFormatting:
            if not antiSymmetry:
                myFile.write("N{0}arr N{0}dep 0 as [0];\n".format(depot.getName()))
            else:
                myFile.write("N{0}arr N{0}dep 0 as [0 0];\n".format(depot.getName()))
        else:
            myFile.write("N{0}arr N{0}dep 0 [0];\n".format(depot.getName()))

    myFile.write("};\n\n")

    pass


def createGENCOLInputFileNetwork(fileName):
    myFile = open(fileName, 'a')
    myFile.write("Networks={\n")
    myFile.write("Net Source (Destination);")
    myFile.write("\n};")


def createCompleteGENCOLInputFile(fileName, g, fixedCost, timeIntervals, droneSpeed=600, droneAutonomy=25,
                                  recursiveAlgorithm=False, printStatistics=False, VrpGencolFormatting=False, antiSymmetryArcs=False):
    """Creates the complete GENCOL input file used by GENCOL to solve the VRPTW"""
    fileName = "../output/" + fileName  # builds the GENCOL input file into the right directory
    createGENCOLInputFile(fileName)
    createGENCOLInputFileResources(fileName)
    createGENCOLInputFileRows(fileName, g)
    createGENCOLInputFileTasks(fileName, g)
    createGENCOLInputFileColumns(fileName, fixedCost)
    createGENCOLInputFileNodes(fileName, g, timeIntervals)
    createGENCOLInputFileNodesAndArcs(fileName, g, droneSpeed, droneAutonomy, recursiveAlgorithm, printStatistics,
                                      VrpGencolFormatting, antiSymmetryArcs)
    createGENCOLInputFileNetwork(fileName)
    pass


def createVrpGENCOLFileArcSets(fileName):
    myFile = open(fileName, 'a')
    myFile.write("ArcSets={\n")
    myFile.write("as;")
    myFile.write("\n};\n\n")

def createVrpGENCOLInputFileNetwork(fileName):
    myFile = open(fileName, 'a')
    myFile.write("Networks={\n")
    myFile.write("Net Source (Destination) (as);")
    myFile.write("\n};")
    myFile.close()


def createCompleteVrpGENCOLInputFile(fileName, g, fixedCost, timeIntervals, droneSpeed=600, droneAutonomy=25,
                                     recursiveAlgorithm=False, printStatistics=False, VrpGencolFormatting=True, antiSymmetryArcs=True):
    """Creates the VrpGENCOL input file used by VrpGencol to solve the VRP-TW"""
    fileName = "../output/" + fileName  # builds the VrpGencol input file into the right directory
    createGENCOLInputFile(fileName)
    createGENCOLInputFileResources(fileName, antiSymmetryArcs)
    createGENCOLInputFileRows(fileName, g)
    createGENCOLInputFileTasks(fileName, g)
    createGENCOLInputFileColumns(fileName, fixedCost)
    if not antiSymmetryArcs:
        createGENCOLInputFileNodes(fileName, g, timeIntervals)
    createVrpGENCOLFileArcSets(fileName)
    createGENCOLInputFileNodesAndArcs(fileName, g, droneSpeed, droneAutonomy, recursiveAlgorithm, printStatistics,
                                      VrpGencolFormatting, antiSymmetryArcs, timeIntervals)
    createVrpGENCOLInputFileNetwork(fileName)
    pass
