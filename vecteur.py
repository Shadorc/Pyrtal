from math import *

class vec():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    #Produit vectoriel
    def __mul__(self, vec1):
        x = self.y * vec1.z - self.z * vec1.y
        y = - self.x * vec1.z + self.z * vec1.x
        z = self.x * vec1.y - self.y * vec1.x 
        return vec(x, y, z)

    #Produit scalaire
    def scal(self, vec1):
        return self.x + vec1.x + self.y + vec1.y + self.z + vec1.z

    #Addition
    def __add__(self, vec1):
        x = self.x + vec1.x
        y = self.y + vec1.y
        z = self.z + vec1.z
        return vec(x, y, z)

    #Soustraction
    def __sub__(self, vec1):
        x = self.x - vec1.x
        y = self.y - vec1.y
        z = self.z - vec1.z
        return vec(x, y, z)

    def norme(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def __repr__(self):
        return '/' + str(self.x) + '\\\n| ' + str(self.y) + '| \n\\' + str(self.z) + '/'
