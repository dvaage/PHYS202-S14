##Devin Vaage's Version of the BlobFinder python module 
##
##
##This module follows the suggested code structure from the Particle Identification
##section of the Avagadros Number project
##
##
##
import matplotlib as plt
from PIL import Image
#Create a python module called Blobfinder.py that 
#includes a class Blob() (following the suggested code structure)
class Blob():
    def __init__(self):
        """construct an empty blob"""
        self.pixels = []
    def add(self, i, j):
        """add a pixel (i, j) to the blob"""
        self.pixels.append((i,j))
    def mass(self):
        """return number of pixels added = its mass"""
        return len(self.pixels)
    def centerOfMass(self):
        """return tuple of (x,y) values for this blob's center 
        of mass format center-of-mass coordinates with 4 digits 
        to right of decimal point"""
        xsum = ysum = 0
        for pixel in self.pixels:
            xsum += pixel[0]
            ysum += pixel[1]
        return (xsum / len(self.pixels), ysum / len(self.pixels))
    def distanceTo(self, blob):
        """For particle tracking purposes, returns displacement"""
        return round(((self.centerOfMass()[0] - blob.centerOfMass()[0]) ** 2 + \
                    (self.centerOfMass()[1] - blob.centerOfMass()[1]) ** 2) ** .5, 4)

    
#effectively applying the monochrome filter from counting stars
#to each image allows the blobs to be found more easily. 

def monochrome(picture, tau): #this comes from the counting stars tour
    """Sets background to white and pixels above threshold to black"""
    temp = picture.load()
    xsize, ysize = picture.size
    for x in range(xsize):
        for y in range(ysize):
            r,g,b = temp[x,y]
            if r+g+b >= tau:
                temp[x,y] = (0,0,0)
            else:
                temp[x,y] = (255,255,255)
                
def fillBlob(picture, xsize, ysize, xstart, ystart):
    """each call to 'fillBlob' takes care of one pixel in the blob,
    then calls 'fillBlob' again to take care of the neighbors"""
    BLACK = (0,0,0)
    RED = (255,0,0)
    queue = [(xstart,ystart)]
    blob = Blob()
    blob.add(xstart, ystart)
    while queue:
        x,y,queue = queue[0][0], queue[0][1], queue[1:]
        if picture[x,y] == BLACK:
            picture[x,y] = RED
            blob.add(x,y)
            if x > 0:
                 queue.append((x-1,y))
            if x < (xsize-1):
                 queue.append((x+1,y))
            if y > 0:
                 queue.append((x, y-1))
            if y < (ysize-1):
                queue.append((x, y+1))
    return blob

def BlobFinder(picture, tau):
    """find all blobs in the picture using a given Tau"""
    blobs = []
    xsize, ysize = picture.size
    temp = picture.load()
    BLACK = (0,0,0)
    RED = (255,0,0)
    #replacing the RGB values of each with either 
    #black or white depending on whether its total 
    #luminance, tau
    monochrome(picture, tau)
    for x in range(xsize):
        for y in range(ysize):
            if temp[x,y] == BLACK:
                blobs.append(fillBlob(temp,xsize,ysize,x,y))
    return blobs

#following the suggest code structure:
def countBeads(P, blobs):
    """return the number of beads with >= P pixels"""
    bead_count = 0
    for blob in blobs:
        if blob.mass() >= P:
            bead_count += 1
    return bead_count

#following the suggest code structure:
def getBeads(P, blobs):
    """return all beads with >= P pixels"""
    beads = []
    for blob in blobs:
        if blob.mass() >= P:
            beads.append(blob)
    return beads