# Author : Alexandre Dossin


def createGENCOLInputFile(fileName):
    myFile = open(fileName, 'w')
    pass

def createGENCOLInputFileResources(fileName):
    myFile = open(fileName, 'a')
    myFile.write("Resources={\nTime Strong;\nAutonomy Strong;\n};\n\n")
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


def createGENCOLInputFileNodes(fileName, g, timeIntervals, droneAutonomy=25):
    myFile = open(fileName, 'a')
    myFile.write("Nodes={\n")

    myFile.write("Source [0 0] [0 0];\n")

    #droneAutonomy *= 60  # converting minutes to seconds

    for i, depot in enumerate(g.getRealDepots()):  # writing the rows for the depots
        myFile.write("N{}arr [{} {}] [{} {}]; \n".format(str(depot.getName()), timeIntervals[i][0], timeIntervals[i][1], 0, droneAutonomy))
        myFile.write("N{}dep [{} {}] [{} {}]; \n".format(str(depot.getName()), timeIntervals[i][0], timeIntervals[i][1], 0, droneAutonomy))

    for customer in g.getCustomers():  # writing the rows for the customers
        myFile.write("C{} [{} {}] [{} {}] D{}; \n".format(str(customer.getName()), 0, 3600, 0, droneAutonomy, str(customer.getName())))

    myFile.write("Destination [0 3600] [0 {}];\n".format(droneAutonomy))

    myFile.write("};\n\n")
    pass


def createGENCOLInputFileArcs(fileName, g, serviceTime, droneSpeed=666, droneAutonomy=45, VrpGencolFormatting=False):

    myFile = open(fileName, 'a')
    myFile.write("Arcs={\n")

    #droneAutonomy *= 60  # converting minutes to seconds
    #serviceTime *= 60

    # if VrpGencolFormatting:
    #     myFile.write("Source N0dep 0 as [0 0] (RowVeh -1);\n")
    # else:
    #     myFile.write("Source N0dep 0 [0 0] (RowVeh -1);\n")

    for customer in g.getCustomers():  # writing rows between customers
        for otherCustomer in g.getCustomers():
            if customer != otherCustomer:
                time = int(g.distanceMatrix[int(customer.getName())][int(otherCustomer.getName())] / droneSpeed)
                if VrpGencolFormatting:
                    myFile.write("C{0} C{1} {2} as [{2} {2}];\n".format(customer.getName(), otherCustomer.getName(), time + serviceTime))
                else:
                    myFile.write("C{0} C{1} {2} [{2} {2}];\n".format(customer.getName(), otherCustomer.getName(), time + serviceTime))

    for depot in g.getRealDepots():  # writing rows between depots
        for otherDepot in g.getRealDepots():
            if depot != otherDepot:
                time = int(g.distanceMatrix[int(depot.getName())][int(otherDepot.getName())] / droneSpeed)
                if VrpGencolFormatting:
                    myFile.write("N{0}dep N{1}arr {2} as [{2} {2}];\n".format(depot.getName(), otherDepot.getName(), time))
                else:
                    myFile.write("N{0}dep N{1}arr {2} [{2} {2}];\n".format(depot.getName(), otherDepot.getName(), time))

    for depot in g.getRealDepots():  # writing rows for the charging at the different stations
        chargingTime = 0  # in the first place we put a negligible charging time similar to a change of the batteries
        if VrpGencolFormatting:
            myFile.write("N{0}arr N{0}dep {1} as [{1} {2}];\n".format(depot.getName(), chargingTime, "-" + str(droneAutonomy)))
        else:
            myFile.write("N{0}arr N{0}dep {1} [{1} {2}];\n".format(depot.getName(), chargingTime, "-" + str(droneAutonomy)))

    for customer in g.getCustomers():  # writing rows between customers and depots
        for depot in g.getRealDepots():
            time = int(g.distanceMatrix[int(customer.getName())][int(depot.getName())] / droneSpeed)
            # service time is taken into account the last visited node only
            if VrpGencolFormatting:
                myFile.write("C{0} N{1}arr {2} as [{2} {2}];\n".format(customer.getName(), depot.getName(), time))
                myFile.write("N{0}dep C{1} {2} as [{2} {2}];\n".format(depot.getName(), customer.getName(), time + serviceTime))
            else:
                myFile.write("C{0} N{1}arr {2} [{2} {2}];\n".format(customer.getName(), depot.getName(), time))
                myFile.write("N{0}dep C{1} {2} [{2} {2}];\n".format(depot.getName(), customer.getName(), time + serviceTime))

    for depot in g.getRealDepots():  # writing rows between depots and Destination
        time = int(g.distanceMatrix[0][int(depot.getName())] / droneSpeed)
        if VrpGencolFormatting:
            myFile.write("Source N{0}dep {1} as [{1} {1}] (RowVeh -1);\n".format(depot.getName(), time))
            myFile.write("N{0}arr Destination {1} as [{1} {1}];\n".format(depot.getName(), time))
        else:
            myFile.write("Source N{0}dep {1} [{1} {1}] (RowVeh -1);\n".format(depot.getName(), time))
            myFile.write("N{0}arr Destination {1} [{1} {1}];\n".format(depot.getName(), time))
    myFile.write("};\n\n")

    pass

