# Author : Alexandre Dossin

import graph
import math
import itertools

def exploreSimplePaths(g, s, t, currentPath=[], simplePaths=[], droneSpeed=600, droneAutonomy=25):
    """Function that returns the list of all simple paths between node named s and node named t in graph g.
    s and t have to be different at the beginning."""

    node_s = g.getNode(s)  # we get the node object from its name
    node_t = g.getNode(t)

    currentPath.append(node_s)  # we add the current node to the current path

    usedCapacity = 0  # we reset at each call of the function the used capacity to avoid numerical errors

    # we then compute again the used capacity even if not in an optimal way
    for i in range(len(currentPath[:-1])):
        if i != 0:
            usedCapacity += currentPath[i].getServiceTime()
        usedCapacity += float(currentPath[i].computeDist(currentPath[i+1])) / droneSpeed
    # if the last node in currentPath is not a depot, we add its service time to the used capacity
    # consider code to change if the depot have a non-negative service time
    if currentPath[-1].getServiceTime() != -1:
        usedCapacity += currentPath[-1].getServiceTime()

    # base case of the recursion algorithm : the beginning node is the end node
    if node_s == node_t:
        currentPathCopy = currentPath[:]
        simplePaths.append(currentPathCopy)
        return

    else:
        for v in g.childrenOf(node_s):

            # we first set the service time of a depot to 0
            if v.getServiceTime() == -1:
                serviceTime = 0
            else:
                serviceTime = v.getServiceTime()

            # if the node is not already visited and that the drone can reach to the end node after
            # and if the node is not a new depot different from the destination depot that is a function's argument
            if v not in currentPath \
                    and usedCapacity + (float(node_s.computeDist(v)) / droneSpeed) + serviceTime <= droneAutonomy \
                    and not (v.getServiceTime() == -1 and v != node_t):
                # recursion
                exploreSimplePaths(g, v.getName(), node_t.getName(), currentPath, simplePaths, droneSpeed, droneAutonomy)
                # backtracking
                currentPath.pop()
        pass

    #print([[node.getName() for node in path] for path in simplePaths])
    return simplePaths

def filterSimplePaths(g, simplePaths, droneSpeed=600):
    """Returns a filtered list of simple paths consisting in keeping the simple paths of least cost only, e.g. 
    keeping the simple path [1, 2, 3, 4] (say 1 and 4 are depots) instead of [1, 3, 2, 4] if the cost of that last
    path is higher than the previous one."""

    if len(g.getCustomers()) >= 2:  # the filter is useful in that case only
        customers = g.getCustomers()
        filteredSimplePaths = []
        for i in range(2, len(customers) + 1):
            targetSubsets = list(set(itertools.combinations(customers, i)))  # finds all subsets of size i of the customers set
            #print(targetSubsets)
            for targetSubset in targetSubsets:
                #print(targetSubset)
                simplePathsToFilter = [path for path in simplePaths if len(path) == i + 2 and set(targetSubset).issubset(path)]
                #print("Target Subset : ", targetSubset[0], targetSubset[1])
                #print([[node.getName() for node in path] for path in simplePathsToFilter])
                #print(simplePathsToFilter)
                #print(targetSubset)
                if simplePathsToFilter != []:
                    leastCostPath = simplePathsToFilter[0]  # initialization of the minimization small algorithm
                    leastCostPathObject = graph.Path(leastCostPath)
                    for path in simplePathsToFilter:  # we retain here the path corresponding to the minimum cost
                        pathObject = graph.Path(path)
                        if pathObject.computeLength(droneSpeed) < leastCostPathObject.computeLength(droneSpeed):
                            leastCostPath = path
                            leastCostPathObject = graph.Path(leastCostPath)

                    filteredSimplePaths.append(leastCostPath)

        return filteredSimplePaths


def exploreAllSimplePaths(g, droneSpeed=600, droneAutonomy=25, printStatistics=False):
    """Returns the list of all simple paths between depots in graph g, 
    with a drone speed of 600 m/min and an autonomy of 25 min by default.
    printStatistics option True displays some statistics"""

    allSimplePaths = []

    depotsListForGraphExploration = g.getRealDepots()
    depotsListForSelfLoops = g.getOtherDepots()

    for depot in depotsListForGraphExploration:  # simple paths between different depots
        for other in depotsListForGraphExploration:
            if depot != other:
                simplePaths = exploreSimplePaths(g, depot.getName(), other.getName(), [], [], droneSpeed, droneAutonomy)
                allSimplePaths.extend(filterSimplePaths(g, simplePaths, droneSpeed))

    for depot in depotsListForSelfLoops:
        associatedDepot = depotsListForGraphExploration[depotsListForSelfLoops.index(depot)]  # real depot associated
        simplePaths = exploreSimplePaths(g, depot.getName(), associatedDepot.getName(), [], [], droneSpeed, droneAutonomy)
        allSimplePaths.extend(filterSimplePaths(g, simplePaths, droneSpeed))

    if printStatistics:  # useful statistics about the built graph
        numberOfCustomers = len(g.getCustomers())
        numberOfDepots = len(g.getDepots())
        numberOfDepots = int(numberOfDepots / 2)  # this is the number of real depots
        print("Number of customers : {}".format(numberOfCustomers))
        print("Number of Depots : {}".format(numberOfDepots))
        print("Number of paths : ", len(allSimplePaths))
        min_nbr = min([len(path) - 2 for path in allSimplePaths])  # always 0 for because of self-loops and depot-depot simple paths
        max_nbr = max([len(path) - 2 for path in allSimplePaths])
        print("Min number of customers between two depots : {}".format(min_nbr))
        print("Max number of customers between two depots : {}".format(max_nbr))
        mean = float(sum([len(path) - 2 for path in allSimplePaths]))
        mean /= len(allSimplePaths)
        print("Mean number of customers per leg : {}".format(mean))
        # number of simple paths between any pair of depots in a directed clique, with origin and destination different
        totalNumberPaths = math.factorial(numberOfCustomers) * sum(
            [1 / math.factorial(k) for k in range(numberOfCustomers + 1)])
        # we multiply by the number of ordered pairs of depots
        totalNumberPaths *= numberOfDepots * (numberOfDepots - 1)
        # we add the simple paths due to self loops
        numberOfPathsForOneSelfLoop = math.factorial(numberOfCustomers) * sum(
            [1 / math.factorial(k) for k in range(numberOfCustomers + 1)])
        totalNumberPaths += numberOfPathsForOneSelfLoop * numberOfDepots

        print("Total possible number of paths : {}".format(totalNumberPaths))
        fracPaths = len(allSimplePaths) / totalNumberPaths
        print("Fraction of used paths : {} %".format(fracPaths * 100))

    return allSimplePaths
