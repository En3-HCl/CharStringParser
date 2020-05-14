from fontTools.misc.bezierTools import *

print(calcCubicBounds((0,0),(25,100),(75,100),(100,0)))
print(calcCubicBounds((0, 0), (25, 100), (75,100), (100, 0)))
print(calcCubicBounds((1, 1), (25, 100), (75,100), (100, 0)))
print(calcCubicBounds((300, 57), (465, 57), (599,191), (599, 356)))
print(calcCubicBounds((0, 0), (165, 0), (299,134), (299, 299)))
