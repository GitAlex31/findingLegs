# Author : Alexandre Dossin

from tkinter import Tk, Canvas, Frame
from PIL import Image, ImageDraw
import re  # package used to do manipulate strings in a more flexible way than standard operations
import pickle

from docutils.nodes import sidebar


def solutionFileToRoutesList(g, solutionFileName):
    """Returns a list of performed routes based on the VrpGencol solution file.
     A route is defined by a sequence of nodes beginning by the Source node and ending with Destination node."""

    with open(solutionFileName, 'r') as file:
        routes = []
        copy = False
        for line in file:
            if 'Source' in line:
                copy = True
                route_aux = []  # auxiliary list for intermediate modifications
            elif 'Destination' in line:
                copy = False
                route = []
                for nodes in route_aux:
                    for node in nodes.strip().split():  # nodes.strip().split() is the list of nodes names
                        route.append(node)
                route = [node for node in route if node != ' ']
                routes.append(route)
            elif copy:
                # we remove the useless characters and keep only the node names
                if 'N' in line:
                    route_aux.append(re.sub("[^0-9]", " ", line.strip()[0:line.strip().index('[')]))
                else:
                    route_aux.append(re.sub("[^0-9]", " ", line.strip()))

    #print(routes)
    routesWithoutDuplicates = []
    for route in routes:
        zipList = list(zip(route, route[1:]))
        routeWithoutDuplicates = [name1 for name1,name2 in zipList if name1 != name2] + [route[-1]]
        routesWithoutDuplicates.append(routeWithoutDuplicates)

    #print(routesWithoutDuplicates)
    routesWithoutDuplicates = [[g.getNode(name) for name in route] for route in routes]
    return routesWithoutDuplicates

# Tk is the main window
# A frame is a container
# A canvas is a window on which we draw shapes

class Window(Frame):
    """Window is inherited from Frame which contains other widgets"""
    def __init__(self, parent, g, solutionFileName):
        Frame.__init__(self, parent)  # we initialize the Frame object
        # then the attributes and methods of Window object
        self.parent = parent
        self.customers = g.getCustomers()
        self.depots = g.getRealDepots()
        self.solutionFileName = solutionFileName
        self.initUI(g)  # fill the Window object with what we want

    def initUI(self, g):
        """Fills the Window with what we want"""
        self.parent.title("Routes")  # name of the main window
        self.pack(fill='both', expand=1)  # pack the Window in the main widget
        canvas = Canvas(self)  # a canvas is a widget on which we draw shapes

        # PIL create an empty image and draw object to draw on
        # memory only, not visible
        image = Image.new("RGB", (1100, 600), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)

        # customers are represented by circles, depots by squares
        for customer in self.customers:
            x = customer.getCoordinates()[0] / 2
            y = customer.getCoordinates()[1] / 2

            size = 10  # size of the circles
            canvas.create_oval(x, y, x + size, y + size)
            draw.ellipse((x, y, x + size, y + size), outline=(0, 0, 0))

        for depot in self.depots:
            x = depot.getCoordinates()[0] / 2
            y = depot.getCoordinates()[1] / 2
            size = 10  # size of the circles

            if depot.getName() == '0':  # special case for the central depot
                canvas.create_rectangle(x, y, x + size, y + size, fill='blue')
                draw.rectangle((x, y, x + size, y + size), outline=(0, 0, 0), fill=(0, 0, 255))
            else:
                canvas.create_rectangle(x, y, x + size, y + size)
                draw.rectangle((x, y, x + size, y + size), outline=(0, 0, 0))


        routes = solutionFileToRoutesList(g, self.solutionFileName)  # we get the routes from the solution file

        colors = ['black', 'red', 'green', 'blue', 'cyan', 'yellow', 'magenta']
        colorsPIL = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 255, 0), (255, 0, 255)]

        for colorIdx, route in enumerate(routes):  # we then draw the routes on the canvas
            for i in range(len(route)-1):
                coordinates1 = tuple(i / 2 + 5 for i in route[i].getCoordinates())
                coordinates2 = tuple(i / 2 + 5 for i in route[i+1].getCoordinates())
                canvas.create_line(coordinates1, coordinates2, arrow='last', fill=colors[colorIdx])
                coordinatesPIL = coordinates1 + coordinates2
                draw.line(coordinatesPIL, width=1, fill=colorsPIL[colorIdx])
                
        canvas.pack(fill='both', expand=1, padx=70)  # packing of the canvas in the Window object
        # padx translates the canvas to the right

        # PIL image can be saved as .png .jpg .gif or .bmp file (among others)
        filename = "my_drawing.jpg"
        image.save(filename)

if __name__ == '__main__':
    VrpGencolSolutionFileName = input("Please enter VrpGencol solution file name :")
    VrpGencolSolutionFileName = "../input/" + VrpGencolSolutionFileName
    g = pickle.load(open("../temp/graph.p", "rb"))

    root = Tk()  # top level widget in TkInter
    try:
        window = Window(root, g, VrpGencolSolutionFileName)  # creation of the window in the top level widget root
    except FileNotFoundError:
        print("File not present. Please enter again the file.")
    root.geometry("1100x600+300+100")  # geometry and position of the root widget
    root.mainloop()
