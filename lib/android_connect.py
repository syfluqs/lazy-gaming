#!/bin/env python2

import subprocess
import sys
import os
import time

class android_com(object):

    def __init__(self, dev_id=None, adb_path="adb"):

        """
        dev_id
        keeps track of device id as a string, if a device is detected.
        if not this is set to -1
        if the user does not wants to provide any id, dev_id is set to 0, in which case it is upto adb to chose the device.

        dev_detected
        True for devie detected, although it is set True if explicitly told to not use and id.

        """


        self.adb_path = adb_path
        self.dev_id = -1
        self.dev_detected = False
        (self.dev_id, self.dev_detected) = self.getDeviceList(dev_id)

        

    def getDeviceList(self, n=None):
        (a,b) = (self.dev_id, self.dev_detected)
        (self.dev_id, self.dev_detected) = (0, True)
        l=self.adb('devices')
        (self.dev_id, self.dev_detected) = (a,b)
        l=l[0].split('\n')
        l=l[1:-2]
        dev_enum = enumerate(l)

        if len(l)==0:
                print "No devices detected"
                return (-1, False)

        if n == None:
            print "Select the device: (0 for not using id)"
            for item in dev_enum:
                print str(item[0]+1)+": "+str(item[1])
                while True:
                    try:
                        n = int(raw_input('> '))
                        assert (n<=len(l) and n>=0), 'Illegal input'
                        break
                    except ValueError, AssertionError:
                        continue
            if n:
                return (l[n-1].split('\t')[0], True)
            else:
                return (0, True)

        elif type(n) == str:
            #dev_present = False
            for item in dev_enum:
                if n in item[1]:
                    n = item[0]+1
                    #dev_present = True
                    return (n, True)

            print "No device found with the specified id"
            return (-1, False)


        elif type(n) == int:
            try:
                assert (n<=len(l) and n>=0), 'Illegal input'
                return (l[n-1].split('\t')[0], True)
                if ~n:
                    return (0, False)
            except ValueError, AssertionError:
                return (-1, False)

        else:
            return (-1, False)


        


    def adb(self, parameter=''):
        if self.dev_id>=0:
            p = subprocess.Popen(self.adb_path+' '+parameter, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
            return (p.stdout.read(), p.stderr.read())
        #if not returned already return error tuple
        return (1,1)

    def shell(self, cmd='date'):
        """
        Be careful not to pass cmd as ''
        This causes the script to hang up by invoking adb shell
        """
        if self.dev_id>=0:
            p = subprocess.Popen(self.adb_path+' shell '+cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
            return (p.stdout.read(), p.stderr.read())
        #if not returned already return error tuple
        return (1,1)

    def tap(self, x, y, delay=0):
        (a,b) = self.shell('input tap %d %d'%(x,y))
        if ~delay:
            time.sleep(delay/1000.0)
        if b!='' or b==1:
            return 1
        return 0


    def swipe(self, x1, y1, x2, y2, duration=50, delay=0):
        (a,b) = self.shell('input swipe %d %d %d %d'%(x1, y1, x2, y2))
        if ~delay:
            time.sleep(delay/1000.0)
        if b!='' or b==1:
            return 1
        return 0

    def text(self, msg, delay=0):
        (a,b) = self.shell('input text %s'%(msg))
        if ~delay:
            time.sleep(delay/1000.0)
        if b!='' or b==1:
            return 1
        return 0

    def keycode(self, key, longpress=False, delay=0):
        (a,b) = self.shell('input keyevent %s%s'%(('','--longpress ')[longpress],key))
        if ~delay:
            time.sleep(delay/1000.0)
        if b!='' or b==1:
            return 1
        return 0

    def bashscript(self, filename):
        self.adb('push %s /sdcard/tmp.sh'%(filename))
        self.shell('sh /sdcard/tmp.sh')
        self.shell('rm /sdcard/tmp.sh')

    def screenshot(self, out_dir=os.getcwd()):
        self.shell('screencap -p /sdcard/tmp.png')
        self.adb('pull /sdcard/tmp.png %s'%(out_dir))
        self.shell('rm /sdcard/tmp.png')


"""

*    *                                       *          
*   *                                        *          
*  *                                         *          
* *      ****   *    *   ****    ****    *** *   ****   
**      *    *  *    *  *    *  *    *  *   **  *    *  
* *     ******  *    *  *       *    *  *    *  ******  
*  *    *       *   **  *       *    *  *    *  *       
*   *   *    *   *** *  *    *  *    *  *   **  *    *  
*    *   ****        *   ****    ****    *** *   ****   
                *    *                                  
                 ****                                   

                                *             
                                *             
                                *             
 ****   *   *   ****   * ***   ****    ****   
*    *  *   *  *    *  **   *   *     *    *  
******  *   *  ******  *    *   *      **     
*        * *   *       *    *   *        **   
*    *   * *   *    *  *    *   *  *  *    *  
 ****     *     ****   *    *    **    ****   



0 -->  "KEYCODE_UNKNOWN" 
1 -->  "KEYCODE_MENU" 
2 -->  "KEYCODE_SOFT_RIGHT" 
3 -->  "KEYCODE_HOME" 
4 -->  "KEYCODE_BACK" 
5 -->  "KEYCODE_CALL" 
6 -->  "KEYCODE_ENDCALL" 
7 -->  "KEYCODE_0" 
8 -->  "KEYCODE_1" 
9 -->  "KEYCODE_2" 
10 -->  "KEYCODE_3" 
11 -->  "KEYCODE_4" 
12 -->  "KEYCODE_5" 
13 -->  "KEYCODE_6" 
14 -->  "KEYCODE_7" 
15 -->  "KEYCODE_8" 
16 -->  "KEYCODE_9" 
17 -->  "KEYCODE_STAR" 
18 -->  "KEYCODE_POUND" 
19 -->  "KEYCODE_DPAD_UP" 
20 -->  "KEYCODE_DPAD_DOWN" 
21 -->  "KEYCODE_DPAD_LEFT" 
22 -->  "KEYCODE_DPAD_RIGHT" 
23 -->  "KEYCODE_DPAD_CENTER" 
24 -->  "KEYCODE_VOLUME_UP" 
25 -->  "KEYCODE_VOLUME_DOWN" 
26 -->  "KEYCODE_POWER" 
27 -->  "KEYCODE_CAMERA" 
28 -->  "KEYCODE_CLEAR" 
29 -->  "KEYCODE_A" 
30 -->  "KEYCODE_B" 
31 -->  "KEYCODE_C" 
32 -->  "KEYCODE_D" 
33 -->  "KEYCODE_E" 
34 -->  "KEYCODE_F" 
35 -->  "KEYCODE_G" 
36 -->  "KEYCODE_H" 
37 -->  "KEYCODE_I" 
38 -->  "KEYCODE_J" 
39 -->  "KEYCODE_K" 
40 -->  "KEYCODE_L" 
41 -->  "KEYCODE_M" 
42 -->  "KEYCODE_N" 
43 -->  "KEYCODE_O" 
44 -->  "KEYCODE_P" 
45 -->  "KEYCODE_Q" 
46 -->  "KEYCODE_R" 
47 -->  "KEYCODE_S" 
48 -->  "KEYCODE_T" 
49 -->  "KEYCODE_U" 
50 -->  "KEYCODE_V" 
51 -->  "KEYCODE_W" 
52 -->  "KEYCODE_X" 
53 -->  "KEYCODE_Y" 
54 -->  "KEYCODE_Z" 
55 -->  "KEYCODE_COMMA" 
56 -->  "KEYCODE_PERIOD" 
57 -->  "KEYCODE_ALT_LEFT" 
58 -->  "KEYCODE_ALT_RIGHT" 
59 -->  "KEYCODE_SHIFT_LEFT" 
60 -->  "KEYCODE_SHIFT_RIGHT" 
61 -->  "KEYCODE_TAB" 
62 -->  "KEYCODE_SPACE" 
63 -->  "KEYCODE_SYM" 
64 -->  "KEYCODE_EXPLORER" 
65 -->  "KEYCODE_ENVELOPE" 
66 -->  "KEYCODE_ENTER" 
67 -->  "KEYCODE_DEL" 
68 -->  "KEYCODE_GRAVE" 
69 -->  "KEYCODE_MINUS" 
70 -->  "KEYCODE_EQUALS" 
71 -->  "KEYCODE_LEFT_BRACKET" 
72 -->  "KEYCODE_RIGHT_BRACKET" 
73 -->  "KEYCODE_BACKSLASH" 
74 -->  "KEYCODE_SEMICOLON" 
75 -->  "KEYCODE_APOSTROPHE" 
76 -->  "KEYCODE_SLASH" 
77 -->  "KEYCODE_AT" 
78 -->  "KEYCODE_NUM" 
79 -->  "KEYCODE_HEADSETHOOK" 
80 -->  "KEYCODE_FOCUS" 
81 -->  "KEYCODE_PLUS" 
82 -->  "KEYCODE_MENU" 
83 -->  "KEYCODE_NOTIFICATION" 
84 -->  "KEYCODE_SEARCH" 
85 -->  "TAG_LAST_KEYCODE
"""


if __name__ == '__main__':
    #connect to first android device connected and print date
    a = android_com(1)
    a.screenshot()