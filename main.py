import graph, simplePaths
import random, math

def timeToDist(time, speed):
    return float(time)*speed

def distToTime(dist, speed):
    return float(dist) // speed

def test1():
    """Working test of building a graph with 10 nodes with random positions in a 10*10 unit of distance square.
    A node is a site to explore after the disaster."""
    nodes = []
    numberOfCustomers = 10
    maxDistance = 10

    for name in range(numberOfCustomers):
        x = random.random() * maxDistance
        y = random.random() * maxDistance
        nodes.append(graph.Node(str(name), x, y))
    g = graph.Digraph()
    for n in nodes:
        g.addNode(n)

    #  generation of a complete graph
    for node in nodes:
        for other in nodes:
            if node != other:
                g.addEdge(graph.Edge(node, other))

    print('The graph:')
    print(g)

def test2():
    """Simulation of the enumeration of the simple paths in a graph between the first and last node 
    with realistic parameter values for drone exploration after a disaster, e.g. in Haiti.
    Here we de not account differentiate depots and customers"""
    nodes = []
    numberOfCustomers = 5
    maxDistance = 1000  # in meters
    explorationTime = 5  # in minutes
    droneSpeed = 600  # in m/min
    droneAutonomy = 25  # in minutes

    for name in range(numberOfCustomers):
        x = random.random() * maxDistance  # square of dimensions maxDistance*maxDistance
        y = random.random() * maxDistance
        nodes.append(graph.Node(str(name), x, y, explorationTime))  # all customers have a 5 minutes exploration time

    g = graph.Digraph()

    for n in nodes:
        g.addNode(n)

    # generation of a complete graph
    for node in nodes:
        for other in nodes:
            if node != other:
                g.addEdge(graph.Edge(node, other))

    paths = simplePaths.exploreSimplePaths(g, 0, numberOfCustomers - 1,
                                           droneSpeed=droneSpeed, droneAutonomy=droneAutonomy, toPrint=False)
    print("Number of customers : {}".format(numberOfCustomers))
    print("Size of the square : {} meters".format(maxDistance))
    if paths is not None:  # temporary solution for handling the case when the departure node is the destination node
        ("Number of paths : ", len(paths))
        min_nbr = min([len(path) - 2 for path in paths])
        max_nbr = max([len(path) - 2 for path in paths])
        print("Min number of clients between two depots : {}".format(min_nbr))
        print("Max number of clients between two depots : {}".format(max_nbr))
        mean = float(sum([len(path) - 2 for path in paths]))
        mean /= len(paths)
        print("Mean number of clients between two depots per leg : {}".format(mean))
        totalNumberPaths = math.factorial(numberOfCustomers - 2) * sum([1 / math.factorial(k) for k in range(numberOfCustomers - 1)])
        fracPaths = len(paths) / totalNumberPaths
        print("Fraction of used paths : {} %".format(fracPaths*100))
        print("Simple paths : ", [[node.getName() for node in trip] for trip in paths])

def buildGraph(numberOfCustomers, numberOfDepots, maxDistance, explorationTime=5):
    """Build graph g with user-defined parameter values"""

    g = graph.Digraph()

    customers = []
    for i in range(1, numberOfCustomers+1):
        x = random.random() * maxDistance  # square of dimensions maxDistance*maxDistance
        y = random.random() * maxDistance
        name = str(i)
        customers.append(graph.Node(name, x, y, explorationTime))

    depots = []
    for i in range(numberOfCustomers+1, numberOfCustomers + numberOfDepots+1):
        x = random.random() * maxDistance  # square of dimensions maxDistance*maxDistance
        y = random.random() * maxDistance
        name = str(i)
        depots.append(graph.Node(name, x, y, -1))  # the depot has no exploration time : so -1 by default

    # generation of a complete graph
    nodes = customers + depots
    for node in nodes:
        g.addNode(node)

    for node in nodes:
        for other in nodes:
            if node != other:
                g.addEdge(graph.Edge(node, other))

    return g


def main():
    #test1()
    #test2()
    g = buildGraph(2, 2, 10)  # for testing
    allSimplePaths = simplePaths.exploreAllSimplePaths(g)
    print([[node.getName() for node in trip] for trip in allSimplePaths])
    pass

if __name__ == '__main__':
    main()