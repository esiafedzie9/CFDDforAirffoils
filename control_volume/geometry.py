import numpy as np
import math


class Geometry(object):

    def __init__(self):
        self._points = None
        self._n_points = None
        self._area = None
        self._volume = None
        self._perimeter = None

    @property
    def points(self):
        return self._points

    @property
    def x(self):
        if self._points is not None:
            return self._points[:, 0]
        else:
            raise ValueError('No points')
    
    @property
    def y(self):
        if self._points is not None:
            return self._points[:, 1]
        else:
            raise ValueError('No points')
    
    @property
    def z(self):
        if self._points is None:
            raise ValueError('No points')
        else:
            return self._points[:, 2]

    @property
    def n_points(self):
        return self._n_points
    
    @x.setter
    def x(self, value):
        if isinstance(value, np.ndarray):
            self._points[:, 0] = value
        else:
            raise ValueError('Must set x property as a numpy array')
    
    @y.setter
    def y(self, value):
        if isinstance(value, np.ndarray):
            self._points[:, 1] = value
        else:
            raise ValueError('Must set y property as a numpy array')
    
    @z.setter
    def z(self, value):
        if isinstance(value, np.ndarray):
            self._points[:, 2] = value
        else:
            raise ValueError('Must set z property as a numpy array')
    
    @points.setter
    def points(self, points):
        """
        Expects a list of points / numpy array of points
        N = [[x1, y1, z1], [x2, y2, z2], ...]
        N[:, 0] 
        main = []
        p1 = [1, 2, 3]
        p2 = [2, 4, 5]
        main = np.array([[1, 2, 3], [2, 4, 5]])
        """
        if isinstance(points, list):
            points = np.array(points)
        self._points = points
        self._n_points = np.size(points)


class Ellipse(Geometry):

    def __init__(self, a, b, n):
        super().__init__()
        self.n = n
        theta = np.linspace(0, 360, self.n+1)
        theta = theta[:-1]
        self._x = []
        self._y = []
        points = []
        for num in theta:  
            d = b*math.cos((num*math.pi)/180)
            self._x.append(d)
            f = a*math.sin((num*math.pi)/180)
            self._y.append(f)
            points.append([d, f])
        self.points = points


class Rectangle(Geometry):
    def __init__(self, width, height, n):
        super().__init__()
        self.n = n
        c = np.linspace(0, 2*math.pi, self.n + 1)
        self.t = c[:-1]
        x = width * (np.abs(np.cos(self.t))*np.cos(self.t) + np.abs(np.sin(self.t))*np.sin(self.t)) 
        y = height * (np.abs(np.cos(self.t))*np.cos(self.t) - np.abs(np.sin(self.t))*np.sin(self.t)) 
        points = []
        for a, b in zip(x, y):
            points.append([a,b])
        self.points = points
