import matplotlib as plt
from PIL import Image
#Classifying what a blob is
class Blob():
    def __init__(self):
        self.pixels = []
    def add(self, i, j):
        self.pixels.append((i,j))
    def mass(self):
        return len(self.pixels)
    def centerOfMass(self):
        """Averages the x and y components of every pixel in blob to estimate center of mass"""
        xsum = ysum = 0
        for pixel in self.pixels:
            xsum += pixel[0]
            ysum += pixel[1]
            return (xsum / len(self.pixels), ysum / len(self.pixels))
    def distanceTo(self, blob):
        return round(((self.centerOfMass()[0] - blob.centerOfMass()[0]) ** 2 + (self.centerOfMass()[1] - blob.centerOfMass()[1]) ** 2) ** .5, 4)
#Defining the filterImage function to invert the colorscale to adjust the 
#background to a white color and the pixels to a black color
def filterImage(picture, tau):
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
#from Counting stars, defining a fill function that counts the black pixels
#and makes them red
def fillBlob(picture, xsize, ysize, xstart, ystart):
    """each call to 'fillrec' takes care of one pixel then calls 'fillrec' again to take care of the neighbors"""
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
#defining a BlobFinder function that uses fillBlob
def BlobFinder(picture, tau):
    blobs = []
    xsize, ysize = picture.size
    temp = picture.load()
    BLACK = (0,0,0)
    RED = (255,0,0)
    filterImage(picture, tau)
    for x in range(xsize):
        for y in range(ysize):
            if temp[x,y] == BLACK:
                blobs.append(fillBlob(temp,xsize,ysize,x,y))
                return blobs
#defining the function that counts blobs
def countBeads(P, blobs):
    '''return the number of beads with >= P pixels'''
    bead_count = 0
    for blob in blobs:
        if blob.mass() >= P:
            bead_count += 1
        return bead_count
#defining the function that takes blobs and determines if they weigh enough to be beads
def getBeads(P, blobs):
    '''return all beads with >= P pixels'''
    beads = []
    for blob in blobs:
        if blob.mass() >= P:
            beads.append(blob)
            return beads
#defining the analyze image function that when called, will give you the number of beads and their mass    
def analyzeImage(P, tau, image_file):
    pic = Image.open(image_file)
    blobs = BlobFinder(pic, tau)
    print "Beads with mass >= %d:" %P
    for bead in getBeads(P, blobs):
        print "Mass: ", bead.mass()