# Author : Alexandre Dossin

from tkinter import Tk, Canvas, Frame, BOTH
import re  # stands for "regular expression" operations
import pickle


def solutionFileToRoutesList(g, solutionFileName):  #TODO : not functionnal when nodes with double digits numbers
    """Returns a list of performed routes based on the GENCOL solution file.
     A route is defined by a sequence of nodes beginning by the Source node and ending with Destination node."""

    with open(solutionFileName, 'r') as file:
        routes = []
        copy = False
        for line in file:
            if 'Source' in line:
                copy = True
                route_aux = []  # auxiliary variable for easier string modification
            elif 'Destination' in line:
                copy = False
                route = []
                for nodes in route_aux:
                    for node in nodes.strip().split():  # nodes.strip().split() is the list of nodes names
                        route.append(node)
                route = [node for node in route if node != ' ']
                routes.append(route)
            elif copy:
                route_aux.append(re.sub("[^0-9]", " ", line.strip()))  # we remove the useless characters and keep only the node numbers

    routes = [[g.getNode(name) for name in route] for route in routes]

    return routes

# Tk is the main window
# A frame is a container
# A canvas is a window on which we draw shapes

class Window(Frame):

    def __init__(self, parent, g, solutionFileName):
        Frame.__init__(self, parent)

        self.parent = parent
        self.customers = g.getCustomers()
        self.depots = g.getRealDepots()
        self.solutionFileName = solutionFileName
        self.initUI(g)

    def initUI(self, g):
        self.parent.title("Routes")
        self.pack(fill=BOTH, expand=1)

        canvas = Canvas(self)

        # customers are represented by circles, depots by squares
        for customer in self.customers:
            x = customer.getCoordinates()[0] / 2
            y = customer.getCoordinates()[1] / 2

            size = 10
            canvas.create_oval(x, y, x + size, y + size)

        for depot in self.depots:
            x = depot.getCoordinates()[0] / 2
            y = depot.getCoordinates()[1] / 2
            size = 10

            if depot.getName() == '0':
                canvas.create_rectangle(x, y, x + size, y + size, fill='blue')
            else:
                canvas.create_rectangle(x, y, x + size, y + size)

        routes = solutionFileToRoutesList(g, self.solutionFileName)

        for route in routes:
            for i in range(len(route)-1):
                canvas.create_line(tuple(i / 2 + 5 for i in route[i].getCoordinates()),
                                   tuple(i / 2 + 5 for i in route[i+1].getCoordinates()), arrow='last')

        canvas.pack(fill=BOTH, expand=1)

if __name__== '__main__':
    GENCOLSolutionFileName = input("Please enter GENCOL solution file name :")
    GENCOLSolutionFileName = "../output/" + GENCOLSolutionFileName
    g = pickle.load(open("../temp/graph.p", "rb"))

    root = Tk()
    try:
        window = Window(root, g, GENCOLSolutionFileName)
    except FileNotFoundError:
        print("File not present. Please enter again the file.")
    root.geometry("800x600+300+100")
    root.mainloop()
