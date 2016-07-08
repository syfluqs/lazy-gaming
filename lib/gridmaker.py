#!/bin/env python2

class gridmaker(object):

    def __init__(self, width, height, x_div, y_div, tolerance=0, x_offset=0, y_offset=0):
        self.x_offset = x_offset
        self.y_offset = y_offset
        #size of whole canvas
        self.size = (width,height)
        #size of each grid
        self.grid_size = (None, None)
        #list of origin coordinates (top-left corner) of each grid in the order starting from top left corner of the canvas and then to the right
        self.grid_list = []

        self.cols=x_div
        self.rows=y_div

        if (type(tolerance)==int):
            self.makeGrid(x_div, y_div, tolerance, tolerance, tolerance, tolerance)
        elif (type(tolerance)==tuple and len(tolerance)==4 and type(tolerance[0])==int and type(tolerance[1])==int and type(tolerance[2])==int and type(tolerance[3])==int):
            self.makeGrid(x_div, y_div, tolerance[0], tolerance[1], tolerance[2], tolerance[3])
        else:
            print 'Invalid input parameters'


    """
    +-----+-----+-----+-----+-----+-----+
    |  0  |  1  |  2  |  3  |  4  |  5  |
    |     |     |     |     |     |     |
    +-----+-----+-----+-----+-----+-----+
    |  6  |  7  |  8  |  9  | 10  | 11  |
    |     |     |     |     |     |     |
    +-----+-----+-----+-----+-----+-----+
    | 12  | 13  | 14  | 15  | 16  | 17  |
    |     |     |     |     |     |     |
    +-----+-----+-----+-----+-----+-----+
    :     :     :     :     :     :     :
    :     :     :     :     :     :     :
    and so on
    """

    def num2xy(self, num):
        """
        This method will take number as input and return equivalent cartesian coordinates
        of the grid.
        The origin is the top-left box.
        """
        #num=num+1
        m = self.cols*self.rows-1
        if (num>=m or num<0):
            return (-1,-1)
        else:
            return ((num)%self.cols,num/self.cols)

    def xy2num(self, x, y):
        if (x>self.cols or x<0 or y>self.rows or y<0):
            return -1
        else:
            return y*self.cols+x


    def makeGrid(self, x_div, y_div, tolerance_x1, tolerance_x2, tolerance_y1, tolerance_y2):
        s = (self.size[0]/x_div, self.size[1]/y_div)
        self.grid_list = []
        for i in xrange(y_div):
            for j in xrange(x_div):
                self.grid_list.append((self.x_offset+j*s[0]+tolerance_x1, self.y_offset+i*s[1]+tolerance_y1, self.x_offset+(j+1)*s[0]-tolerance_x2, self.y_offset+(i+1)*s[1]-tolerance_y2))
        self.grid_size = (s[0]-tolerance_x1-tolerance_x2, s[1]-tolerance_y1-tolerance_y2)

    def getGridCoord(self, n):
        return self.grid_list[n]

    def getGridNum(self, x, y):
        """
         Finds the number of grid in which the given coordinate is present
         Returns -1 if the coordinate is not inside or is on the line of any grid
        """
        first_row = self.grid_list[:self.cols]
        first_col = self.grid_list[0::self.cols]
        print first_row
        print first_col

        #searching using binary search
        i = self.cols
        j = self.rows
        print "binary search"

        tmp = first_row
        while (i):
            i=i/2
            if tmp[i][0]<x:
                tmp=tmp[:i]
            elif tmp[i][0]>x:
                tmp=tmp[i:]
            else:
                return -1
            print tmp,i



if __name__ == '__main__':
    g = gridmaker(100,100,5,4)
    print g.getGridNum(3,4)
