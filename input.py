# Author : Alexandre Dossin
import simplePaths
import graph

def createInputFile(g, fileName, droneSpeed=600, droneAutonomy=25, toPrint=False, printStatistics=False):
    """Returns the input file that contains the list of legs.
    A leg is represented by an id, its cost, an origin and a destination depot and a list of visited customers"""

    simplePathsList = simplePaths.exploreAllSimplePaths(g, droneSpeed, droneAutonomy, toPrint, printStatistics)
    myFile = open(fileName, "w")
    myFile.write("Number of customers: {}   Number of Depots: {}    Drone Autonomy: {} min  Drone Speed:{} m/min"
                 .format(len(g.getCustomers()), len(g.getDepots()), droneAutonomy, droneSpeed))
    myFile.write('\n \n')

    # description of the columns
    myFile.write("leg_id    time    originDepot destinationDepot    visitedNodes")
    myFile.write('\n')

    # filling the file with legs
    for i, leg in enumerate(simplePathsList):
        leg_id = i

        if leg[0] in g.getOtherDepots():
            dep = g.getNode(int(leg[0].getName()) - 1)
        else:
            dep = leg[0]

        if leg[-1] in g.getOtherDepots():
            dest = g.getNode(int(leg[-1].getName()) - 1)
        else:
            dest = leg[-1]
        legObject = graph.Path(leg)  # more OOP way
        time = legObject.computeLength(droneSpeed)
        visitedNodesStr = str()
        if len(leg) > 2:
            visitedNodesStr = " ".join([node.getName() for node in leg[1:-1]])


        myFile.write(str(leg_id) + '        ' + str(round(time, 1)) + '         ' + str(dest.getName())
                     + '           ' + str(dest.getName()) + '                   '
                     '[' + visitedNodesStr + ']')
        myFile.write('\n')
    pass

def createGENCOLInputFile(fileName):
    myFile = open(fileName, 'w')
    pass

def createGENCOLInputFileResources(fileName):
    myFile = open(fileName, 'a')
    myFile.write("Resources={\nTime Strong;\n};")
    pass

def createGENCOLInputFileRows():
    pass

"""fileName = "test.txt"
createGENCOLInputFile(fileName)
createGENCOLInputFileResources(fileName)"""




