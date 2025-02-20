import pygame #for handeling most inputs and the window
import drawmap # module for plotting on the pycanvas
import ImageConverter # module for creating a list of colors from a png/jpg
import Widgetmanager # module for eazy creation of widgets
import PeterNav
import JsonHandeler

pygame.init()

canvasWidth : int = 600
canvasHeight : int = 680

jsonName = "test.json"
image = '' #fill this in yourself
running = True
selectedColor = 0
roomSize = [0,0]
peterPos = [20,48]
datafile = {}

json = JsonHandeler.Json(jsonName)

def Dataread() -> None:
    'get all data out of a jsonfile'
    global colors
    global datafile
    global roomMap
    global roomSize
    global squaresize
    global colorNames
    global peterPos
    datafile = json.Open()
    colors = datafile['colors'] #get the colors
    roomMap = datafile['map']
    squaresize = (canvasWidth - 50)//len(roomMap[0])
    roomSize[0] = len(roomMap)*squaresize
    roomSize[1] = len(roomMap[0])*squaresize
    colorNames = datafile["colorNames"]
    peterPos = datafile['peterLocation']

def DataStore() -> None:
    'put data into a json file'
    datafile['timesrun'] = datafile['timesrun'] + 1
    datafile['colors'] = colors
    datafile['peterLocation'] = navigation.position

    
    datafile["colorNames"] = colorNames
    datafile['map'] = roomMap

    itemnumber = 0
    for inputBox in Widgetmanager.widgets :#for all inputboxes
        if type(inputBox[1]).__name__ == "InputBox" :
            colorNames[str(SelectedColorTextboxes[itemnumber])] = inputBox[1].text
            itemnumber += 1
    json.Store(datafile)
            
 

def Initialisemap() -> None:
    "only run when resetting the map to the original image"
    global roomMap
    global roomSize
    global colors
    global squaresize
    global colorNames
    global datafile
    global navigation
    global canvas
    global peterPos
    

    roomMap = ImageConverter.Load(image)
    colors = ImageConverter.Colors
    squaresize = (canvasWidth - 50)//len(roomMap[0])
    roomSize[0] = len(roomMap)*squaresize #getting the width of the map
    roomSize[1] = len(roomMap[0])*squaresize # getting the height of the map
    colorNames = {} 
    colorNames["0"] = "wall"
    colorNames["1"] = "path"
    colorNames["2"] = "route"
    peterPos  = [20,48]
    for colorNumber in range(len(colors)-3) :
        colorNumber += 3
        colorNames[f"{colorNumber}"] = ""

def PixelToSquare(x : int,y : int) -> tuple:
    "converts pixelcoordinates to coordinates on the map"
    xsquare = x//squaresize
    ysquare = y//squaresize
    return xsquare, ysquare

def ChangeMap(item : int, coords : tuple) -> None:
    "change a squares value"
    roomMap[coords[0]][coords[1]] = item #change the map list 
    canvas.DrawSquare(coords[0], coords[1]) # draw the new square

def MouseDown(mousebutton) -> None:
    "all events to happen when mousebutton 1 is down"
    x,y = pygame.mouse.get_pos() # get the position of the mouse
    if x <= roomSize[0] and y <= roomSize[1] : # if the mouse is on the map
        xsquare, ysquare = PixelToSquare(x,y) # convert to a position in the grid
        navigation.GoTo((xsquare,ysquare))
        ChangeMap(selectedColor, (xsquare,ysquare)) # change the squares value

    Widgetmanager.CheckForClick(x,y, mousebutton) # checks all widgets for clicks

def KeyDown(event) -> None:
    letter = event.unicode
    if Widgetmanager.textboxActive == True :
        Widgetmanager.TextInput(letter)
    if letter == "=" :
        ChangeSelectedColor(selectedColor+1)
    elif letter == "-" :
        ChangeSelectedColor(selectedColor-1)

def ResetMap() -> None:
    "resets the map back to the original image"
    Initialisemap()
    canvas.mapvalues = roomMap
    navigation.mapCanvas = roomMap
    navigation.position = peterPos
    canvas.DrawFullMap()

def ChangeSelectedColor(color) -> None:
    "changes the selected color and displays it on the canvas"
    global selectedColor
    color = max(color, 0) # make sure it cant go below 0
    color = min(color, len(colors)-1) # make sure it cant go above the amount of colors
    selectedColor = color
    canvas.DrawRect(colorRect, colors[f"{color}"])

