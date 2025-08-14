from SoundWaves import *
import keyboard
import os

sources = [(0,0)]
hashSources = 4
activeSource = -1
wavelen = 2

mode = "NONE"

sourceCommandMatch = {
    "up":(0,0.5),
    "down":(0,-0.5),
    "left":(-0.5,0),
    "right":(0.5,0)
}
waveCommandMatch = {
    "up":0.1,
    "down":-0.1,
}

key=""
while key != "esc":
    key = keyboard.read_key()
    if key.isnumeric():
        mode = "SRC"
        activeSource = int(key) -1
    elif key == "w":
        mode = "WAV"
    elif key == "insert":
        sources.append((0,0))
    elif key == "delete":
        sources.remove(sources[-1])
    elif key in sourceCommandMatch.keys() and mode == "SRC":
        sources[activeSource] = tuple(map(sum, zip(sources[activeSource] , sourceCommandMatch[key])))
    elif key in waveCommandMatch.keys() and mode == "WAV":
        wavelen += waveCommandMatch[key]
    
    saveImage("output.png",calculateAmplitude(sources,10,256,wavelen))
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"Wavelength: {wavelen}")
    print("Sources:")
    for i in sources:
        print(i)