from PIL import Image
import numpy as np
import math
import imageio.v2 as imageio



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


def saveImage(fileName,pixels:list):
    array = np.array(pixels,dtype=np.uint8)

    newImage = Image.fromarray(array)
    newImage.save(fileName)

def saveVideo(fileName,frames,frameRate):
    frames = [np.array(img,dtype=np.uint8) for img in frames]

    if fileName[-3:] == "gif":
        imageio.mimsave(fileName, frames, fps=frameRate,loop=0)
    else:
        imageio.mimsave(fileName, frames, fps=frameRate)



def calculateAmplitude(sources:list[tuple] = [(-3,0),(3,0)],width:float|int=10,resolution:int=256,sourceWavelength:float|int=2):
    
    center = (0,0)
    strengthPerPoint = 1/len(sources)
    increment = width / resolution
    initX , initY = center[0]-width/2 , center[1]+width/2
    x , y = initX , initY
    
    pix = []
    while (initY-y) < width:
        tempPix = []
        while (x-initX) < width:
            phases = []
            for emitter in sources:
                pointDistance = distance((x,y),(emitter))
                phases.append(2 * math.pi * (pointDistance % sourceWavelength) / sourceWavelength)
            
            pixelStrength = amplitudeFromPhase(*phases) * strengthPerPoint * 255
            
            tempPix.append((pixelStrength,pixelStrength,pixelStrength))
            x += increment
        
        pix.append(tempPix)
        
        x = initX
        y -= increment

    return pix



def calculateVideo(sources:list[tuple] = [(-3,0),(3,0)],width:float|int=10,resolution:int=256,sourceWavelength:float|int=2,numFrames:int=30,colourWave=False):
    
    center = (0,0)
    timeIncrement = (2*math.pi)/(numFrames+1)
    strengthPerPoint = 1/len(sources)
    increment = width / resolution
    initX , initY = center[0]-width/2 , center[1]+width/2
    x , y = initX , initY
    
    frames = []

    for frame in range(numFrames):
        x , y = initX , initY
        pix = []
        while (initY-y) < width:
            tempPix = []
            while (x-initX) < width:
                strength = 0
                for emitter in sources:
                    pointDistance = distance((x,y),(emitter))
                    strength += math.sin( (2 * math.pi * (pointDistance % sourceWavelength) / sourceWavelength) - (frame*timeIncrement) ) * strengthPerPoint
                if colourWave:
                    if strength >= 0:
                        pixStrength = strength * 255
                        tempPix.append((0,pixStrength,pixStrength))
                    else:
                        pixStrength = -strength * 255
                        tempPix.append((pixStrength,pixStrength/2,0))
                else:
                    pixelStrength = (strength + 1) * 127.5
                    tempPix.append((pixelStrength,pixelStrength,pixelStrength))
                
                x += increment
            
            pix.append(tempPix)
            
            x = initX
            y -= increment
            
        frames.append(pix)
        print(f"Frame {frame} done")

    return frames



def calculateSounds(sources:list[tuple] = [(-3,0),(3,0)],width:float|int=10,resolution:int=256,sourceWavelength:float|int=2,numFrames:int=30,framerate:int=15,colourWave:bool=False):
    
    ampFrame = calculateAmplitude(sources,width,resolution,sourceWavelength)
    saveImage("Amplitude.png",ampFrame)
    videoFrames =calculateVideo(sources,width,resolution,sourceWavelength,numFrames,colourWave)
    saveVideo("Sound.gif",videoFrames,framerate)
    
    print("All Done")