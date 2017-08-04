# Author : Alexandre Dossin

from tkinter import Tk, Canvas, Frame
#from PIL import Image, ImageDraw
import subprocess
import re  # package used to do manipulate strings in a more flexible way than standard operations
import pickle  # package used to save the generated graph in a binary file

from docutils.nodes import sidebar


def solutionFileToRoutesList(g, solutionFileName):
    """Return a list of performed routes based on the VrpGencol solution file.
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
        routeWithoutDuplicates = [name1 for name1, name2 in zipList if name1 != name2] + [route[-1]]
        routesWithoutDuplicates.append(routeWithoutDuplicates)

    #print(routesWithoutDuplicates)
    routesWithoutDuplicates = [[g.getNode(name) for name in route] for route in routes]
    return routesWithoutDuplicates

# Tk is the main window
# A frame is a container
# A canvas is a window on which we draw shapes

class Window(Frame):
    """Window is inherited from Frame which contains other widgets"""
    def __init__(self, parent, solutionFileName, scaling=10):
        Frame.__init__(self, parent)  # we initialize the Frame object
        # then the attributes and methods of Window object
        self.parent = parent
        self.solutionFileName = solutionFileName
        self.customers = self.getGraph(solutionFileName).getCustomers()
        self.depots = self.getGraph(solutionFileName).getRealDepots()
        self.initUI(scaling)  # fill the Window object with the nodes and the routes

    def getGraph(self, solutionFileName):
        """Returns the graph corresponding to the solution file."""
        solutionFileName = solutionFileName[10:]  # get rid of the directory path
        idx1 = solutionFileName.index("Vrp") + 3
        idx2 = solutionFileName.index("tight") - 1
        numberList = solutionFileName[idx1:idx2].split("_")
        numberOfCustomers, numberOfDepots = numberList[0], numberList[1]
        g = pickle.load(
            open("../temp/graph{}_{}_5000.p".format(numberOfCustomers, numberOfDepots), "rb"))  # TODO : to generalize
        return g


    def initUI(self, scaling):
        """Fills the Window with the nodes and the routes."""
        self.parent.title("Routes")  # name of the main window
        self.pack(fill='both', expand=1)  # pack the Window in the main widget
        canvas = Canvas(self)  # a canvas is a widget on which we draw shapes

        # # PIL create an empty image and draw object to draw on
        # # memory only, not visible
        # image = Image.new("RGB", (1100, 600), color=(255, 255, 255))
        # draw = ImageDraw.Draw(image)

        # customers are represented by circles, depots by squares
        for customer in self.customers:
            x = customer.getCoordinates()[0] / scaling
            y = customer.getCoordinates()[1] / scaling

            size = 10  # size of the circles
            canvas.create_oval(x, y, x + size, y + size)
            #draw.ellipse((x, y, x + size, y + size), outline=(0, 0, 0))

        for depot in self.depots:
            x = depot.getCoordinates()[0] / scaling
            y = depot.getCoordinates()[1] / scaling
            size = 10  # size of the circles

            if depot.getName() == '0':  # special case for the central depot
                canvas.create_rectangle(x, y, x + size, y + size, fill='blue')
                #draw.rectangle((x, y, x + size, y + size), outline=(0, 0, 0), fill=(0, 0, 255))
            else:
                canvas.create_rectangle(x, y, x + size, y + size)
                #draw.rectangle((x, y, x + size, y + size), outline=(0, 0, 0))

        routes = solutionFileToRoutesList(self.getGraph(self.solutionFileName), self.solutionFileName)  # we get the routes from the solution file

        colors = ['black', 'red', 'green', 'blue', 'cyan', 'yellow', 'magenta', 'gold', 'orange', 'dark orange',
                  'coral', 'light coral', 'tomato', 'orange red', 'hot pink', 'deep pink', 'pink', 'light pink',
                  'pale violet red', 'maroon', 'medium violet red', 'violet red', 'medium orchid', 'dark orchid',
                  'dark violet', 'blue violet', 'purple', 'medium purple', 'powder blue', 'pale turquoise',
                  'dark turquoise', 'medium turquoise', 'turquoise', 'azure', 'alice blue', 'lavender',
                  'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'dark salmon', 'salmon',
                  'light salmon']
        #colorsPIL = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 255, 0), (255, 0, 255)]

        for colorIdx, route in enumerate(routes):  # we then draw the routes on the canvas
            for i in range(len(route)-1):
                coordinatesCentralDepot = tuple(i / scaling + 5 for i in route[0].getCoordinates())
                coordinates1 = tuple(i / scaling + 5 for i in route[i].getCoordinates())
                coordinates2 = tuple(i / scaling + 5 for i in route[i+1].getCoordinates())
                canvas.create_line(coordinates1, coordinates2, arrow='last', fill=colors[colorIdx])
                # coordinatesPIL = coordinates1 + coordinates2
                # draw.line(coordinatesPIL, width=1, fill=colorsPIL[colorIdx])

                # we draw the arc from the last intermediate depot to the central depot (named Destination)
                if (i == len(route) - 2) and route[i+1] != route[0]:
                    canvas.create_line(coordinates2, coordinatesCentralDepot, arrow='last', fill=colors[colorIdx])

        canvas.pack(fill='both', expand=1, padx=70)  # packing of the canvas in the Window object
        # padx translates the canvas to the right

        # # PIL image can be saved as .png .jpg .gif or .bmp file (among others)
        # filename = "routes.jpg"
        # image.save(filename)

        # generating a postscript document
        canvas.update()  # what does it do ?
        print(self.solutionFileName)
        idx1 = self.solutionFileName.index("Vrp") + 3
        idx2 = self.solutionFileName.index(".out")
        routesFileNamePs = "../output/routes{}.ps".format(self.solutionFileName[idx1:idx2])
        routesFileNamePDF = "../output/routes{}.pdf".format(self.solutionFileName[idx1:idx2])
        canvas.postscript(file=routesFileNamePs, colormode='color', width=500, height=600)
        # then convert it to a pdf file
        subprocess.Popen(["ps2pdf", routesFileNamePs, routesFileNamePDF], shell=True)

if __name__ == '__main__':
    VrpGencolSolutionFileName = input("Please enter VrpGencol solution file name :")
    VrpGencolSolutionFileName = "../input/" + VrpGencolSolutionFileName

    root = Tk()  # top level widget in TkInter
    try:
        window = Window(root, VrpGencolSolutionFileName)  # creation of the window in the top level widget root
    except FileNotFoundError:
        print("File not present. Please enter again the file.")
    root.geometry("1100x600+300+100")  # geometry and position of the root widget
    root.mainloop()
