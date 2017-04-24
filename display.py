# Author : Alexandre Dossin

from tkinter import Tk, Canvas, Frame, BOTH

# Tk is the main window
# A frame is a container
# A canvas is an window on which we draw shapes

def solutionFileNameToRoute(g, solutionFileName):
    """Returns the list of performed routes based on the solution file.
     A route is defined by a sequence of nodes beginning by the Origin node, ending with the Destination node."""
    with open(solutionFileName) as file:
        routesList = []

    pass


class Window(Frame):

    def __init__(self, parent, g, solutionFileName):
        Frame.__init__(self, parent)

        self.parent = parent
        self.customers = g.getCustomers()
        self.depots = g.getRealDepots()
        self.solutionFileName = solutionFileName
        self.initUI()

    def initUI(self):
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
            #print(x, y)
            size = 10
            canvas.create_rectangle(x, y, x + size, y + size)



        #canvas.create_line(15, 25, 200, 25)
        #canvas.create_line(300, 35, 300, 200, dash=(4, 2))
        #canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85)

        canvas.pack(fill=BOTH, expand=1)

def displayRoutes(g, solutionFileName):
    """Creates a TkInter display with customers, depots and routes."""
    pass
