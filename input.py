import simplePaths
import graph

def createInputFile(g, fileName, droneSpeed=600, droneAutonomy=25, toPrint= False):
    """Returns the input file that contains the list of legs.
    A leg is represented by an id, its cost, an origin and a destination depot and a list of visited customers"""

    simplePathsList = simplePaths.exploreAllSimplePaths(g, droneSpeed, droneAutonomy, toPrint)
    myFile = open(fileName, "w")
    myFile.write("Number of customers: {}   Number of Depots: {}    Drone Autonomy: {} min  Drone Speed:{} m/s"
                 .format(len(g.getCustomers()), len(g.getDepots()), droneAutonomy, droneSpeed))

    pass





