from SoundWaves import *
import keyboard
import os
import base64
import io

sources = [(0,0)]
hashSources = 4
activeSource = -1
wavelen = 2
height = 10

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

heightCommandMatch = {
    "up":-0.5,
    "down":0.5
}

print("Press ENTER to start")

key=""
while key != "esc":
    key = keyboard.read_key()
    if key.isnumeric():
        mode = "SRC"
        activeSource = int(key) -1
    elif key == "w":
        mode = "WAV"
    elif key == "h":
        mode = "HIG"
    elif key == "insert":
        sources.append((0,0))
    elif key == "delete":
        sources.remove(sources[-1])
    elif key in sourceCommandMatch.keys() and mode == "SRC":
        sources[activeSource] = tuple(map(sum, zip(sources[activeSource] , sourceCommandMatch[key])))
    elif key in waveCommandMatch.keys() and mode == "WAV":
        wavelen = round(wavelen+waveCommandMatch[key],1)
    elif key in heightCommandMatch.keys() and mode == "HIG":
        height = round(height+heightCommandMatch[key],1)
    elif key == "s":
        pixels = calculateAmplitude(sources,height,1080,wavelen)
        array = np.array(pixels,dtype=np.uint8)
        newImage = Image.fromarray(array)
        
        buffer = io.BytesIO()
        newImage.save(buffer, format="PNG")
        buffer.seek(0)
        b64_string = base64.b64encode(buffer.read()).decode("utf-8")
        
        with open("SavedSettings.md","a") as f:
            f.write(f"\n![AmplitudeMap](data:image/png;base64,{b64_string})\n\n```python\n# ---settings---\nWavelength: {wavelen}\nheight: {height}\nSources: {len(sources)}\n")
            
            for source in sources:
                f.write(f"    {source}\n")
            
            f.write("```\n\n---\n")
            
    saveImage("output.png",calculateAmplitude(sources,height,256,wavelen))
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"Wavelength: {wavelen}\nheight: {height}\nSources: {len(sources)}")
    for source in sources:
        print(f"    {source}")
        
    print(f"\nKeys:\n    1-9 : select Sources\n    w : select wavelength\n    h : select height\n    Insert/Delete : Add/Remove source\n    Arrows : Move/change values")
        