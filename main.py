import math                                 #moduł zawierający matematyczne funkcje i stałe
import numpy as np                          #biblioteka do obliczeń naukowych, w tym operacji na wielowymiarowych tablicach i macierzach
from matplotlib import pyplot as plt        #moduł do tworzenia wykresów
from PIL import Image                       #moduł do obsługi obrazów

class Point:                                #Definicja klasy Point, która reprezentuje punkt na płaszczyźnie
    def __init__(self, x, y) -> None:       #Konstruktor klasy Point przyjmuje dwie wartości x i y i przypisuje je do atrybutów self.x i self.y
        self.x = x
        self.y = y

    def draw(self, ax):
        ax.scatter(self.x, self.y, color = "b")     #Metoda draw rysuje punkt na wykresie przy użyciu obiektu ax.scatter

class Line:                                         #Definicja klasy Line, która reprezentuje odcinek pomiędzy dwoma punktami
    def __init__(self, head, tail) -> None:         #Konstruktor klasy Line przyjmuje dwa obiekty klasy Point jako punkty początkowy 
        self.head = head                            #i końcowy i przypisuje je do atrybutów self.head i self.tail
        self.tail = tail

    def length(self):                               #Metoda length oblicza długość odcinka za pomocą funkcji matematycznych
        return math.sqrt(math.pow(self.head.x - self.tail.x, 2) + math.pow(self.head.y - self.tail.y,2))

    def draw(self, color, ax):                      #Metoda draw rysuje odcinek na wykresie ax
        ax.plot([self.head.x, self.tail.x], [self.head.y, self.tail.y], linestyle="-", color = color, linewidth=0.5)

class Triangle:                                     #Definicja klasy Triangle, która reprezentuje trójkąt na płaszczyźnie

    def __init__(self, A, B, C) -> None:            #Konstruktor klasy Triangle przyjmuje trzy obiekty klasy Point jako 
        self.A = A                                  #wierzchołki A, B i C i przypisuje je do atrybutów self.A, self.B i self.C
        self.B = B
        self.C = C
        self.points = {A,B,C}                       #Tworzy także zbiory points i edges zawierające odpowiednio punkty i krawędzie trójkąta
        self.edges = {Line(A,B), Line(A,C), Line(B,C)}

    def draw(self, color, ax):                      #Metoda draw rysuje trójkąt na wykresie przez wywołanie metody draw na każdej krawędzi
        Line(self.A, self.B).draw(color, ax)
        Line(self.A, self.C).draw(color, ax)
        Line(self.B, self.C).draw(color, ax)

    def orientationCheck(self):                     #Metoda orientationCheck oblicza orientację trójkąta na podstawie współrzędnych jego wierzchołków
        AC = [self.C.x - self.A.x, self.C.y - self.A.y]
        AB = [self.B.x - self.A.x, self.B.y - self.A.y]
        v = AC[0] * AB[1] - AB[0] * AC[1]
        return v

    def inCircumCircle(self, point):                #Metoda inCircumCircle sprawdza, czy dany punkt leży w okręgu opisanym na trójkącie
        matrix = np.array([[math.pow(point.x,2)+math.pow(point.y,2), point.x, point.y, 1],
                           [math.pow(self.A.x,2)+math.pow(self.A.y,2), self.A.x, self.A.y, 1],
                           [math.pow(self.B.x,2)+math.pow(self.B.y,2), self.B.x, self.B.y, 1],
                           [math.pow(self.C.x,2)+math.pow(self.C.y,2), self.C.x, self.C.y, 1]])
        
        det = np.linalg.det(matrix)

        if self.orientationCheck() > 0:
            return det > 0
        else:
            return det < 0
    
    def connectedToSuperTriangle(self, super_triangle):     #Metoda connected.. sprawdza, czy trójkąt ma wspólny wierzchołek z trójkątem super trójkąta
        for t in self.points:
            for st in super_triangle.points:
                if t == st:
                    return True
        return False

