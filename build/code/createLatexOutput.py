# Author : Alexandre Dossin


def createLatexOutputResults(reportFileName):
    """Creates a LaTeX table with relevant parameters based on the reading of the report file."""

    # we save the relevant parameters in variables
    idx1 = reportFileName.index("Vrp")
    idx2 = reportFileName.index(".out")
    instanceName = reportFileName[idx1:idx2]
    with open(reportFileName, 'r') as reportFile:  # with open automatically closes the file when not used anymore

        bestFeasibleSolution = 0
        numberOfVehicles = 0
        entireTime = 0
        bestRelaxationCost = 0

        for line in reportFile:
            if "Best feasible solution" in line:
                idx1 = line.index(":")
                idx2 = line.index("(")
                bestFeasibleSolution = str(int(float(line[idx1+1:idx2].strip())))
            elif "Number of vehicles used" in line and "maximum capacity" not in line:
                idx = line.index("=")
                numberOfVehicles = line[idx+1:-1].strip()
            elif "Entire solving process" in line:
                idx1 = line.index("Time")
                idx2 = line.index(")")
                entireTime = line[idx1+4:idx2].strip()
            elif "Best relaxation cost" in line:
                idx1 = line.index(":")
                idx2 = line.index("(")
                bestRelaxationCost = line[idx1+1:idx2].strip()

        parametersList = [instanceName, bestFeasibleSolution, numberOfVehicles, entireTime, bestRelaxationCost]

    # we create the LaTeX table here
    latexTable = str()
    latexTable += "begin{tabular}{|c|c|c|c|}"
    latexTable += "\n\hline\n"
    latexTable += r"Instance & Optimum(Number of Vehicles) & Time & Best Relaxation Solution \\"
    latexTable += "\n\hline\n"
    latexTable += r"{} & {}({}) & {} & {} \\".format(*parametersList)
    latexTable += "\n\hline\n"
    latexTable += "end{tabular}"

    #print(latexTable)
    return latexTable


if __name__ == '__main__':
    reportFileName = input("Please enter VrpGencol report file name :")
    reportFileName = "../input/" + reportFileName
    createLatexOutputResults(reportFileName)
