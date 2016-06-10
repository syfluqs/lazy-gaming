#!/bin/env python2

import subprocess
import sys

class android_com(object):

    def __init__(self, adb_path="adb", dev_id=None):
        #self.dev_id = dev_id
        self.adb_path = adb_path
        if dev_id == None:
            self.dev_id = self.getDeviceList()
        else if type(dev_id) == 'str':
            self.dev_id = dev_id
        else if type(dev_id) == 'int':
            self.dev_id = self.getDeviceList(dev_id)
        else:
            print "Illegal device id supplied\nContinuing without a device id"

        

    def getDeviceList(self, n=None):
        l=self.sendCommand('devices')
        l=l[0].split('\n')
        l=l[1:-2]
        if n == None:
            if len(l)==0:
                print "No devices detected"
                return -1
            else:
                print "Select the device: (0 for not using id)"
                for item in enumerate(l):
                    print str(item[0]+1)+": "+str(item[1])
                    while True:
                        try:
                            n = int(raw_input('> '))
                            break
                        except ValueError:
                            continue

        if n:
            return l[n-1].split('\t')[0]
        else:
            return 0


    def adb(self, parameter):
        p = subprocess.Popen(self.adb_path+' '+parameter, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
        return (p.stdout.read(), p.stderr.read())

    def shell(self, cmd):
        p = subprocess.Popen(self.adb_path+' shell '+cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
        return (p.stdout.read(), p.stderr,read())


"""
if __name__ == '__main__':
    a = android_com()
    a.sendCommand('shell ls')
"""