def ChangeColorItemLower(text) -> None:
    ChangeItemTextbox(False, text)

def ChangeColorItemHigher(text) -> None:
    ChangeItemTextbox(True, text)

def ChangeItemTextbox(state : bool, text) -> None:
    "changes the item of the textboxes when clicked on them"
    textboxnumber = len(text) # this indicates what textbox to use
    if textboxnumber == 0 :
        textboxcolor = textbox1Color
        textbox = textbox1
    elif textboxnumber == 1 :
        textboxcolor = textbox2Color
        textbox = textbox2
    elif textboxnumber == 2 :
        textboxcolor = textbox3Color
        textbox = textbox3
    elif textboxnumber == 3 :
        textboxcolor = textbox4Color
        textbox = textbox4
    color = textboxcolor.color # get the color of the textbox
    index = int(list(colors.keys())[list(colors.values()).index(color)]) # find the colorindex
    
    if state == False :
        color = min(index +1,len(colors)-1) # make sure it cant go above or under the amount of colors
    else :
        color = max(index-1, 0)

    textboxcolor.color = colors[str(color)] # change the color in the widget
    textboxcolor.ClickColorChange() #draw the actual color
    colorNames[str(SelectedColorTextboxes[textboxnumber]) ] = textbox.text # change the name in the list of names

    SelectedColorTextboxes[textboxnumber] = color # set the selected color in a list to check eazier later

    textbox.text = colorNames[f"{color}"] #change the textbox to have the correct text
    textbox.Clicked(False) # deselect and update the textbox
    
Dataread()
#Initialisemap()
canvas = drawmap.CanvasMap((canvasWidth, canvasHeight), roomSize, squaresize, colors, roomMap) # the canvas
navigation = PeterNav.Navigation(roomMap, peterPos, 0, canvas)
ChangeMap(0, peterPos)
canvas.DrawFullMap()
resetButton = Widgetmanager.Button((canvasWidth-50,canvasHeight-50), (50,50), (255,0,0), canvas, ResetMap, "reset")
colorRect = pygame.Rect(canvasWidth-50, 0, 50, 50) # the rectangle that shows the selected color

canvas.DrawRect(colorRect, colors[f"{selectedColor}"]) # drawing the color
canvas.DrawText("use + and - to draw different colors", (canvasWidth//2-180, roomSize[1]+25), (255,255,255)) # drawing text with instructions

textbox1 = Widgetmanager.InputBox((30, canvasHeight-80), (150,30), canvas, 13, colorNames["0"]) # all textboxes for handeling items
textbox2 = Widgetmanager.InputBox((30, canvasHeight-40), (150,30), canvas, 13, colorNames["1"])
textbox3 = Widgetmanager.InputBox((270, canvasHeight-80), (150,30), canvas, 13, colorNames["2"])
textbox4 = Widgetmanager.InputBox((270, canvasHeight-40), (150,30), canvas, 13, colorNames["3"])

textbox1Color = Widgetmanager.Button((180,canvasHeight-80), (30,30), colors["0"], canvas, ChangeColorItemLower, "", ChangeColorItemHigher, True) # all colors next to the textboxes for items
textbox2Color = Widgetmanager.Button((180,canvasHeight-40), (30,30), colors["1"], canvas, ChangeColorItemLower, " ", ChangeColorItemHigher, True) # text is for checking the corresponding textbox
textbox3Color = Widgetmanager.Button((420,canvasHeight-80), (30,30), colors["2"], canvas, ChangeColorItemLower, "  ", ChangeColorItemHigher, True)
textbox4Color = Widgetmanager.Button((420,canvasHeight-40), (30,30), colors["3"], canvas, ChangeColorItemLower, "   ", ChangeColorItemHigher, True)



SelectedColorTextboxes = [0,1,2,3]
while running :
    event = canvas.UpdateScreen()
    if event == None :
        continue
    print(event.type)
    if event.type == 32787:
        running = False

    #check all mouse inputs
    elif event.type == pygame.MOUSEBUTTONDOWN :
        if pygame.mouse.get_pressed(num_buttons=3)[0] == True or pygame.mouse.get_pressed(num_buttons=3)[2] == True : # check if the left mouse button has been pressed
            MouseDown(pygame.mouse.get_pressed(num_buttons=3).index(True)+1)

    #check all keyboard inputs        
    elif event.type == pygame.KEYDOWN :
        KeyDown(event)

DataStore() # save all changes

 
