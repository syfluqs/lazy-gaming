#!/bin/env python2

import sys
sys.path.insert(0,'../lib')
import android_connect
import gridmaker
import numpy as np
from cv2 import *
from matplotlib import pyplot as plot

#initialising connetion to phone
print "> Initialising connection to phone > "+str(time.time()-t)
phone = android_connect.android_com(1)
if not phone.dev_detected:
    quit()

phone.screenshot()

im = imread('tmp.png')
(h, w, ch) = img.shape