def QuadTree(img,STARTx, ENDx, width, STARTy, ENDy, height):      #Definicja funkcji QuadTree, która implementuje algorytm QuadTree dla podanego obrazu
    MIDx = STARTx+width//2                                           #Zmienna MIDx przechowuje środkową wartość współrzędnej x, 
    MIDy = STARTy + height//2                                        #a MIDy - środkową wartość współrzędnej y
    global ax1

    def check(xPoczatek, xKoniec, yPoczatek,yKoniec):           #Funkcja wewnętrzna check sprawdza, czy obszar o podanych współrzędnych 
        white = 0                                               #zawiera zarówno czarne jak i białe piksele
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
                ax1.plot([STARTx,ENDx],[ENDy,STARTy], color = "palevioletred", linewidth=0.5)     #Jeśli tak, rekurencyjnie wywołuje funkcję QuadTree 
                ax1.plot([STARTx,MIDx],[MIDy,STARTy], color = "palevioletred", linewidth=0.5)     #dla czterech podobszarów, a jeśli nie, rysuje odcinki na
                ax1.plot([MIDx,ENDx],[ENDy,MIDy], color = "palevioletred", linewidth=0.5)         #wykresie przy użyciu obiektu ax1.plot

    if width > 20 and height > 20:          #Warunek width > 20 and height > 20 kontroluje, czy obszar jest podzielny na mniejsze obszary
        check(STARTx, MIDx, STARTy,MIDy)
        check(MIDx, ENDx, STARTy,MIDy)
        check(STARTx, MIDx, MIDy,ENDy)
        check(MIDx, ENDx, MIDy,ENDy)

    ax1.plot([MIDx,MIDx],[STARTy,ENDy], color = "palevioletred", linewidth=0.7)    #Na końcu funkcji rysuje pionowy i poziomy odcinek na wykresie
    ax1.plot([STARTx,ENDx],[MIDy,MIDy], color = "palevioletred", linewidth=0.7)


def Strukturalna(plik):                     #Definicja funkcji Strukturalna, która przyjmuje nazwę obrazu jako argument
    image = Image.open(plik, "r")           #Funkcja otwiera obraz, wczytuje go przy użyciu Image.open i przypisuje go do zmiennej image
    ax1.imshow(image)                       #Następnie używa ax1.imshow do wyświetlenia obrazu na wykresie
    img = image.load()
    QuadTree(img, 0, image.size[0], image.size[0], 0, image.size[1], image.size[1]) #Wywołuje funkcję QuadTree dla obrazu i rysuje siatkę strukturalną na wykresie
    ax1.title.set_text('Siatka strukturalna')   

def createSuperTriangle(pointsList):        #Definicja funkcji createSuperTriangle, która tworzy super trójkąt na podstawie listy punktów

    pointsList.sort(key=lambda p: abs(p.x))              #Najpierw lista punktów jest sortowana względem wartości bezwzględnej współrzędnej x lub y
    m = 3
    big = max(max(abs(p.x), abs(p.y)) for p in pointsList)  #a następnie obliczana jest wartość maksymalna dla odpowiedniej osi
    p1 = Point(m * big, 0)                                  #Na podstawie tej wartości tworzony jest trójkąt o odpowiednich współrzędnych
    p2 = Point(0, m * big)
    p3 = Point(-1 * m * big, -1 * m * big)

    return Triangle(p1, p2, p3)       #Zwracany jest obiekt klasy Triangle reprezentujący super trójkąt

def notSharedEdge(edge, triangleList):      #Definicja funkcji notSharedEdge, która sprawdza, czy krawędź nie jest współdzielona 
    count = 0                               #przez żadne inne trójkąty w liście trójkątów
    for triangle in triangleList:
        for e in triangle.edges:
            if (e.head == edge.head and e.tail == edge.tail) or (e.head == edge.tail and e.tail == edge.head):
                count += 1

    if count == 1:              #Zlicza wystąpienia krawędzi wśród trójkątów i zwraca True, jeśli 
        return True             #występuje tylko raz, a w przeciwnym przypadku False
    else:
        return False


