import pygame
buttonclicktime = 100
widgets = [] # a list with the position of all widgets and their class [widget, widgettype]
textboxActive = False

def CheckForClick(mouseposx : int, mouseposy : int, mousebutton : int) -> None:
    if mousebutton == 1 :
        global textboxActive
        selected = False # a bool that indicates if any widget has been selected this click
        for widget in widgets :
            if widget[0].collidepoint((mouseposx, mouseposy)) :
                widget[1].Clicked(True) # run all functions for the selected widget
                if type(widget[1]).__name__ == "InputBox" :
                    textboxActive = True
                    selected = True
                else :
                    textboxActive = False
            else : 
                if selected == False : #check if no other itemboxes have been selected
                    textboxActive = False
                widget[1].Clicked(False)
    if mousebutton == 3 :
        for widget in widgets :
            if widget[0].collidepoint((mouseposx, mouseposy)) :
                if type(widget[1]).__name__ == "Button" :
                    widget[1].Clicked(True, 3)

def TextInput(input : str) -> None:
    for widget in widgets :
        if type(widget[1]).__name__ == "InputBox" :
            if widget[1].selected == True :
                widget[1].ChangeText(input) 

class Button :
    def __init__(self, position : tuple, buttonSize : tuple, color : tuple, canvas : object, buttonFunction, text : str = "", buttonfunction2 = None, returnButtonText : bool = False) -> None:
        '''position in (x,y) with topleft anchor\n
        buttonSize in (x,y)\n
        color in RGB\n
        canvas in drawmap object\n
        buttonFunction in functionname without ()'''
        self.color = color
        self.canvas = canvas
        self.function = buttonFunction
        self.text = text
        self.returnButtonText = returnButtonText

        if buttonfunction2 == None : #check if there is a second function for right click, if not make the first function run
            self.function2 = buttonFunction
        else :
            self.function2 = buttonfunction2

        self.buttonRect = pygame.Rect(position[0], position[1], buttonSize[0],buttonSize[1]) #create the rectangle
        self.size = [position[0], position[1], buttonSize[0], buttonSize[1]]
        self.canvas.DrawRect(self.size, self.color) #draw the background color
        self.Textoperation() #draw the text on screen
        widgets.append((self.buttonRect, self)) # add to the list of all widgets
        
    def Clicked(self, state : bool, button = 1) -> None:
        "all events to happen when a click occurs"
        if state and button == 1:
            self.ClickColorChange()
            if self.returnButtonText == True :
                self.function(self.text)
            else :
                self.function() #run the buttons main function
                
        if state and button == 3:
            self.ClickColorChange()
            if self.returnButtonText == True :
                self.function2(self.text)
            else :
                self.function2() # run the secondary function
    
    def ClickColorChange(self) -> None:
        "change color of the button for a set amount of time"
        #set the color to a be little darker to indicate a click 
        self.canvas.DrawRect(self.size, (max(self.color[0]- 50, 0), max(self.color[1]- 50, 0), max(self.color[2]- 50, 0))) # draw color a little darker when clicked
        self.Textoperation() #make sure the text stays on top
        pygame.display.update() # show the screen
        pygame.time.delay(buttonclicktime) 
        self.canvas.DrawRect(self.size, self.color) # draw the original color again
        self.Textoperation()

    def Textoperation(self)  -> None :
        "calculate the start point for the text and display it"
        xposition = self.size[0] + self.size[2]//2 - len(self.text) * 3.5 #start at the middle of the button and move 2 to the left for each caracter
        yposition = self.size[1] + self.size[3]//2 #start at the middle of the button
        self.canvas.DrawText(self.text,(xposition, yposition))

class InputBox :
    def __init__(self, position : tuple, size : tuple, canvas : object, fontsize : int = 18, text : str = "") -> None:
        self.selected : bool = False
        self.canvas = canvas
        self.text = text
        self.fontsize = fontsize

        self.textBoxRect = pygame.Rect(position[0], position[1], size[0], size[1]) # intialise the rectangle
        self.textposition = self.textBoxRect[0]+20, self.textBoxRect[1]+ self.textBoxRect[3]//2 #change the position to center it
        
        self.canvas.DrawRect(self.textBoxRect, (50,50,50)) #draw the background color of the textbox
        self.ChangeText("")
        widgets.append((self.textBoxRect, self)) # add to list of all widgets

    def Clicked(self, state) -> None:
        'standard function to run all comands on a click'
        self.ChangeState(state) 
    
    def ChangeState(self, state) -> None:
        if state == False :
            self.canvas.DrawRect(self.textBoxRect, (50,50,50))
            self.canvas.DrawText(self.text, self.textposition, (255,255,255), self.fontsize) # make sure the text doesnt dissapear when unselecting
        if state == True :
            self.canvas.DrawRect(self.textBoxRect, (70,70,70))
            self.canvas.DrawText(self.text, self.textposition, (255,255,255), self.fontsize) # same with selecting
        self.selected = state
    
    def ChangeText(self, input : str) -> None:
        if input == '\x08' :
            self.text = self.text[:-1] # remove the last character when backspace is pressed
            self.canvas.DrawRect(self.textBoxRect, (70,70,70)) # clear the textbox in order to remove the letter
        else :
            if len(self.text) < (self.textBoxRect[2] // (self.fontsize//1.3)) : # set a max amount of characters
                self.text = self.text + input # add the new character to the text
        self.canvas.DrawText(self.text, self.textposition, (255,255,255), self.fontsize) # update the screen

