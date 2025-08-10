# from PIL import Image
import numpy as np
import math
import imageio.v2 as imageio

soundPoints = [
    (3,0),
    (-3,0)
]

def distance(p1:tuple,p2:tuple):
    dX = p2[0] - p1[0]
    dY = p2[1] - p1[1]
    return math.sqrt(dX**2 + dY**2)

resolution = 256
width = 10
center = (0,0)
wavelength = 2
frames = 30
timeIncrement = (2*math.pi)/(frames+1)

strengthPerPoint = 0.5/len(soundPoints)
increment = width / resolution
initX , initY = center[0]-width/2 , center[1]+width/2
x , y = initX , initY

images = []

for frame in range(frames):
    x , y = initX , initY
    pix = []
    while (initY-y) < width:
        tempPix = []
        while (x-initX) < width:
            strength = 0
            for emitter in soundPoints:
                pointDistance = distance((x,y),(emitter))
                strength += math.sin( (2 * math.pi * (pointDistance % wavelength) / wavelength) - (frame*timeIncrement) ) * strengthPerPoint
            pixelStrength = (strength + 0.5) * 255
            tempPix.append((pixelStrength,pixelStrength,pixelStrength))
            x += increment
        
        pix.append(tempPix)
        
        x = initX
        y -= increment
        
    images.append(pix)
    print(frame)
    
frames = [np.array(img,dtype=np.uint8) for img in images]
imageio.mimsave("Output.gif", frames, fps=15,loop=0)