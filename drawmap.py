import pygame
pygame.init()
font = "couriernew"

class CanvasMap() :
    def __init__(self, canvasSize : tuple, roomSize : tuple, tilesize : int, colors : dict, mapvalues : list) -> None:
        '''canvasSize in pixels on screen (x,y)n,\n
        roomSize in pixels on screen,\n
        tilesize in pixels per tile,\n
        colors in a dict per map value in rgb format {'0' : [r,g,b]}, \n
        mapvalues in a nested list list'''
        canvaswidth : int = canvasSize[0] #amount of pixels that are shown in the x
        canvasheight : int = canvasSize[1] #amount of pixels that are shown in the y
        self.roomwidth : int = roomSize[0]
        self.roomheight : int = roomSize[1]
        self.tilesize : int = tilesize #the size of each tile in pixels
        self.colors : list = colors #a list with all colors in rgb format
        self.mapvalues : list = mapvalues #a nested list with all the values of the map
        
        self.canvas = pygame.display.set_mode((canvaswidth, canvasheight)) # initialise the canvas
        
        self.totalWidth = self.roomwidth//self.tilesize # calculate the amount of squares in the x direction
        self.totalLength = self.roomheight//self.tilesize # calculate the amount of squares in the y direction
        self.totalSquares = self.totalWidth*self.totalLength # total amount of squares

    def DrawSquare(self, xcoord : int, ycoord : int) -> None:
        "draws a square of the map on screen"
        pygame.draw.rect(self.canvas, self.colors[str(int(self.mapvalues[xcoord][ycoord]))], (xcoord*self.tilesize, ycoord*self.tilesize, self.tilesize, self.tilesize)) #draw the square on the canvas
    
    def DrawRect(self, rect, color : tuple) -> None:
        "draws a rectangle on screen"
        pygame.draw.rect(self.canvas, color, rect)

    def DrawText(self, text : str, coords : tuple, color : tuple = (0,0,0), fontsize : int = 18) -> None:
        "draws a text on screen"
        fontObject = pygame.font.SysFont(font, fontsize)
        textrect = fontObject.render(text, False, color) # make a rectangle for the text
        xposition = coords[0] - (fontsize//2) # take the position and center it to that position, otherwise it would be bottom right
        yposition = coords[1] - (fontsize//2) 
        self.canvas.blit(textrect, (xposition, yposition)) # place on screen
    
    def DrawFullMap(self) -> None:
        'draws the full map on the canvas'
        for i in range(self.totalSquares) : #repeat for every square
            xcoord = (i%self.totalWidth) #get the xcoordinate
            ycoord = (i//self.totalWidth) #get the ycoordinate
            self.DrawSquare(xcoord, ycoord)
    
            
        