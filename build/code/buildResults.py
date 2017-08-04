# Author : Alexandre Dossin

import matplotlib.pyplot as plt

def buildResultsDictionary(reportFileName):
    """Build the dictionary of results for a single VrpGencol report file named reportFileName."""
    results = dict()

    with open("../input/" + reportFileName, 'r') as reportFile:

        for line in reportFile:
            if "Best feasible solution" in line:
                idx1 = line.index(":")
                idx2 = line.index("(")
                bestFeasibleSolution = int(float(line[idx1 + 1:idx2].strip()))
                results['opt'] = bestFeasibleSolution
            elif "Number of vehicles used" in line and "maximum capacity" not in line:
                idx = line.index("=")
                numberOfVehicles = line[idx + 1:-1].strip()
                results['n_v'] = numberOfVehicles
            elif "Entire solving process" in line:
                idx1 = line.index("Time")
                idx2 = line.index(")")
                entireTime = line[idx1 + 4:idx2].strip()
                results['time'] = entireTime
            elif "Best relaxation cost" in line:
                idx1 = line.index(":")
                idx2 = line.index("(")
                bestRelaxationCost = line[idx1 + 1:idx2].strip()
                results['lr'] = bestRelaxationCost
            elif "Nodes" in line:
                idx1 = line.index(":")
                numberOfNodes = line[idx1+1:-1].strip()
                results['nodes'] = numberOfNodes
            elif "Arcs" in line:
                idx1 = line.index(":")
                numberOfArcs = line[idx1+1:-1].strip()
                results['arcs'] = numberOfArcs

    return results


def buildAllResultsDictionary(reportFileNameList):
    """Returns the dictionary containing the dictionaries of results for each
    report in the VrpGencol report list given."""
    allResults = dict()

    for reportFileName in reportFileNameList:
        allResults[reportFileName] = buildResultsDictionary(reportFileName)

    return allResults

def printLaTeXSubTable(reportFileNameList):
    """Print the necessary lines of the LaTeX subtable (to integrate in the main table) for quick copy-paste."""
    numberOfCustomers = 10
    for reportFileName in reportFileNameList:
        reportResults = buildResultsDictionary(reportFileName)
        numberOfNodes = reportResults['nodes']
        numberOfArcs = reportResults['arcs']
        optimalSolution = reportResults['opt']
        numberOfVehicles = reportResults['n_v']
        runningTime = reportResults['time']
        linearSolution = reportResults['lr']
        print("\cline{2-7}")
        print("& {} & {} & {} & {} ({}) & {} & {}\\\\".format(numberOfCustomers, numberOfNodes, numberOfArcs,
                                                             optimalSolution, numberOfVehicles, runningTime,
                                                             linearSolution))
        numberOfCustomers += 5
    pass

def plotResults(reportFileNameList, yVar, xVar):
    """Plot the results on a graph with y and x variables specified, e.g. time against number of customers"""
    pass

if __name__ == '__main__':
    #reportFileName = input("Please enter VrpGencol report file name :")
    print("ATTENTION : bien classer les fichiers report dans l'ordre croissant des clients.")
    reportList = ['reportVrp17_5_tight60_s15_a60_as.out', 'reportVrp18_5_tight60_s15_a60_as.out']
    #buildResultsDictionary(reportFileName)
    #print(buildAllResultsDictionary(reportList))
    printLaTeXSubTable(reportList)