def createGENCOLInputFileNetwork(fileName):
    myFile = open(fileName, 'a')
    myFile.write("Networks={\n")
    myFile.write("Net Source (Destination);")
    myFile.write("\n};")


def createCompleteGENCOLInputFile(fileName, g, fixedCost, timeIntervals, serviceTime, droneSpeed=666, droneAutonomy=45,
                                  VrpGencolFormatting=False):
    """Creates the comple GENCOL input file without generating the legs"""
    fileName = "../output/" + fileName  # builds the gencol input file into the right directory
    createGENCOLInputFile(fileName)
    createGENCOLInputFileResources(fileName)
    createGENCOLInputFileRows(fileName, g)
    createGENCOLInputFileTasks(fileName, g)
    createGENCOLInputFileColumns(fileName, fixedCost)
    createGENCOLInputFileNodes(fileName, g, timeIntervals, droneAutonomy)
    createGENCOLInputFileArcs(fileName, g, serviceTime, droneSpeed, droneAutonomy, VrpGencolFormatting)
    createGENCOLInputFileNetwork(fileName)
    pass

def createVrpGENCOLFileArcSets(fileName):
    myFile = open(fileName, 'a')
    myFile.write("ArcSets={\n")
    myFile.write("as;\n")
    myFile.write("};\n\n")

def createVrpGENCOLInputFileNetwork(fileName):
    myFile = open(fileName, 'a')
    myFile.write("Networks={\n")
    myFile.write("Net Source (Destination) (as);")
    myFile.write("\n};")

def createCompleteVrpGENCOLInputFile(fileName, g, fixedCost, timeIntervals, serviceTime, droneSpeed=666,
                                     droneAutonomy=45, VrpGencolFormatting=True):
    """Creates the comple GENCOL input file without generating the legs"""
    fileName = "../output/" + fileName  # builds the gencol input file into the right directory
    createGENCOLInputFile(fileName)
    createGENCOLInputFileResources(fileName)
    createGENCOLInputFileRows(fileName, g)
    createGENCOLInputFileTasks(fileName, g)
    createGENCOLInputFileColumns(fileName, fixedCost)
    createGENCOLInputFileNodes(fileName, g, timeIntervals, droneAutonomy)
    createVrpGENCOLFileArcSets(fileName)
    createGENCOLInputFileArcs(fileName, g, serviceTime, droneSpeed, droneAutonomy, VrpGencolFormatting)
    createVrpGENCOLInputFileNetwork(fileName)
    pass