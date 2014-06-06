from PIL import Image
def compareFrames(frame1, frame2, P, tau, deltaP):
    """Returns the displacement of each particle from one frame to the next"""
    f1 = Image.open(frame1)
    frame1_blobs = getBeads(P, BlobFinder(f1, tau))
      
    f2 = Image.open(frame2)
    frame2_blobs = getBeads(P, BlobFinder(f2, tau))
    
    
    displacements = []
    
    #Start with a blob in frame1, and find the closet blob in frame2 within distance deltaP.
    #Add to displacements list and remove blobs
    for i in range(len(frame1_blobs)):
        min_dr = deltaP
        for j in range(len(frame2_blobs)):
            dr = frame1_blobs[i].distanceTo(frame2_blobs[j])
            if(dr < min_dr):
                min_dr = dr
                closestBlob = j
        if min_dr < deltaP:
            #print frame1_blobs[i].centerOfMass(), frame2_blobs[closestBlob].centerOfMass()
            displacements.append(str(min_dr)+'\n')          
            del frame2_blobs[closestBlob]
    
    return displacements
        

def record_motion(P, tau, deltaP, images, out_file_name):
    displacements = []
    out = open(out_file_name, 'w')
    for i in xrange(len(images) - 1):
        displacements += compareFrames(images[i], images[i+1], P, tau, deltaP)
        print "Image", i + "Done"
    out.writelines(displacements)
    out.close()