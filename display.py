# Author : Alexandre Dossin

from tkinter import Tk, Canvas, Frame, BOTH
import re


def solutionFileToRoutesList(g, solutionFileName):
    """Returns the list of performed routes based on the GENCOL solution file.
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
                    for node in nodes.strip():
                        route.append(node)
                route = [node for node in route if node != ' ']
                routes.append(route)
            elif copy:
                route_aux.append(re.sub("[^0-9]", " ", line.strip()))  # we remove the useless characters

    routes = [[g.getNode(name) for name in route] for route in routes]

    return routes

# Tk is the main window
# A frame is a container
# A canvas is an window on which we draw shapes

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
            x = customer.getCoord()[0] / 2
            y = customer.getCoord()[1] / 2
            #print(x, y)
            size = 10
            canvas.create_oval(x, y, x + size, y + size)

        for depot in self.depots:
            x = depot.getCoord()[0] / 2
            y = depot.getCoord()[1] / 2
            print(x, y)
            size = 10
            if depot.getName() == '0':
                canvas.create_rectangle(x, y, x + size, y + size, fill='blue')
            else:
                canvas.create_rectangle(x, y, x + size, y + size)


        route = solutionFileToRoutesList(g, self.solutionFileName)[0]
        print(route)

        #canvas.create_line(15, 25, 200, 25)
        #canvas.create_line(300, 35, 300, 200, dash=(4, 2))
        #canvas.create_line((55, 85), (155, 85), (105, 180), (55, 85))
        for i in range(len(route)-1):
            canvas.create_line(tuple(i / 2 + 5 for i in route[i].getCoord()), tuple(i / 2 + 5 for i in route[i+1].getCoord()), arrow='last')

        canvas.pack(fill=BOTH, expand=1)

def displayRoutes(g, solutionFileName):
    """Creates a TkInter display with customers, depots and routes."""
    pass
