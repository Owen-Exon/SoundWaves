from PIL import Image
import numpy as np
import math

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

strengthPerPoint = 1/len(soundPoints)
increment = width / resolution
initX , initY = center[0]-width/2 , center[1]+width/2
x , y = initX , initY

pix = []
while (initY-y) < width:
    tempPix = []
    while (x-initX) < width:
        # strength = 0
        phases =[]
        for emitter in soundPoints:
            pointDistance = distance((x,y),(emitter))
            phases.append(2 * math.pi * (pointDistance % wavelength) / wavelength)
            
        pixelStrength = abs(2*strengthPerPoint*math.cos((phases[1]-phases[0])/2)) * 255
        tempPix.append((pixelStrength,pixelStrength,pixelStrength))
        x += increment
    
    pix.append(tempPix)
    
    x = initX
    y -= increment

    
array = np.array(pix,dtype=np.uint8)

newImage = Image.fromarray(array)
newImage.save(f"Amplitude.png")
