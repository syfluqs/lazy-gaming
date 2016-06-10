#!/bin/env python2

import cv2
import os
import android_connect

phone = android_connect.android_com(1)
print phone.shell('ls')