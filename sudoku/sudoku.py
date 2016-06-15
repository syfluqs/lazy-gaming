#!/bin/env python2
import time
t = time.time()

from cv2 import *
#for importing custom modules
import sys
sys.path.insert(0, '../lib')
import android_connect
import gridmaker
import numpy as np
import subprocess
import os


canvas = (1052, 1124)
buttons = ((350,1410), (542,1388), (750,1388), (316,1606), (548,1598), (762,1610), (308,1812), (544,1804), (754,1794))

sample = []
for i in xrange(9):
    sample.append(imread("%d.png"%(i+1)))

#initialising connetion to phone
print "> Initialising connection to phone > "+str(time.time()-t)
phone = android_connect.android_com(1)
if not phone.dev_detected:
    quit()
    

"""
phone.tap(520,777,100)
phone.tap(461,721,100)
phone.tap(441,1454,100)
time.sleep(0.5)
"""

phone.screenshot()

img = imread('tmp.png')
(h, w, ch) = img.shape

def compare(img, template, threshold=0.80):
    res = matchTemplate(img, template, TM_CCOEFF_NORMED)
    l = np.where(res>=threshold)
    l = zip(*l)
    if len(l):
        return True
    else:
        return False

#make grid object
grid = gridmaker.gridmaker(canvas[0], canvas[1], 9, 9, 10, 14, 164)

#sagestring is written in a file for sage to evaluate
sagestring = "s = Sudoku('"
input_board = []

#looping over all grids and identifying the digits
print "> Identifying digits > "+str(time.time()-t)
for n in xrange(81):
    match = False
    for s in enumerate(sample):
        toCompare = img[grid.getGridCoord(n)[1]:grid.getGridCoord(n)[3], grid.getGridCoord(n)[0]:grid.getGridCoord(n)[2]]
        if compare(toCompare, s[1]):
            sagestring+=str(s[0]+1)
            input_board.append(s[0]+1)
            match = True
    if not match:
        sagestring+="."
        input_board.append(0)

#constructing the rest of the sagestring
sagestring+="')\nnext(s.solve()).to_list()\nf=open('sageout','w')\nf.write(str(next(s.solve()).to_list()))\nf.close()"

#writing sagestring to file
print "> Calling sage > "+str(time.time()-t)
sagetemp = open('sagetemp.sage', 'w')
sagetemp.write(sagestring)
sagetemp.close()
#subprocess.Popen('sage sagetemp.sage', shell=True)
subprocess.call(('sage','sagetemp.sage'))

#reading sage output
print "> Parsing sage output > "+str(time.time()-t)
sageout = open('sageout','r')
out = sageout.read()
sageout.close()

#removing useless files
os.remove('sageout')
os.remove('sagetemp.sage')
os.remove('sagetemp.sage.py')
os.remove('tmp.png')

#parsing the output
out = out[1:-1].split(', ')

#sending taps
print "> Sending taps > "+str(time.time()-t)
adbtemp = open('adbtemp.sh','w')
for i in enumerate(input_board):
    if not i[1]:
        adbtemp.write("input tap %d %d\n"%((grid.getGridCoord(i[0])[0]+grid.getGridCoord(i[0])[2])/2,(grid.getGridCoord(i[0])[1]+grid.getGridCoord(i[0])[3])/2))
        ans = int(out[i[0]])
        #adbtemp.write("input tap %d %d\n"%(buttons[ans-1][0], buttons[ans-1][1]))
        adbtemp.write("input keyevent %d\n"%(ans+7))
adbtemp.close()
phone.bashscript('adbtemp.sh')
os.remove('adbtemp.sh')

print "==> Total time taken:"+str(time.time()-t)