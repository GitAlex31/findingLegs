# Author : Alexandre Dossin

import graph, simplePaths, input
import random, math


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
                                           droneSpeed=droneSpeed, droneAutonomy=droneAutonomy)
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


def main():
    #test1()
    #test2()
    numberOfCustomers = 1
    numberOfDepots = 2
    if numberOfCustomers >= 1 and numberOfDepots >= 2:
        g = graph.buildGraph(numberOfCustomers, numberOfDepots, 1000)  # for testing
    else:
        raise ValueError("The network must have at least 1 customer and 2 depots.")
    #print(g)
    #allSimplePaths = simplePaths.exploreAllSimplePaths(g)
    #print([[node.getName() for node in trip] for trip in allSimplePaths])
    input.createInputFile(g, "clients.txt")
    fileName = "input0.txt"
    timeIntervals = [[0, 1440]] * numberOfDepots
    fixedCost = 10000  # if high value, the problem is the minimization of the number of vehicles
    input.createCompleteGENCOLInputFile(fileName, g, fixedCost, timeIntervals,
                                  droneSpeed=600, droneAutonomy=25, printStatistics=False)

    #input.generateGENCOLInputFiles(5, 2, 10000)

if __name__ == '__main__':
    main()