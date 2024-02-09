import random
import math
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image



def QuadTree(img,xStart, xFinish, width, yStart, yFinish, height):

    middleX = xStart+width//2
    middleY = yStart + height//2


    def sprawdzenie(xPoczatek, xKoniec, yPoczatek,yKoniec):
        white = 0
        black = 0
        for i in range (xPoczatek,xKoniec):
            for j in range (yPoczatek, yKoniec):
                #img[i,j]
                if img[i, j] == 0:
                    black += 1
                elif img[i, j] == 255:
                    white += 1
            if white > 40 and black > 40:
                QuadTree(img,xPoczatek, xKoniec, width//2, yPoczatek, yKoniec, height//2)
                break

    if width > 20 and height > 20:
        sprawdzenie(xStart, middleX, yStart,middleY)
        sprawdzenie(middleX, xFinish, yStart,middleY)
        sprawdzenie(xStart, middleX, middleY,yFinish)
        sprawdzenie(middleX, xFinish, middleY,yFinish)

    plt.plot([middleX,middleX],[yStart,yFinish], color = "palevioletred")
    plt.plot([xStart,xFinish ],[middleY,middleY], color = "palevioletred")


def get_macierz(plik):
    image = Image.open(plik, "r")
    plt.imshow(image)
    img = image.load()
    QuadTree(img, 0, image.size[0], image.size[0], 0, image.size[1], image.size[1])


if __name__ == '__main__':
    get_macierz("cloud.jpg")
    plt.show()

