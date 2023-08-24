import numpy as np
from PIL import Image
from PIL import ImageOps
import matplotlib.pyplot as plt
import itertools
import math
import cv2
import time 

def ssd (window, image):
    return ((image-window)**2).sum()

def ncc (window, image):
    window = window[:, 0]
    image = image[:, 0]
    window = window / np.linalg.norm(window)
    image = image / np.linalg.norm(image)
    return np.correlate(window, image, mode = 'full').sum()
    #return cv2.matchTemplate(np.float32(window-image.mean()), np.float32(window-image.mean()), cv2.TM_CCORR_NORMED)[0,0]

def displace(image, base_image):
    minimum_score = math.inf # if ssd invert negative sign
    # blue as base and green as windowed
    for dx, dy in itertools.product(range(-15,16), repeat=2):
        windowed = np.roll(image,(dx,dy), axis=(1,0))
        score = ssd(windowed, base_image)
        if score < minimum_score: # if ssd invert to < 
            minimum_score = score
            displacement = (dx,dy)

    return displacement

def run(image):
    l = int(len(image)/3)
    b = image[:l]
    g = image[l:2*l]
    r = image[2*l:3*l]
    b = b[5:-10,10:-20]
    g = g[5:-10,10:-20]
    r = r[5:-10,10:-20]
    '''
    # blue base
    dg1, dg2 = displace(g, b)
    dr1, dr2 = displace(r, b)
    gdisplaced = np.roll(g, (dg1,dg2), axis=[1,0])
    rdisplaced = np.roll(r, (dr1,dr2), axis=[1,0])
    b = Image.fromarray(b)
    g = Image.fromarray(gdisplaced)
    r = Image.fromarray(rdisplaced)
    print(dg1, dg2, dr1, dr2)'''
    '''
    # red base
    db1, db2 = displace(b, r)
    dg1, dg2 = displace(g, r)
    bdisplaced = np.roll(b, (db1,db2), axis=[1,0])
    gdisplaced = np.roll(g, (dg1,dg2), axis=[1,0])
    b = Image.fromarray(bdisplaced)
    g = Image.fromarray(gdisplaced)
    r = Image.fromarray(r)
    print(db1, db2, dg1, dg2)'''
    
    
    # green base
    db1, db2 = displace(b, g)
    dr1, dr2 = displace(r, g)
    bdisplaced = np.roll(b, (db1,db2), axis=[1,0])
    rdisplaced = np.roll(r, (dr1,dr2), axis=[1,0])
    b = Image.fromarray(bdisplaced)
    g = Image.fromarray(g)
    r = Image.fromarray(rdisplaced)
    print(db1, db2, dr1, dr2)
    
    img = Image.merge('RGB',(r,g,b))
    img.show()

    #img.save("ssdBlue_01112.jpeg")      

# opens the image
#img = 'data/00351v.jpg'
#img = 'data/00398v.jpg'
#img = 'data/01112v.jpg'
#img = 'data/00153v.jpg'
#img = 'data/00149v.jpg'
img = 'data/00125v.jpg'
image = np.array(Image.open(img))
start_time = time.time()
run(image)
end_time = time.time()
print(end_time - start_time)

