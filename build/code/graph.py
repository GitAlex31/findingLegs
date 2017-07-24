# Author : Alexandre Dossin

import math, random

# graph.py contains the classes implementation : Node, Arc, Path and Digraph classes

class Node(object):
    def __init__(self, name, x, y, serviceTime=0, timeWindow = (0, 86400)):
        """A node has 4 attributes : its name, coordinates x and y, a service time, and a time window.
        Service time and time windows are respectively 0 and [0, 86400] (one day) by default. """
        self.name = name
        self.x = x
        self.y = y
        self.serviceTime = serviceTime
        self.timeWindow = timeWindow

    def getName(self):
        return self.name
    def getServiceTime(self):
        return self.serviceTime
    def getCoordinates(self):
        return (self.x, self.y)
    def getTimeWindow(self):
        return self.timeWindow

    def computeDistance(self, other):
        """Returns the euclidian distance between two nodes."""
        return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))

    def __str__(self):
        """String representation of a Node."""
        return "Node " + self.name + " with coordinates " + "(" + str(int(self.x)) + "," + str(int(self.y)) + ")" \
               + " and time window [" + str(self.getTimeWindow()[0]) + "," + str(self.getTimeWindow()[1]) + "]"

    def __lt__(self, other):
        """Definition of Node sorting by name index."""
        return int(self.getName()) < int(other.getName())

    def __ge__(self, other):
        return int(self.getName()) >= int(other.getName())


class Arc(object):
    def __init__(self, dep, dest):
        """An arc has two attributes : its departure and destination nodes."""
        self.dep = dep
        self.dest = dest
        self.dist = Node.computeDistance(self.dep, self.dest)  # distance between 2 nodes
        # is an attribute for fast computation

    def getSource(self):
        return self.dep
    def getDestination(self):
        return self.dest
    def getDistance(self):
        return self.dist

    def __str__(self):
        """String representation of an arc."""
        return str(self.dep) + '->' + str(self.dest) + ' of distance ' + str(self.dist)


class Path(object):

    def __init__(self, nodesList):
        """A path consists in an ordered list of nodes."""
        self.nodesList = nodesList

    def computeLength(self, speed):
        """Returns the length of the path, without counting the service time of the origin or destination nodes.
        Operations are performed in seconds in order to get the same results as the solution without leg generation."""
        length = 0
        for i in range(len(self.nodesList[:-1])):
            if i != 0:
                length += int(self.nodesList[i].getServiceTime() * 60)
            length += int(float(self.nodesList[i].computeDistance(self.nodesList[i + 1])) * 60 / speed)
        return int(length)

    def computeLengthWithDistanceMatrix(self, g, speed):
        """Returns the length of the path, without counting the service time of the origin or destination nodes.
        It uses a distance matrix, which is an attribute of the graph, that in turn accelerate the algorithm.
        Operations are performed in seconds in order to get the same results as the solution without leg generation."""
        length = 0
        for i in range(len(self.nodesList[:-1])):
            if i != 0:
                length += int(self.nodesList[i].getServiceTime() * 60)
            length += int((g.distanceMatrix[int(self.nodesList[i].getName())][int(self.nodesList[i+1].getName())] / speed) * 60)
        return int(length)


