# -*- coding:utf-8 -*-

import math

class Vector(list):
    def __init__(self, x=0, y=0):
        if isinstance(x, (list, tuple)):
            self.append(x[0])
            self.append(x[1])
        else:
            self.append(x)
            self.append(y)

    def getX(self):
        return self[0]

    def setX(self, value):
        self[0] = value

    x = property(getX, setX)

    def getY(self):
        return self[1]
    
    def setY(self, value):
        self[1] = value

    y = property(getY, setY)


    def __add__(self, v2):
        try:
            return Vector(self[0]+v2[0], self[1]+v2[1])
        except TypeError as e:
            return Vector(self[0]+v2, self[1]+v2)

    def __iadd__(self, v2):
        try:
            self[0] += v2[0]
            self[1] += v2[1]
        except TypeError as e:
            self[0] += v2
            self[1] += v2
        return self

    def __sub__(self, v2):
        try:
            return Vector(self[0]-v2[0], self[1]-v2[1])
        except TypeError as e:
            return Vector(self[0]-v2, self[1]-v2)

    def __isub__(self, v2):
        try:
            self[0] -= v2[0]
            self[1] -= v2[1]
        except TypeError as e:
            self[0] -= v2
            self[1] -= v2
        return self

    def __mul__(self, v2):
        try:
            return Vector(self[0]*v2[0], self[1]*v2[1])
        except TypeError as e:
            return Vector(self[0]*v2, self[1]*v2)

    def __imul__(self, v2):
        try:
            self[0] *= v2[0]
            self[1] *= v2[1]
        except TypeError as e:
            self[0] *= v2
            self[1] *= v2
        return self

    def __div__(self, v2):
        try:
            return Vector(self[0]/v2[0], self[1]/v2[1])
        except TypeError as e:
            return Vector(self[0]/v2, self[1]/v2)

    def __eq__(self, v2):
        return self[0] == v2[0] and self[1] == v2[1]

    def __ne__(self, v2):
        return self[0] != v2[0] and self[1] != v2[1]

    def length(self):
        return math.sqrt(self[0]**2 + self[1]**2)

    def norm(self):
        len = float(self.length())
        self[0] /= len
        self[1] /= len
    
    def __repr__(self):
        return 'V('+str(self[0])+', '+str(self[1])+')'


if __name__ == '__main__':
    V = Vector
    a = V(6, 5)
    print a
    a.norm()
    print a