import math
import pygame

test = True
if test == False :
    import ArduinoTalk
class Navigation :
    def __init__(self, mapCanvas : list, startPosition : tuple, startAngle : int, canvas, json : object) -> None:
        self.mapCanvas : list = mapCanvas #the map
        self.position : list = list(startPosition) #current position
        self.angle : int = startAngle #orientation
        self.canvas = canvas #for drawing on the canvas
        self.lastDrawnPos = self.position
        self.json = json
        if test == False :
            motorSpeed = 110 #between 0 and 255
            forwardTime = 260 #in ms
            forwardStartTime = 400 #in ms
            forwardStopTime = 170 #in ms
            rotateTimeL = 600 #in ms
            rotateTimeR = 710 #in ms
            startTime = 100 #in ms
            motorAdjustment = 96 #in %
            sensStopDistance = 100 #in cm
            ArduinoTalk.Write(f"s{motorSpeed}")
            ArduinoTalk.Write(f"ft{forwardStartTime}")
            ArduinoTalk.Write(f"fp{forwardStopTime}")
            ArduinoTalk.Write(f"ff{forwardTime}")
            ArduinoTalk.Write(f"rl{rotateTimeL}")
            ArduinoTalk.Write(f"rr{rotateTimeR}")
            ArduinoTalk.Write(f"a{startTime}")
            ArduinoTalk.Write(f"m{motorAdjustment}")
            ArduinoTalk.Write(f"d{sensStopDistance}")
           
    def GoToPos(self, coords : tuple) -> None:
        "moves peter to a point on the map"
        currentPosition = self.position 
        endPosition = coords
        sides = 4 # amount of sides peter can drive, for now hardcoded to 4 for simplification (right, up, left, down)
        def FindDirection(startPosition : tuple) -> list:
            "makes the route from a to b"
            checkedPositions = [[startPosition, 0]]
            times = 0
            again = True
            while again :
                if times >= len(checkedPositions) :
                    print("No route could be found")
                    directions = None
                    break
                position = checkedPositions[times][0]
                oldDistance = checkedPositions[times][1] # take the amount of steps it took to get to that node
                possibleDirections = []
                def EstimateFurthestSide(positions : list, destination) -> int:
                    "returns the index of the furthest position"
                    highestdistance = [0, -1] # list with the distance and the index of that distance
                    #estimate distance using d(a, b) = sqrt((xb - xa)^2 +(yb - xb)^2)
                    for coordinate in range(len(positions)) :
                        distance = math.sqrt(math.pow((destination[0] - positions[coordinate][0]), 2) + math.pow((destination[1] - positions[coordinate][1]), 2))
                        if highestdistance[0] < distance : #check if the distance is further than the current furthest one
                            highestdistance = [distance, coordinate]
                    return highestdistance[1]
                
                def GetRoute() :
                    endDistance = checkedPositions[-1][1]
                    lastPosition = list(endPosition)
                    route = [lastPosition]
                    for i in range(endDistance) :
                        nextDistance = endDistance - i 
                        for side in range(sides) : # get all positions around the current position
                            if side == 0 :
                                position = [lastPosition[0] + 1, lastPosition[1]] #right
                            elif side == 1 :
                                position = [lastPosition[0], lastPosition[1] + 1] #up
                            elif side == 2 :
                                position = [lastPosition[0] - 1, lastPosition[1]] #left
                            elif side == 3 :
                                position = [lastPosition[0], lastPosition[1] - 1] #down
                            
                            #construct the route
                            for item in range(len(checkedPositions)) :
                                if checkedPositions[item][0] == position and checkedPositions[item][1] == nextDistance : #get the first ocurrance of the next distance that is borderd to the last point
                                    lastPosition = checkedPositions[item][0] # set the new old node for the next iteration
                                    route.append(lastPosition)
                                    self.mapCanvas[lastPosition[0]][lastPosition[1]] = 2 #change the map list 
                                    break
                            if position == lastPosition : #if the position is the destination then stop
                                self.mapCanvas[endPosition[0]][endPosition[1]] = 2 # add the destination too
                                break
                    route.reverse() #make the route the correct order
                    self.canvas.DrawFullMap()
                    pygame.display.update()
                    return route
                         
                for side in range(sides) : # get all positions around the current position
                    if side == 0 :
                        nextPosition = [position[0] + 1, position[1]] #right
                    elif side == 1 :
                        nextPosition = [position[0], position[1] + 1] #up
                    elif side == 2 :
                        nextPosition = [position[0] - 1, position[1]] #left
                    elif side == 3 :
                        nextPosition = [position[0], position[1] - 1] #down
                    if  nextPosition[0] >= 0 and nextPosition[1] >= 0 and nextPosition[0] < len(self.mapCanvas[0]) and nextPosition[1] < len(self.mapCanvas): #check if the position is in bounds
                        if self.mapCanvas[nextPosition[0]][nextPosition[1]] == 1 or self.mapCanvas[nextPosition[0]][nextPosition[1]] == 2 : #check if the position is in bounds
                            possibleDirections.append(nextPosition)

                if len(possibleDirections) >= 2 : # if there are 2 or more directions left remove 1
                    furthestDistanceIndex = EstimateFurthestSide(possibleDirections, endPosition)
                    possibleDirections.pop(furthestDistanceIndex)

                for item in range(len(possibleDirections)) :
                    oldamount = len(checkedPositions)
                    finalitem = oldamount
                    for i in range(oldamount) : #check if the item is already in the list
                        if possibleDirections[item] == checkedPositions[i][0] :
                            if checkedPositions[i][1] > oldDistance + 1 : # if the distance is shorter replace with the shorter one
                                checkedPositions[i][1] = oldDistance + 1
                            finalitem = i
                            break
                    if oldamount == finalitem : # if the loop is over add the new position and distance
                        checkedPositions.append([possibleDirections[item], oldDistance + 1])


                if list(endPosition) not in [x[0] for x in checkedPositions] : #if the endpostion is not in the list do another loop
                    times += 1
                else : #else finalise the route
                    again = False
                    directions = GetRoute()
            return directions
        
        def CreateInstructions(route) -> list:
            'create the final instructions to send to peter'
            rotation = self.angle
            instructions = []
            changes = []
            lastposition = self.position

            itemnumber = 0
            for item in route :
                itemnumber += 1
                xchange = item[0] - lastposition[0]
                ychange = item[1] - lastposition[1]
                if xchange == 1 : #right
                    if rotation == 0 :
                        instructions.append("left")
                        changes.append([0, 0])
                    elif rotation == 90 : 
                        if len(instructions) != 0 :
                            instructions.append("forward")
                    elif rotation == 180 :
                        instructions.append("right")
                        changes.append([0, 0])
                    elif rotation == 270 :
                        instructions.append("backward")
                        changes.append([0, 0])
                    if rotation != 90 :
                        try :
                            instructions.pop(-2)
                        except IndexError :
                            pass
                        else :
                            instructions.insert(-1, "forwardStop")
                        instructions.append("forwardStart")
                    rotation = 90

                elif ychange == 1 : #down
                    if rotation == 0 : 
                        if len(instructions) != 0 :
                            instructions.append("forward")
                    if rotation == 90 :
                        instructions.append("right")
                        changes.append([0, 0])
                    elif rotation == 180 :
                        instructions.append("backward")
                        changes.append([0, 0])
                    elif rotation == 270 :
                        instructions.append("left")
                        changes.append([0, 0])
                    if rotation != 0 :
                        try :
                            instructions.pop(-2)
                        except IndexError :
                            pass
                        else : 
                            instructions.insert(-1, "forwardStop")
                        instructions.append("forwardStart")
                    rotation = 0

                elif xchange == -1 : #left
                    if rotation == 0 :
                        instructions.append("right")
                        changes.append([0, 0])
                    elif rotation == 90 :
                        instructions.append("backward")
                        changes.append([0, 0])
                    elif rotation == 180 :
                        instructions.append("left")
                        changes.append([0, 0])
                    elif rotation == 270 :
                        if len(instructions) != 0 :
                            instructions.append("forward")
                    if rotation != 270 :
                        try :
                            instructions.pop(-2)
                        except IndexError :
                            pass
                        else :
                            instructions.insert(-1, "forwardStop")
                        instructions.append("forwardStart")
                    rotation = 270

                elif ychange == -1 : #up
                    if rotation == 0 :
                        instructions.append("backward")
                        changes.append([0, 0])
                    elif rotation == 90 :
                        instructions.append("left")
                        changes.append([0, 0])
                    elif rotation == 180 :
                        if len(instructions) != 0 :
                            instructions.append("forward")
                    elif rotation == 270 :
                        instructions.append("right")
                        changes.append([0, 0])
                    if rotation != 180 :
                        try :
                            instructions.pop(-2)
                        except IndexError :
                            pass
                        else :
                            instructions.insert(-1, "forwardStop")
                        instructions.append("forwardStart")
                    rotation = 180
                if len(instructions) == 0 :
                    instructions.append("forwardStart")
                lastposition = item
                changes.append([xchange, ychange]) #for the later use to make instructions
            instructions[-1] = "forwardStop" #append the final stop
            print(instructions)
            return instructions, changes
            
        def SendInstructions(instructions) -> None:
            "sends the instructions to the arduino and updates the map to where peter is"
            index = 0
            if test == False :
                ArduinoTalk.Write("reset") # reset any posible errors
            for item in instructions :
                if test == False :  # check if no breaks or errors have occured
                    ArduinoTalk.Write("1")
                    response = ArduinoTalk.Read()
                else :
                    response = "0"
            
                if response != "0" : # if the response gives an error stop everything
                    self.DrawPeter()
                    print("arduino error: the arduino has given an error, something might be too close")
                    break

                print(item)
                if test == False : #send the instruction and wait for reaction
                    ArduinoTalk.Write(item)
                    response = ArduinoTalk.Read()
                else :
                    pygame.time.wait(400)
                    response = "done"
                
                if response != "done" : #if the response is wrong give an error
                    print("response error: either conection got lost or messed up")
                    break
                if item == "0" : #this will always be the last item, to stop
                    continue

                if item == "forward" or item == "forwardStart" or item == "forwardStop":
                    self.position = route[index]
                    index += 1
                    self.DrawPeter()
                


                match changes[index-1] : # set the angle of peter to match the one on the map
                    case [1,0] :
                        self.angle = 90
                    case [0,1] :
                        self.angle = 0
                    case [-1,0] :
                        self.angle = 270
                    case [0,-1] :
                        self.angle = 180
                jsonSend = [self.position, self.angle]
                self.json.Change("peterLocation", jsonSend)

        route = FindDirection(currentPosition)
        if route != None : #check if no errors have orrured in the route making
            instructions, changes = CreateInstructions(route)
            SendInstructions(instructions)

    def DrawPeter(self) -> None:
        position = self.position
        self.mapCanvas[position[0]][position[1]] = 0
        self.mapCanvas[self.lastDrawnPos[0]][self.lastDrawnPos[1]] = 1
        self.canvas.DrawSquare(position[0], position[1])
        self.canvas.DrawSquare(self.lastDrawnPos[0], self.lastDrawnPos[1])

        self.lastDrawnPos = position
        self.canvas.UpdateScreen()