class Digraph(object):

    def __init__(self):
        """A Digraph has a set of nodes and a dictionary of edges, in the form of an adjacency list."""
        self.nodes = set([])  # a set in Python is an unordered collection of unique elements
        self.edges = {}
        self.distanceMatrix = None  # initialization of the distance matrix

    def addNode(self, node):
        """Adds node to the set of nodes and an empty list to the dictionary of edges with node key."""
        if node.getName() in self.nodes:
            raise ValueError('Duplicate node')  # verify if the node is not already in the nodes set
        else:
            self.nodes.add(node)
            self.edges[node] = []

    def addEdge(self, edge):
        """Adds edge of source dep and destination dest in the edges dictionary in the form of an adjacency list."""
        dep = edge.getSource()
        dest = edge.getDestination()
        if not (dep in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')  # verify if both source and dest are in the node set
        self.edges[dep].append(dest)

    def childrenOf(self, node):
        """Returns the list of the children of node."""
        return self.edges[node]

    def hasNode(self, node):
        """Returns True if node is in the set of nodes."""
        return node in self.nodes

    def getNode(self, idx):
        """Returns node named idx if present in nodes set."""
        idx = str(idx)  # str conversion to provide a working comparison
        list_aux = [node for node in self.nodes if node.getName() == idx]
        if list_aux == []:
            raise ValueError("Node not present in list of nodes")
        else:
            return list_aux[0]

    def getNodes(self):
        """Returns the sorted list of nodes, either a customer or a depot."""
        return sorted(self.nodes)

    def getCustomers(self):
        """Returns the sorted list of nodes that represent customers, i.e. have a service time different from -1."""
        return sorted([node for node in self.nodes if node.getServiceTime() != -1])

    def getDepots(self):
        """Returns the list of nodes that represent depots, i.e. have a service time of -1."""
        return [node for node in self.nodes if node.getServiceTime() == -1]

    def getRealDepots(self):
        """Returns the list of real depots"""
        sortedDepotsList = sorted(self.getDepots())
        return [depot for depot in sortedDepotsList if sortedDepotsList.index(depot) % 2 == 0]

    def getOtherDepots(self):
        """Returns the list of virtual depots used for self-loops paths."""
        sortedDepotsList = sorted(self.getDepots())
        return [depot for depot in sortedDepotsList if sortedDepotsList.index(depot) % 2 != 0]

    def __str__(self):
        """String representation of a Digraph object."""
        res = ''
        for k in self.edges:
            for d in self.edges[k]:
                res = res + str(k) + '->' + str(d) + ' distance of ' + str(k.computeDistance(d)) + '\n'
        return res[:-1]


def buildGraph(numberOfCustomers, numberOfDepots, maxDistance, timeWindows, explorationTime=5):  # TODO : maxDistance should be an attribute of graph ?
    """Builds graph g with user-defined parameter values and random positions for nodes : customers and depots.
    We create dummy vertices to allow for self-loops is the duplication of depots."""

    g = Digraph()

    customers = []
    for i in range(1, numberOfCustomers+1):
        x = random.random() * maxDistance  # square of dimensions maxDistance*maxDistance
        y = random.random() * maxDistance
        name = str(i)
        customers.append(Node(name, x, y, explorationTime))

    depots = []
    # first we add the central depot named "0"
    # and depot named "numberOfCustomers + 1" its corresponding virtual depot for self-loops paths
    timeWindowsIdx = 0
    x = random.random() * maxDistance
    y = random.random() * maxDistance
    #depots.append(Node(str(0), x, y, -1))
    depots.append(Node(str(0), x, y, -1, timeWindows[timeWindowsIdx]))
    depots.append(Node(str(numberOfCustomers + 1), x, y, -1, timeWindows[timeWindowsIdx]))

    name = numberOfCustomers + 2  # names of the real depots other than the central depot
    for i in range(numberOfCustomers+2, numberOfCustomers + numberOfDepots+1):
        timeWindowsIdx += 1
        x = random.random() * maxDistance  # square of dimensions maxDistance*maxDistance
        y = random.random() * maxDistance
        depots.append(Node(str(name), x, y, -1, timeWindows[timeWindowsIdx]))  # -1 indicates no service time for the depot
        depots.append(Node(str(name+1), x, y, -1, timeWindows[timeWindowsIdx]))  # we duplicate each depot
        name += 2

    # generation of a graph allowing the exploration of the complete graph and also the self circuits
    nodes = customers + depots
    for node in nodes:
        g.addNode(node)

    depotsListForGraphExploration = g.getRealDepots()
    depotsListForSelfLoops = g.getOtherDepots()

    for customer in customers:  # first, we make a directed clique with the customers set
        for other in customers:
            if customer != other:
                g.addEdge(Arc(customer, other))

    for depot in depotsListForGraphExploration:  # then we add the edges for the graph exploration
        for customer in customers:
            g.addEdge(Arc(depot, customer))
            g.addEdge(Arc(customer, depot))
        for other in depotsListForGraphExploration:
            if depot != other:
                g.addEdge(Arc(depot, other))

    for depot in depotsListForSelfLoops:  # finally we add the edges to allow for self circuits
        for customer in customers:
            g.addEdge(Arc(depot, customer))

        # index corresponding to the associated depot for graph exploration
        correspondingDepotIdx = g.getOtherDepots().index(depot)

        g.addEdge(Arc(depot, g.getRealDepots()[correspondingDepotIdx]))

    g.distanceMatrix = [[node.computeDistance(otherNode) for otherNode in g.getNodes()] for node in g.getNodes()]

    return g