def Delaunay (image_name, ax):          #Definicja funkcji Delaunay, która implementuje algorytm Delaunay triangulation na podstawie obrazu
    image = Image.open(image_name, "r") #Parametry: image_name - nazwa obrazu, ax - obiekt osi wykresu, Funkcja otwiera obraz, wczytuje go przy użyciu
    ax2.imshow(image)                   #Image.open i przypisuje go do zmiennej image,->używa ax2.imshow do wyświetlenia obrazu na drugim wykresie
    img = image.load()

    points = []                                         #Tworzy listę punktów na podstawie czarnych pikseli w obrazie
    for x in range(0, image.size[0], 5):                
        for y in range(0, image.size[1], 5):
            if img[x, y][0] == 0:
                points.append(Point(x,y))

    pointList = []                                      #Wybiera co trzeci punkt z listy punktów jako punkty trójkątów
    for p in range(0,len(points)-1, 3):
        pointList.append(points[p])
        
    triangulation = []
    super_triangle = createSuperTriangle(pointList)     #Tworzy super trójkąt za pomocą funkcji createSuperTriangle.
    triangulation.append(super_triangle)                #Dodaje go do listy trójkątów.
    for point in pointList:                             #Dla każdego punktu z listy punktów, znajduje trójkąty, które zawierają ten 
        badTriangles = []                               #punkt w swoim okręgu opisanym i oznacza je jako złe trójkąty.
        for triangle in triangulation:                  #Następnie tworzy listę krawędzi, które nie są współdzielone przez złe trójkąty.
            if triangle.inCircumCircle(point):          #Usuwa złe trójkąty z listy trójkątów.
                badTriangles.append(triangle)           #Dla każdej krawędzi z listy krawędzi tworzy nowy trójkąt i dodaje go do listy trójkątów.
        polygon = []                                    #Usuwa trójkąty, które są połączone z super trójkątem.
        for triangle in badTriangles:                   #Następnie usuwa trójkąty, których krawędzie mają długość większą niż 20.
            for edge in triangle.edges:                 #Na koniec rysuje trójkąty na wykresie za pomocą metody draw obiektu klasy Triangle.
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
            if edge.length() > 40:
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

def faze(t, image):                         #Definicja funkcji faze, która zwraca fazę dla danego trójkąta i obrazu.
    
    img = image.load()

    if img[t.A.x, t.A.y][0] == 0 and img[t.B.x, t.B.y][0] == 0 and img[t.C.x, t.C.y][0] == 0:
        return 0                            #Jeśli piksele wierzchołków trójkąta są czarne, zwraca 0, w przeciwnym razie zwraca 1.
    else:
        return 1


def export(mesh, image):            #Definicja funkcji export, która eksportuje wynik triangulacji do pliku tekstowego.
    T = mesh['T']                   #Parametry funkcji to: mesh - wynik triangulacji, image - obraz.
    P = mesh['P']
    file = "idefix.txt"             #Funkcja tworzy nowy plik o nazwie "idefix.txt" i zapisuje w nim informacje o węzłach i elementach
    f = open(file,"w")
    f.write("nodes:\n")
    for i in range(len(P)-1):
        f.write("{} {} {}\n".format(i, P[i].x, P[i].y))
    f.write("\nelements:\n")
    for i in range(len(T)-1):
        f.write("{} {} {} {} {}\n".format(i, P.index(T[i].A), P.index(T[i].B), P.index(T[i].C), faze(T[i],image)))
    #Węzły to punkty, a elementy to trójkąty. Każdy trójkąt ma przypisaną fazę na podstawie funkcji faze *


if __name__ == '__main__':                #Warunek sprawdzający, czy skrypt jest uruchomiony jako plik główny
    image_name = "piesek.png"           #Wczytuje obraz o nazwie "piesek.png" przy użyciu Image.open i przypisuje go do zmiennej image
    image = Image.open(image_name, "r")
    img = image.load()                  #Zapisuje wczytany plik do macierzy img[x,y]
    
    global ax1, ax2
    fig, (ax1, ax2) = plt.subplots(1,2)
    
    Strukturalna(image_name)            #Następnie wywołuje funkcje Strukturalna, Delaunay i export
    structural = Delaunay(image_name, ax2)
    export(structural, image)
    plt.show()                          #plt.show() - Wyświetla wykresy