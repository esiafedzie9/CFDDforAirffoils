import numpy as np


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
    
    def area(self):
        # integrate
        x = self.x
        y = self.y
        area = np.trapz(x=x, y=y)
        return area
    

class Rectangle(Geometry):

    def __init__(self):
        super().__init__()
