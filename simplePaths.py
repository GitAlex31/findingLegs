# Author : Alexandre Dossin

import graph
import math, itertools, time, random

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
    # consider changing the code if the depot have a non-negative service time
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

    return simplePaths


def filterSimplePaths(g, simplePaths, droneSpeed=600):
    """Returns a filtered list of simple paths consisting in keeping the simple paths of least cost only, e.g. 
    keeping the simple path [1, 2, 3, 4] (say 1 and 4 are depots) instead of [1, 3, 2, 4] if the cost of that last
    path is higher than the previous one."""

    if len(g.getCustomers()) >= 2:  # the filter is useful in that case only
        customers = g.getCustomers()
        filteredSimplePaths = []  # initialization of the list containing the best simple paths between two depots
        #for i in range(2, len(customers) + 1):
        for i in range(0, 5):
            # we find all unordered subsets of the customers set
            targetSubsets = list(set(itertools.combinations(customers, i)))
            for targetSubset in targetSubsets:
                # THERE IS AN FACTORIAL NUMBER OF TARGET SUBSETS !
                simplePathsToFilter = [path for path in simplePaths if len(path) == i + 2 and set(targetSubset).issubset(path)]
                if simplePathsToFilter != []:
                    leastCostPath = simplePathsToFilter[0]  # initialization of the minimization small algorithm
                    leastCostPathObject = graph.Path(leastCostPath)
                    for path in simplePathsToFilter:  # we retain here the path corresponding to the minimum cost
                        # linear complexity in the simplePathsToFilter list
                        pathObject = graph.Path(path)
                        if pathObject.computeLength(droneSpeed) < leastCostPathObject.computeLength(droneSpeed):
                            leastCostPath = path
                            leastCostPathObject = graph.Path(leastCostPath)

                    filteredSimplePaths.append(leastCostPath)

        return filteredSimplePaths
    else:
        return simplePaths


def exploreSimplePathsNonRecursive(g, s, t, droneSpeed=600, droneAutonomy=25):  # TODO : review function performance
    """Returns the list of least cost simple paths between node named s and node named t in graph g.
    s and t have to be different at the beginning."""

    node_s = g.getNode(s)  # we get the node object from its name
    node_t = g.getNode(t)

    simplePaths = []
    customers = g.getCustomers()

    if node_s.computeDist(node_t) / droneSpeed <= droneAutonomy:  # first we build the inter-depots routes if possible
        simplePaths.append([node_s, node_t])  # without any customer

    for i, customer in enumerate(customers):  # we build legs with 1 customer only
        temporaryList = [node_s, customer, node_t]
        candidateRoute = graph.Path(temporaryList)
        candidateRouteLength = candidateRoute.computeLength(droneSpeed)

        if candidateRouteLength < droneAutonomy:

            simplePaths.append(temporaryList[:])  # we copy the list to avoid aliasing

            for j, customer2 in enumerate(customers[i+1:], start=i+1):  # now 2 customers in the route if possible

                temporaryList2 = [customer, customer2]
                permutations2 = list(itertools.permutations(temporaryList2))  # candidate routes with 2 customers
                leastCostLeg = [node_s] + list(permutations2[0]) + [node_t]  # initialization of the least cost route
                # filtering of the legs containing the same subset of customers by cost minimization
                # the autonomy of the drone has to be respected
                totalUnfeasibility2 = True
                for perm2 in permutations2:
                    legList = [node_s] + list(perm2) + [node_t]
                    legPathObject = graph.Path(legList)
                    if (legPathObject.computeLength(droneSpeed) <= graph.Path(leastCostLeg).computeLength(droneSpeed))\
                            and (legPathObject.computeLength(droneSpeed) <= droneAutonomy):
                        totalUnfeasibility2 = False
                        leastCostLeg = [node_s] + list(perm2) + [node_t]

                simplePaths.append(leastCostLeg)

                if not totalUnfeasibility2:

                    for k, customer3 in enumerate(customers[j+1:], start=j+1):  # now 3 customers in the route

                        temporaryList3 = [customer, customer2, customer3]
                        permutations3 = list(itertools.permutations(temporaryList3))  # candidate routes with 3 customers
                        leastCostLeg = [node_s] + list(permutations3[0]) + [node_t]
                        totalUnfeasibility3 = True
                        for perm3 in permutations3:
                            legList = [node_s] + list(perm3) + [node_t]
                            legPathObject = graph.Path(legList)
                            if (legPathObject.computeLength(droneSpeed) <= graph.Path(leastCostLeg).computeLength(
                                    droneSpeed)) \
                                    and (legPathObject.computeLength(droneSpeed) <= droneAutonomy):
                                totalUnfeasibility3 = False
                                leastCostLeg = [node_s] + list(perm3) + [node_t]

                        simplePaths.append(leastCostLeg)

                        if not totalUnfeasibility3:

                            for l, customer4 in enumerate(customers[k+1:], start=k+1):  # now 4 customers in the route

                                temporaryList = [customer, customer2, customer3, customer4]
                                permutations4 = list(
                                    itertools.permutations(temporaryList))  # candidate routes with 4 customers
                                leastCostLeg = [node_s] + list(permutations4[0]) + [node_t]
                                totalUnfeasibility4 = True
                                for perm4 in permutations4:
                                    legList = [node_s] + list(perm4) + [node_t]
                                    legPathObject = graph.Path(legList)
                                    if (legPathObject.computeLength(droneSpeed) <= graph.Path(
                                            leastCostLeg).computeLength(
                                            droneSpeed)) \
                                            and (legPathObject.computeLength(droneSpeed) <= droneAutonomy):
                                        totalUnfeasibility4 = False
                                        leastCostLeg = [node_s] + list(perm4) + [node_t]

                                simplePaths.append(leastCostLeg)

    return simplePaths


