# Author : Alexandre Dossin

import matplotlib.pyplot as plt
import numpy as np

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
            elif "No feasible solution was found" in line:
                results['opt'] = "N/A"
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
    """Print the necessary lines of the LaTeX sub-table (to integrate in the main table) for quick copy-paste."""
    numberOfCustomers = [10, 15, 20, 25, 30, 35]
    numberOfCustomersIdx = 0

    for reportFileName in reportFileNameList:
        reportResults = buildResultsDictionary(reportFileName)
        numberOfNodes = reportResults['nodes']
        numberOfArcs = reportResults['arcs']
        optimalSolution = reportResults['opt']
        numberOfVehicles = reportResults['n_v']
        runningTime = reportResults['time']
        linearSolution = reportResults['lr']
        print("\cline{2-7}")
        print("& {} & {} & {} & {} ({}) & {} & {}\\\\".format(numberOfCustomers[numberOfCustomersIdx],
                                                              numberOfNodes, numberOfArcs, optimalSolution,
                                                              numberOfVehicles, runningTime, linearSolution))
        numberOfCustomersIdx += 1
        if numberOfCustomersIdx == 6:
            numberOfCustomersIdx = 0
    pass

def plotResults():
    """Plot the results on a graph with y and x variables specified, e.g. time against number of customers"""

    # # Scatter plots of optimal solution with varying customers
    # x = [10, 15, 20, 25, 30, 35]
    # y_s45_tight15 = [60521, 80798, 111072, 131334, 161589, 181862]
    # y_s15_tight15 = [20174, 20267, 30360, 40441, 50525, 50615]
    # y_s45_tight60 = [20498, 30765, 41031, 51282, 61527, 71787]
    # y_s15_tight60 = [10172, 10624, 20352, 20434, 20515, 30601]
    # plot_s45_tight15 = plt.plot(x, y_s45_tight15, '-o', label="s=45, width=15")
    # plot_s15_tight15 = plt.plot(x, y_s15_tight15, '-o', label="s=15, width=15")
    # plot_s45_tight60 = plt.plot(x, y_s45_tight60, '-o', label="s=45, width=60")
    # plot_s15_tight60 = plt.plot(x, y_s15_tight60, '-o', label="s=15, width=60")
    # plt.legend()
    # plt.xlabel("Number of customers")
    # plt.ylabel("Optimal solution")
    # plt.show()

    # Scatter plots of optimal solution with varying depots
    x = [2, 3, 4, 5]
    y_s45_tight15 = [301625, 161589, 101573, 81560]
    y_s15_tight15 = [100546, 50525, 30517, 20520]
    y_s45_tight60 = [101558, 61527, 51504, 41500]
    y_s15_tight60 = [40525, 20515, 20507, 20504]
    plot_s45_tight15 = plt.plot(x, y_s45_tight15, '-o', label="s=45, width=15")
    plot_s15_tight15 = plt.plot(x, y_s15_tight15, '-o', label="s=15, width=15")
    plot_s45_tight60 = plt.plot(x, y_s45_tight60, '-o', label="s=45, width=60")
    plot_s15_tight60 = plt.plot(x, y_s15_tight60, '-o', label="s=15, width=60")
    plt.legend()
    plt.xlabel("Number of depots")
    plt.ylabel("Optimal solution")
    plt.show()

    # # Draw a pie chart for the time limit overrun
    # labels = ('over time limit', 'under time limit')
    # sizes = [3.1, 100-3.1]
    # fig1, ax1 = plt.subplots()
    # ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # plt.show()

    pass

if __name__ == '__main__':
    #reportFileName = input("Please enter VrpGencol report file name :")
    #print("ATTENTION : bien classer les fichiers report dans l'ordre croissant des clients.")
    # reportList = ['reportVrp10_2_tight15_s45_a60_as.out', 'reportVrp15_2_tight15_s45_a60_as.out',
    #               'reportVrp20_2_tight15_s45_a60_as.out', 'reportVrp25_2_tight15_s45_a60_as.out',
    #               'reportVrp30_2_tight15_s45_a60_as.out', 'reportVrp35_2_tight15_s45_a60_as.out']
    numberOfCustomers = [10, 15, 20, 25, 30, 35]
    serviceTimes = [45, 30, 20, 15]
    reportList = []
    for serviceTime in serviceTimes:
        for customer in numberOfCustomers:
            reportList += ['reportVrp{}_5_tight60_s{}_a60_p.out'.format(customer, serviceTime)]
    #print(reportList)
    #buildResultsDictionary(reportFileName)
    #print(buildAllResultsDictionary(reportList))
    #printLaTeXSubTable(reportList)
    plotResults()

