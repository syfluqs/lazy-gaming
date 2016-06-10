#!/bin/env python2

import subprocess
import sys

class android_com(object):

    def __init__(self, adb_path="adb"):
        #self.dev_id = dev_id
        self.adb_path = adb_path
        self.getDeviceList();

    def getDeviceList(self):
        l=self.sendCommand('devices')
        print l

    def sendCommand(self, cmd):
        p = subprocess.Popen(self.adb_path+' '+cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
        return (p.stdout.read(), p.stderr.read())

if __name__ == '__main__':
    a = android_com()
    a.sendCommand('devices')