def exploreAllSimplePaths(g, droneSpeed=600, droneAutonomy=25, recursiveAlgorithm=False, printStatistics=False):
    """Returns the list of all simple paths between depots in graph g, 
    with a drone speed of 600 m/min and an autonomy of 25 min by default.
    printStatistics option True displays some statistics"""

    start_time = time.time()

    allSimplePaths = []

    depotsListForGraphExploration = g.getRealDepots()
    depotsListForSelfLoops = g.getOtherDepots()

    for depot in depotsListForGraphExploration:  # simple paths between different depots
        for other in depotsListForGraphExploration:
            if depot != other:
                if recursiveAlgorithm:
                    simplePaths = exploreSimplePaths(g, depot.getName(), other.getName(), [], [], droneSpeed, droneAutonomy)
                    #allSimplePaths.extend(simplePaths)
                    allSimplePaths.extend(filterSimplePaths(g, simplePaths, droneSpeed))
                else:
                    simplePaths = exploreSimplePathsNonRecursive(g, depot.getName(), other.getName(), droneSpeed,
                                                     droneAutonomy)
                    allSimplePaths.extend(simplePaths)

    for depot in depotsListForSelfLoops:

        associatedDepot = depotsListForGraphExploration[depotsListForSelfLoops.index(depot)]  # real depot associated

        if recursiveAlgorithm:
            simplePaths = exploreSimplePaths(g, depot.getName(), associatedDepot.getName(), [], [], droneSpeed, droneAutonomy)
            #allSimplePaths.extend(simplePaths)
            allSimplePaths.extend(filterSimplePaths(g, simplePaths, droneSpeed))
        else:
            simplePaths = exploreSimplePathsNonRecursive(g, depot.getName(), associatedDepot.getName(), droneSpeed,
                                             droneAutonomy)
            allSimplePaths.extend(simplePaths)

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

    print("\n Time used for generating the legs : --- {} seconds --- with {} algorithm"
          .format(time.time() - start_time, "recursive" if recursiveAlgorithm else "non-recursive"))

    return allSimplePaths

def buildTimeWindows(numberOfDepots, separatedTW=False, randomTW=False):
    """Returns time windows for depots according to different options : 
    separetedTW indicates time-windows form an equal partition of the whole day.
    randomTW provides randomly chosen time windows during the whole day."""
    timeWindows = []

    if separatedTW:
        timeStep = int(float(86400) / numberOfDepots)
        for i in range(numberOfDepots):
            timeWindows.append([timeStep * i, timeStep * (i + 1)])

    if randomTW:
        for i in range(numberOfDepots):
            a = random.randint(0, 86400)
            b = random.randint(0, 86400)
            if b >= a:
                timeWindows.append([a, b])
            else:
                timeWindows.append([b, a])

    return timeWindows