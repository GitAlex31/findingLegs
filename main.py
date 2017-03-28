import graph, simplePaths
import random

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
    """Simulation of the enumeration of all the simple paths in a graph with realistic parameter values"""
    nodes = []
    numberOfCustomers = 4
    maxDistance = 1000  # in meters
    explorationTime = 5  # in minutes
    droneSpeed = 600  # in m/min

    for name in range(numberOfCustomers):
        x = random.random() * maxDistance  # square of dimensions maxDistance*maxDistance
        y = random.random() * maxDistance
        nodes.append(graph.Node(str(name), x, y, explorationTime))
    g = graph.Digraph()
    for n in nodes:
        g.addNode(n)

    # generation of a complete graph
    for node in nodes:
        for other in nodes:
            if node != other:
                g.addEdge(graph.Edge(node, other))

    paths = simplePaths.exploreSimplePaths(g, 0, numberOfCustomers - 1, droneSpeed=droneSpeed, toPrint=True)
    #print("Simple paths : ", [[node.getName() for node in trip] for trip in paths])


def main():
    #test1()
    test2()

if __name__ == '__main__':
    main()