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

        self.makeGrid(x_div, y_div, tolerance)

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

    def makeGrid(self, x_div, y_div, tolerance=0):
        s = (self.size[0]/x_div, self.size[1]/y_div)
        self.grid_list = []
        for i in xrange(y_div):
            for j in xrange(x_div):
                self.grid_list.append((self.x_offset+j*s[0]+tolerance, self.y_offset+i*s[1]+tolerance, self.x_offset+(j+1)*s[0]-tolerance, self.y_offset+(i+1)*s[1]-tolerance))
        self.grid_size = (s[0]-2*tolerance, s[1]-2*tolerance)

    def getGridCoord(self, n):
        return self.grid_list[n]


if __name__ == '__main__':
    g = gridmaker(1000,1000,10,10,4,1,1)
    print g.grid_size
    print g.grid_list