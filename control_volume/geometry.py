import numpy as np
import os
from scipy.interpolate import CubicSpline
import math


class Geometry(object):

    def __init__(self):
        self._points = None
        self._n_points = None
        self._area = None
        self._volume = None
        self._perimeter = None
    
    def wind(self):
        summ = 0
        for i in range(0, len(self.points)-1):
            s = (self.points[1+i][0] - self.points[i][0])*(self.points[1+i][1] + self.points[i][1])
            summ += s
        if summ < 0:
            print('reversed')
            self.points = self.points[:len(self.points):-1]
        else:
            print('not reversed')

    def create_panels(self):
        self.s = []
        self.c = []
        for i in range(0, len(self.points)-1):
            a = (self.points[1+i][0] - self.points[i][0])/2
            b = (self.points[1+i][1] - self.points[i][1])/2
            self.c.append([a,b])
            d = math.sqrt((self.points[1+i][0] - self.points[i][0])**2 +(self.points[1+i][1] - self.points[i][1])**2)
            self.s.append(d)

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
            raise ValueError('Must set x property as a np array')
    
    @y.setter
    def y(self, value):
        if isinstance(value, np.ndarray):
            self._points[:, 1] = value
        else:
            raise ValueError('Must set y property as a np array')
    
    @z.setter
    def z(self, value):
        if isinstance(value, np.ndarray):
            self._points[:, 2] = value
        else:
            raise ValueError('Must set z property as a np array')
    
    @points.setter
    def points(self, points):
        """
        Expects a list of points / np array of points
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
        self.wind()


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
        self.wind()


class AirfoilParser(object):

    def __init__(self, file,) -> None:
        self.files = os.listdir('data/Airfoils')
        self.files.sort()
        self._upper = None
        self._lower = None
        if file in self.files:
            self._file = file
            self.parse()
        else:
            print("AirfoilParser: No such airfoil file", 'E')

    @property
    def upper(self):
        return self._upper
    
    @property
    def lower(self):
        return self._lower


    def parse(self):
        full_path = os.path.join('data/Airfoils', self._file)
        upper = []
        lower = []
        is_upper = True
        prev = 2
        with open(full_path, 'r') as airfoil_file:
            for line in airfoil_file.readlines():
                content = line.split(' ')
                if len(content) == 1:
                    content = content[0].split('\t')
                content = [i.replace('\n', '') for i in content]
                content = [i for i in content if i != '']
                
                if len(content) == 2:
                    try:
                        x = float(content[0])
                        y = float(content[1])
                        if x > prev:
                            is_upper = False
                        
                        prev = x
                        if is_upper:
                            upper.append([x, y])
                        else:
                            lower.append([x, y])
                        
                    except Exception as E:
                        pass
                    finally:
                        pass
        self._upper = np.array(upper)
        self._lower = np.array(lower)
        if len(upper) > 0 and len(lower) == 0:
            self._lower = np.array(upper)[::-1]
            self._lower[:, 1] = -self._lower[:, 1]


class Airfoil(Geometry):

    def __init__(self, file=None, centroid=[0, 0], n_points=40) -> None:
        super().__init__()
        self._file = file
        points = self.getairfoil(file)
        self._n_points = n_points
        self.points = points
        
    
    def getairfoil(self, file):
        airfoil_data = AirfoilParser(file)
        self._file = file
        upper_points = airfoil_data.upper
        lower_points = airfoil_data.lower
        upper_points_interp = CubicSpline(upper_points[:, 0][::-1], upper_points[:, 1:][::-1], extrapolate=True)
        lower_points_interp = CubicSpline(lower_points[:, 0], lower_points[:, 1:], extrapolate=True)
        x = np.linspace(0, 1, self._n_points) ** 1.4
        upper_points = upper_points_interp(x)
        lower_points = lower_points_interp(x)
        upper_points = np.vstack([x, upper_points.T]).T[::-1]
        lower_points = np.vstack([x, lower_points.T]).T
        points = np.concatenate([upper_points, lower_points], axis=0)
        return points

    def get_chord_length(self):
        return np.max(self.points[:, 0]) - np.min(self.points[:, 0])
    
    def get_thickness(self):
        return np.max(self.points[:, 1]) - np.min(self.points[:, 1])
