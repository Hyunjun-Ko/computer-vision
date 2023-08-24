
import cv2
import numpy as np
from PIL import Image
import itertools
import math
import time

def ssd (window, image):
    return ((image-window)**2).sum()

def ncc (window, image):
    window = window[:, 0] - window.mean()
    image = image[:, 0] - image.mean()
    window = window / np.linalg.norm(window)
    image = image / np.linalg.norm(image)
    return np.correlate(window, image, mode = 'full').sum()

def displace(image, base_image):
    s_image = cv2.resize(image, (0,0), fx = 0.125, fy=0.125)
    s_base_image = cv2.resize(base_image, (0,0), fx = 0.125, fy=0.125)
    q_image = cv2.resize(image, (0,0), fx = 0.25, fy=0.25)
    q_base_image = cv2.resize(base_image, (0,0), fx = 0.25, fy=0.25)
    h_image = cv2.resize(image, (0,0), fx = 0.5, fy=0.5)
    h_base_image = cv2.resize(base_image, (0,0), fx = 0.5, fy=0.5)
    array = []
    array.append(s_image)
    array.append(q_image)
    array.append(h_image)
    array.append(image)
    barray = []
    barray.append(s_base_image)
    barray.append(q_base_image)
    barray.append(h_base_image)
    barray.append(base_image)
    x, y = [0,0]
   
    for iter in range(4):
        # blue as base and green as windowed
        minimum_score = -math.inf # if ssd invert negative sign
        for dx, dy in itertools.product(range(-15,16), repeat=2):
            dx = dx+x
            dy = dy+y
            windowed = np.roll(array[iter],(dx,dy), axis=(1,0))
            score = ncc(windowed, barray[iter])
            if score > minimum_score: # if ssd invert to < 
                minimum_score = score
                displacement = (dx,dy)
        if iter == 2:
            return displacement
        x = int(2*dx)
        y = int(2*dy)



    #return displacement

start_time = time.time()
img = 'data_hires/01861a.tif'
image = cv2.imread(img,cv2.IMREAD_GRAYSCALE)

l = int(len(image)/3)
b = image[:l]
g = image[l:2*l]
r = image[2*l:3*l]
b = b[150:-150,130:-130]
g = g[150:-150,130:-130]
r = r[150:-150,130:-130]
r = np.roll(r, 90,axis=0)
r = np.roll(r, 20,axis=1)
b = np.roll(b, -20,axis=0)

dg1, dg2 = displace(g, b)
dr1, dr2 = displace(r, b)
gdisplaced = np.roll(g, (dg1,dg2), axis=[1,0])
rdisplaced = np.roll(r, (dr1,dr2), axis=[1,0])
b = Image.fromarray(b)
g = Image.fromarray(gdisplaced)
r = Image.fromarray(rdisplaced)
print(dg1,dg2,dr1,dr2)

'''
# red base
db1, db2 = displace(b, r)
dg1, dg2 = displace(g, r)
bdisplaced = np.roll(b, (db1,db2), axis=[1,0])
gdisplaced = np.roll(g, (dg1,dg2), axis=[1,0])
b = Image.fromarray(bdisplaced)
g = Image.fromarray(gdisplaced)
r = Image.fromarray(r)
print(db1,db2,dg1,dg2)'''

'''
# green base
db1, db2 = displace(b, g)
dr1, dr2 = displace(r, g)
bdisplaced = np.roll(b, (db1,db2), axis=[1,0])
rdisplaced = np.roll(r, (dr1,dr2), axis=[1,0])
b = Image.fromarray(bdisplaced)
g = Image.fromarray(g)
r = Image.fromarray(rdisplaced)
print(db1,db2,dr1,dr2)'''

img = Image.merge('RGB',(r,g,b))
end_time = time.time()
total_time = end_time - start_time
print(total_time)
img.show()
#img.save("nccBlue_01816a.jpeg")

