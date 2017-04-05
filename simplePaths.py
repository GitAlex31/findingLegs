
def exploreSimplePaths(g, s, t, currentPath=[], simplePaths=[], droneSpeed=600, droneAutonomy=25, toPrint=False):
    """Function that returns the list of all simple paths between node named s and node named t in graph g."""

    node_s = g.getNode(s)  # we get the node object from its name
    node_t = g.getNode(t)

    currentPath.append(node_s)  # we add the current node to the current path

    usedCapacity = 0  # we reset at each call of the function the used capacity to avoid numerical errors

    # we then compute again the used capacity even if not in an optimal way
    for i in range(len(currentPath[:-1])):
        if i != 0:
            usedCapacity += currentPath[i].getServiceTime()
        usedCapacity += currentPath[i].computeDist(currentPath[i+1]) / droneSpeed

    # base case of the recursion algorithm : the beginning node is the end node
    if node_s == node_t:
        currentPathCopy = currentPath[:]
        simplePaths.append(currentPathCopy)
        return

    else:
        for v in g.childrenOf(node_s):
            # if the node is not already visited and that the drone can reach to the end node after
            # and if the node is not a new depot
            if v not in currentPath \
                    and usedCapacity + (float(node_s.computeDist(v)) / droneSpeed) + v.getServiceTime() <= droneAutonomy\
                    and not (v.getServiceTime() == -1 and v != node_t):
                # recursion
                exploreSimplePaths(g, v.getName(), node_t.getName(), currentPath, simplePaths, droneSpeed, toPrint)
                # backtracking
                currentPath.pop()

    if toPrint:  # print option
        #print("Current Path :")
        #print([node.getName() for node in currentPath])
        print("Simple Paths : ")
        print([[node.getName() for node in trip] for trip in simplePaths])
        #for idx in range(len(g.nodes)):
        #   for idx2 in range(idx):
        #       idx_node = g.getNode(idx)
        #       idx2_node = g.getNode(idx2)
        #       dist = idx_node.computeDist(idx2_node)
        #       print("Distance between {} and {} is {}".format(idx_node, idx2_node, dist))
        #print("Current used capacity :")
        #print(usedCapacity)

    return simplePaths

def exploreAllSimplePaths(g, droneSpeed=600, droneAutonomy=25, toPrint=False):
    """Returns the list of all simple paths between depots in graph g, 
    with a drone speed of 600 m/min and an autonomy of 25 min by default.
    toPrint option True displays some statistics (not working yet)"""

    depots = g.getDepots()

    allSimplePaths = []

    for depot in depots:
        for other in depots:
            if depot != other:

                allSimplePaths.extend(exploreSimplePaths(g, depot.getName(), other.getName(),
                                                         [], [], droneSpeed, droneAutonomy, toPrint))
    return allSimplePaths
