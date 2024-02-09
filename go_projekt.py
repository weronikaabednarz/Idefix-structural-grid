import random
import math
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def draw(self, ax):
        ax.scatter(self.x, self.y, color = "b")

class Line:
    def __init__(self, head, tail) -> None:
        self.head = head
        self.tail = tail

    def length(self):
        return math.sqrt(math.pow(self.head.x - self.tail.x, 2) + math.pow(self.head.y - self.tail.y,2))

    def draw(self, color, ax):
        ax.plot([self.head.x, self.tail.x], [self.head.y, self.tail.y], linestyle="-", color = color, linewidth=0.5)

class Triangle:

    def __init__(self, A, B, C) -> None:
        self.A = A
        self.B = B
        self.C = C
        self.points = {A,B,C}
        self.edges = {Line(A,B), Line(A,C), Line(B,C)}

    def draw(self, color, ax):
        Line(self.A, self.B).draw(color, ax)
        Line(self.A, self.C).draw(color, ax)
        Line(self.B, self.C).draw(color, ax)

    def orientationCheck(self):
        AC = [self.C.x - self.A.x, self.C.y - self.A.y]
        AB = [self.B.x - self.A.x, self.B.y - self.A.y]
        v = AC[0] * AB[1] - AB[0] * AC[1]
        return v

    def inCircumCircle(self, point):
        matrix = np.array([[math.pow(point.x,2)+math.pow(point.y,2), point.x, point.y, 1],
                           [math.pow(self.A.x,2)+math.pow(self.A.y,2), self.A.x, self.A.y, 1],
                           [math.pow(self.B.x,2)+math.pow(self.B.y,2), self.B.x, self.B.y, 1],
                           [math.pow(self.C.x,2)+math.pow(self.C.y,2), self.C.x, self.C.y, 1]])
        
        det = np.linalg.det(matrix)

        if self.orientationCheck() > 0:
            return det > 0
        else:
            return det < 0
    
    def connectedToSuperTriangle(self, super_triangle):
        for t in self.points:
            for st in super_triangle.points:
                if t == st:
                    return True
        return False

def QuadTree(img,xStart, xFinish, width, yStart, yFinish, height):
    middleX = xStart+width//2
    middleY = yStart + height//2
    global ax1

    def sprawdzenie(xPoczatek, xKoniec, yPoczatek,yKoniec):
        white = 0
        black = 0
        for i in range (xPoczatek,xKoniec):
            for j in range (yPoczatek, yKoniec):
                if img[i, j][0] == 0:
                    black += 1
                elif img[i, j][0] == 255:
                    white += 1
            if white > 40 and black > 40:
                QuadTree(img,xPoczatek, xKoniec, width//2, yPoczatek, yKoniec, height//2)
                break
            else:
                ax1.plot([xStart,xFinish],[yFinish,yStart], color = "palevioletred", linewidth=0.5)
                ax1.plot([xStart,middleX],[middleY,yStart], color = "palevioletred", linewidth=0.5)
                ax1.plot([middleX,xFinish],[yFinish,middleY], color = "palevioletred", linewidth=0.5)

    if width > 20 and height > 20:
        sprawdzenie(xStart, middleX, yStart,middleY)
        sprawdzenie(middleX, xFinish, yStart,middleY)
        sprawdzenie(xStart, middleX, middleY,yFinish)
        sprawdzenie(middleX, xFinish, middleY,yFinish)

    ax1.plot([middleX,middleX],[yStart,yFinish], color = "palevioletred", linewidth=0.7)
    ax1.plot([xStart,xFinish],[middleY,middleY], color = "palevioletred", linewidth=0.7)


def Strukturalna(plik):
    image = Image.open(plik, "r")
    ax1.imshow(image)
    img = image.load()
    QuadTree(img, 0, image.size[0], image.size[0], 0, image.size[1], image.size[1])
    ax1.title.set_text('Siatka strukturalna')

def createSuperTriangle(pointsList):
    pointsList.sort(key=lambda p: abs(p.x))
    xMax = abs(pointsList[-1].x)
    pointsList.sort(key=lambda p: abs(p.y))
    yMax = abs(pointsList[-1].y)
    if yMax > xMax:
        M = yMax*4
    else:
        M = xMax*4

    return Triangle(Point(M,0), Point(0,M), Point((-1)*M,(-1)*M))

def notSharedEdge(edge, triangleList):
    count = 0
    for triangle in triangleList:
        for e in triangle.edges:
            if (e.head == edge.head and e.tail == edge.tail) or (e.head == edge.tail and e.tail == edge.head):
                count += 1

    if count == 1:
        return True
    else:
        return False


def Delaunay (image_name, ax):
    image = Image.open(image_name, "r")
    ax2.imshow(image)
    img = image.load()

    points = []
    for x in range(0, image.size[0], 5):
        for y in range(0, image.size[1], 5):
            if img[x, y][0] == 0:
                points.append(Point(x,y))

    pointList = []
    for p in range(0,len(points)-1, 3):
        pointList.append(points[p])
        
    triangulation = []
    super_triangle = createSuperTriangle(pointList)
    triangulation.append(super_triangle)
    for point in pointList:
        badTriangles = []
        for triangle in triangulation:
            if triangle.inCircumCircle(point):
                badTriangles.append(triangle)
        polygon = []
        for triangle in badTriangles:
            for edge in triangle.edges:
                if notSharedEdge(edge, badTriangles):
                    polygon.append(edge)
        for triangle in badTriangles:
            triangulation.remove(triangle)
        for edge in polygon:
            newTri = Triangle(point, edge.head, edge.tail)
            triangulation.append(newTri)
    remove = []
    for triangle in triangulation:
        if triangle.connectedToSuperTriangle(super_triangle):
            remove.append(triangle)

    for triangle in remove:
            triangulation.remove(triangle)
    for triangle in triangulation:
        for edge in triangle.edges:
            if edge.length() > 20:
                remove.append(triangle)
    for triangle in remove:
            try:
                triangulation.remove(triangle)
            except:
                pass
    
    for triangle in triangulation:
        triangle.draw("cornflowerblue", ax)

    ax.title.set_text('Siatka niestrukturalna')

    return {"T":triangulation, "P":pointList}

def faze(t, image):
    
    img = image.load()

    if img[t.A.x, t.A.y][0] == 0 and img[t.B.x, t.B.y][0] == 0 and img[t.C.x, t.C.y] == 0:
        return 0
    else:
        return 1


def export(mesh, image):
    T = mesh['T']
    P = mesh['P']
    file = "idefix.txt"
    f = open(file,"w")
    f.write("nodes:\n")
    for i in range(len(P)-1):
        f.write("{} {} {}\n".format(i, P[i].x, P[i].y))
    f.write("\nelements:\n")
    for i in range(len(T)-1):
        f.write("{} {} {} {} {}\n".format(i, P.index(T[i].A), P.index(T[i].B), P.index(T[i].C), faze(T[i],image)))
    


if __name__ == '__main__':
    image_name = "piesek.png"
    image = Image.open(image_name, "r")
    img = image.load()
    
    global ax1, ax2
    fig, (ax1, ax2) = plt.subplots(1,2)
    points = np.genfromtxt("points.txt", delimiter=" ", usemask=True)
    
    Strukturalna(image_name)
    structural = Delaunay(image_name, ax2)
    export(structural, image)
    plt.show()