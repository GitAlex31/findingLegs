# Author : Alexandre Dossin
import math, random

"""graph.py contains the classes implementation"""

class Node(object):
    def __init__(self, name, x, y, serviceTime=0):
        """A node has 4 attributes : its name, coordinates x and y, and a service time"""
        self.name = name
        self.x = x
        self.y = y
        self.serviceTime = serviceTime

    def getName(self):
        return self.name
    def getServiceTime(self):
        return self.serviceTime
    def getCoord(self):
        return (self.x, self.y)

    def computeDist(self, other):
        """Returns the euclidian distance between two node"""
        return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))

    def __str__(self):
        return "Node " + self.name + " with coordinates " + "(" + str(int(self.x)) + "," + str(int(self.y)) + ")"

    def __lt__(self, other):
        return int(self.getName()) < int(other.getName())

    def __ge__(self, other):
        return int(self.getName()) >= int(other.getName())


class Edge(object):
    def __init__(self, src, dest):
        """An edge has two attributes : its source and destination nodes"""
        self.src = src
        self.dest = dest
        self.dist = Node.computeDist(self.src, self.dest)  # the distance is computed internally

    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def getDist(self):
        return self.dist

    def __str__(self):
        return str(self.src) + '->' + str(self.dest) + ' of distance ' + str(self.dist)

class Path(object):
    def __init__(self, nodesList):
        """A path consist in an order list of nodes. The origin and destination nodes are not necessarily depots."""
        self.nodesList = nodesList

    def computeLength(self, speed):
        """Returns the length of the path, without counting the service time of the origin nor destination nodes."""
        length = 0
        for i in range(len(self.nodesList[:-1])):
            if i != 0:
                length += self.nodesList[i].getServiceTime()
            length += float(self.nodesList[i].computeDist(self.nodesList[i + 1])) / speed
        return length


class Digraph(object):

    def __init__(self):
        """A digraph has got an set of nodes and a dictionary of edges, in the form of an adjacency list"""
        self.nodes = set([])  # a set in Python is an unordered collection of unique elements
        self.edges = {}

    def addNode(self, node):
        """Adds node to the set of nodes and an empty list to the dictionary of edges with node key """
        if node.getName() in self.nodes:
            raise ValueError('Duplicate node')  # verify if the node is not already in the nodes set
        else:
            self.nodes.add(node)
            self.edges[node] = []

    def addEdge(self, edge):
        """Adds edge of source src and destination dest in the edges dictionary in the form of an adjacency list"""
        src = edge.getSource()
        dest = edge.getDestination()
        if not (src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')  # verify if both source and dest are in the node set
        self.edges[src].append(dest)

    def childrenOf(self, node):
        """Returns the list of the children of node"""
        return self.edges[node]

    def hasNode(self, node):
        """Returns True if node is in the set of nodes"""
        return node in self.nodes

    def getNode(self, idx):
        """Returns node named idx if present in nodes set"""
        idx = str(idx)  # str conversion to provide a working comparison
        list_aux = [node for node in self.nodes if node.getName() == idx]
        if list_aux == []:
            raise ValueError("Node not present in list of nodes")
        else:
            return list_aux[0]

    def getNodes(self):
        """Returns the list of nodes, either a customer or a depot"""
        return self.nodes

    def getCustomers(self):
        """Returns the sorted list of nodes that represent customers, i.e. have a service time different from -1"""
        return sorted([node for node in self.nodes if node.getServiceTime() != -1])

    def getDepots(self):
        """Returns the list of nodes that represent depots, i.e. have a service time of -1"""
        return [node for node in self.nodes if node.getServiceTime() == -1]

    def getRealDepots(self):
        """Returns the list of real depots"""
        sortedDepotsList = sorted(self.getDepots())
        return [depot for depot in sortedDepotsList if sortedDepotsList.index(depot) % 2 == 0]

    def getOtherDepots(self):
        """Returns the list of virtual depots used for self-loops paths"""
        sortedDepotsList = sorted(self.getDepots())
        return [depot for depot in sortedDepotsList if sortedDepotsList.index(depot) % 2 != 0]

    def __str__(self):
        """String representation of a Digraph object"""
        res = ''
        for k in self.edges:
            for d in self.edges[k]:
                res = res + str(k) + '->' + str(d) + ' distance of ' + str(k.computeDist(d)) + '\n'
        return res[:-1]


def buildGraph(numberOfCustomers, numberOfDepots, maxDistance, explorationTime=5):  # TODO : maxDistance should be an attribute of graph
    """Build graph g with user-defined parameter values and random positions for nodes.
    Trick used to allow for self-loops is the duplication of depots."""  # TODO : in fact the whole function should be in the class ?

    g = Digraph()

    customers = []
    for i in range(1, numberOfCustomers+1):
        x = random.random() * maxDistance  # square of dimensions maxDistance*maxDistance
        y = random.random() * maxDistance
        name = str(i)
        customers.append(Node(name, x, y, explorationTime))

    depots = []

    # first we add the central depot named "0"
    # and depot named "numberOfCustomers + 1" its corresponding depot for self-loops paths
    x = random.random() * maxDistance
    y = random.random() * maxDistance
    depots.append(Node(str(0), x, y, -1))
    depots.append(Node(str(numberOfCustomers + 1), x, y, -1))

    name = numberOfCustomers + 2  # names of the real depots other than the central depot
    for i in range(numberOfCustomers+2, numberOfCustomers + numberOfDepots+1):
        x = random.random() * maxDistance  # square of dimensions maxDistance*maxDistance
        y = random.random() * maxDistance
        depots.append(Node(str(name), x, y, -1))  # the depot has no exploration time : so -1 by default
        depots.append(Node(str(name+1), x, y, -1))  # we duplicate each depot
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
                g.addEdge(Edge(customer, other))

    for depot in depotsListForGraphExploration:  # then we add the edges for the graph exploration
        for customer in customers:
            g.addEdge(Edge(depot, customer))
            g.addEdge(Edge(customer, depot))
        for other in depotsListForGraphExploration:
            if depot != other:
                g.addEdge(Edge(depot, other))

    for depot in depotsListForSelfLoops:  # finally we add the edges to allow for self circuits
        for customer in customers:
            g.addEdge(Edge(depot, customer))

        # index corresponding to the associated depot for graph exploration
        correspondingDepotIdx = g.getOtherDepots().index(depot)

        g.addEdge(Edge(depot, g.getRealDepots()[correspondingDepotIdx]))

    return g
