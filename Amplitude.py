from PIL import Image
import numpy as np
import math

soundPoints = [
    (-3,-3),
    (-3,3),
    (3,-3),
    (3,3)
]

def distance(p1:tuple,p2:tuple):
    dX = p2[0] - p1[0]
    dY = p2[1] - p1[1]
    return math.sqrt(dX**2 + dY**2)

def amplitudeFromPhase(*phases:float):
    c = 0
    s = 0
    for phase in phases:
        c += math.cos(phase)
        s += math.sin(phase)
    
    return math.sqrt(c**2 + s**2)
    

resolution = 1080
width = 15
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
        phases = []
        for emitter in soundPoints:
            pointDistance = distance((x,y),(emitter))
            phases.append(2 * math.pi * (pointDistance % wavelength) / wavelength)
        
        pixelStrength = amplitudeFromPhase(*phases) * strengthPerPoint * 255
        
        tempPix.append((pixelStrength,pixelStrength,pixelStrength))
        x += increment
    
    pix.append(tempPix)
    
    x = initX
    y -= increment

    
array = np.array(pix,dtype=np.uint8)

newImage = Image.fromarray(array)
newImage.save(f"Amplitude.png")
