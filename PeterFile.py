import pygame #for handeling most inputs and the window
import json # for storing data between uses
import drawmap # module for plotting on the pycanvas
import ImageConverter # module for creating a list of colors from a png/jpg
import Widgetmanager # module for eazy creation of widgets

pygame.init()

canvasWidth : int = 600
canvasHeight : int = 700

jsonName = "test.json"
image = "testwinkel.png"
running = True
selectedColor = 0
roomSize = [0,0]
datafile = {}

def Dataread() :
    'get all data out of a jsonfile'
    global colors
    global datafile
    global roomMap
    global roomSize
    global squaresize
    global inputBoxes
    with open(jsonName) as fp: #open the jsonfile
        datafile = json.load(fp)
    colors = datafile['colors'] #get the colors
    roomMap = datafile['map']
    squaresize = (canvasWidth - 50)//len(roomMap[0])
    roomSize[0] = len(roomMap)*squaresize
    roomSize[1] = len(roomMap[0])*squaresize
    inputBoxes = datafile["InputBoxes"]

def DataStore() :
    'put data into a json file'
    datafile['timesrun'] = datafile['timesrun'] + 1

    datafile['colors'] = colors
    
    inputboxes = {}
    itemnumber = 0
    for inputBox in Widgetmanager.widgets :
        if type(inputBox[1]).__name__ == "InputBox" :
            inputboxes[str(itemnumber)] = inputBox[1].text
            itemnumber += 1
    
    datafile["InputBoxes"] = inputboxes
    datafile['map'] = roomMap
    
            
    with open(jsonName, "w") as outfile : # save the json with updated info
        json.dump(datafile, outfile)

def Initialisemap() :
    "only run when resetting the map to the original image"
    global roomMap
    global roomSize
    global colors
    global squaresize
    global inputBoxes
    global datafile
    roomMap = ImageConverter.Load(image)
    colors = ImageConverter.Colors
    squaresize = (canvasWidth - 50)//len(roomMap[0])
    roomSize[0] = len(roomMap)*squaresize #getting the width of the map
    roomSize[1] = len(roomMap[0])*squaresize # getting the height of the map
    inputBoxes = {}
    inputBoxes["0"] = "wall"
    inputBoxes["1"] = "path"
    textbox1.text = inputBoxes["0"]
    textbox2.text = inputBoxes["1"]

def PixelToSquare(x : int,y : int)  -> tuple:
    "converts pixelcoordinates to coordinates on the map"
    xsquare = x//squaresize
    ysquare = y//squaresize
    return xsquare, ysquare

def ChangeMap(item : int, coords : tuple) :
    "change a squares value"
    roomMap[coords[0]][coords[1]] = item #change the map list 
    Drawmap.DrawSquare(coords[0], coords[1]) # draw the new square

def Mouse1Down() :
    "all events to happen when mousebutton 1 is down"
    x,y = pygame.mouse.get_pos() # get the position of the mouse
    if x <= roomSize[0] and y <= roomSize[1] : # if the mouse is on the map
        xsquare, ysquare = PixelToSquare(x,y) # convert to a position in the grid
        ChangeMap(selectedColor, (xsquare,ysquare)) # change the squares value

    Widgetmanager.CheckForClick(x,y) # checks all widgets for clicks

def KeyDown(event) :
    letter = event.unicode
    if Widgetmanager.textboxActive == True :
        Widgetmanager.TextInput(letter)
    if letter == "=" :
        ChangeSelectedColor(selectedColor+1)
    elif letter == "-" :
        ChangeSelectedColor(selectedColor-1)

def ResetMap() :
    "resets the map back to the original image"
    Initialisemap()
    Drawmap.mapvalues = roomMap
    Drawmap.DrawFullMap()

def ChangeSelectedColor(color) :
    "changes the selected color and displays it on the canvas"
    global selectedColor
    color = max(color, 0) # make sure it cant go below 0
    color = min(color, len(colors)-1) # make sure it cant go above the amount of colors
    selectedColor = color
    Drawmap.DrawRect(colorRect, colors[f"{color}"])


Dataread()
Drawmap = drawmap.CanvasMap((canvasWidth, canvasHeight), roomSize, squaresize, colors, roomMap) # the canvas
Drawmap.DrawFullMap()
resetButton = Widgetmanager.Button((canvasWidth-50,0), (50,50), (255,0,0), Drawmap, ResetMap, "reset")
colorRect = pygame.Rect(canvasWidth-50, 50, 50, 50) # the rectangle that shows the selected color

Drawmap.DrawRect(colorRect, colors[f"{selectedColor}"]) # drawing the color
Drawmap.DrawText("use + and - to draw different colors", (canvasWidth//2-180, roomSize[1]+25), (255,255,255)) # drawing text with instructions

textbox1 = Widgetmanager.InputBox((30, canvasHeight-100), (150,30), Drawmap, 13, inputBoxes["0"])
textbox2 = Widgetmanager.InputBox((30, canvasHeight-60), (150,30), Drawmap, 13, inputBoxes["1"])

textbox1Color = Drawmap.DrawRect(pygame.Rect(180,canvasHeight-100,30,30), colors["0"])
textbox2Color = Drawmap.DrawRect(pygame.Rect(180,canvasHeight-60,30,30), colors["1"])

while running :
    pygame.display.update()
    for event in pygame.event.get():
        #check if the red cross has been clicked
        if event.type == pygame.QUIT:
            running = False
        
        #check all mouse inputs
        elif event.type == pygame.MOUSEBUTTONDOWN :
           if pygame.mouse.get_pressed(num_buttons=3)[0] == True : # check if the left mouse button has been pressed
                Mouse1Down()
        
        #check all keyboard inputs        
        elif event.type == pygame.KEYDOWN :
            KeyDown(event)
    
    pygame.time.Clock().tick(30) # limit the fps to 30 to decrease pc load
DataStore() # save all changes
 