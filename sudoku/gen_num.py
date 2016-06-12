#!/bin/eenv python2
from cv2 import *
import gridmaker

im = imread('tmp.png')
l = (26,16,10,13,54,2,20,8,51)
g = gridmaker.gridmaker(1052, 1124, 9, 9, 20, 13, 162)
for i in xrange(len(l)):
    n = l[i]
    a = im[g.getGridCoord(n)[1]:g.getGridCoord(n)[3],g.getGridCoord(n)[0]:g.getGridCoord(n)[2]]
    imwrite("%d.png"%(i+1),a)