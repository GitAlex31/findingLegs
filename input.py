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
        # making an object of the path is used to compute in a more OOP way the length of that path
        legObject = graph.Path(leg)
        time = legObject.computeLength(droneSpeed)
        visitedNodesStr = str()
        if len(leg) > 2:
            visitedNodesStr = " ".join([node.getName() for node in leg[1:-1]])


        myFile.write(str(leg_id) + '        ' + str(round(time, 1)) + '         ' + str(leg[0].getName())
                     + '           ' + str(leg[-1].getName()) + '                   '
                     '[' + visitedNodesStr + ']')
        myFile.write('\n')
    pass





