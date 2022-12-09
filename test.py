from control_volume.geometry import Geometry,Ellipse,Airfoil
from plot import PLOT
import math
import numpy as np
import matplotlib.pyplot as plt

e = Ellipse(2, 6, 10)
e.create_panels()
PLOT(e)
# d = e.wind()




file = ''
airfoil = Airfoil('naca2412.dat')
PLOT(airfoil)
# f = open(file, 'w')
# f.write('hello Adotey!\nHow are yiw')
# f.close()

# f = open(file, 'r')
# c = f.readlines()
# print(c)
# f.close()

# with open(file, 'a') as f:
#     c = f.write('\nThe keys')
# print(c)

