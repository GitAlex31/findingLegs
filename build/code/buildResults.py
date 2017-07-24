# Author : Alexandre Dossin

import matplotlib.pyplot as plt

def buildResultsDictionary(reportFileName):
    """Build the dictionary of results for a single VrpGencol report file named reportFileName"""

    results = dict()  # initialization of the dictionary of results

    # we save the relevant parameters in variables

    # with open automatically closes the file when not used anymore
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

    return results


def buildAllResultsDictionary(reportFileNameList):
    """Returns the dictionary containing the dictionaries of results for each
    report in the VrpGencol report list given."""
    allResults = dict()

    for reportFileName in reportFileNameList:
        allResults[reportFileName] = buildResultsDictionary(reportFileName)

    return allResults

def plotResults(reportFileNameList, yVar, xVar):
    """Plot the results on a graph with y and x variables specified, e.g. time against number of customers"""
    pass


if __name__ == '__main__':
    #reportFileName = input("Please enter VrpGencol report file name :")
    reportList = ['reportVrp50_2_tight15_as.out']
    #buildResultsDictionary(reportFileName)
    #print(buildAllResultsDictionary(reportList))

