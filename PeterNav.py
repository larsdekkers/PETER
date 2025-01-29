import math
import ArduinoTalk
class Navigation :
    def __init__(self, mapCanvas : list, startPosition : tuple, startAngle : int, canvas):
        self.mapCanvas : list = mapCanvas
        self.position : tuple = startPosition
        self.angle : int = startAngle
        self.canvas = canvas
    
    def GoTo(self, coords : tuple) :
        currentPosition = self.position 
        endPosition = coords
        sides = 4 # amount of sides peter can drive, for now hardcoded to 4 for simplification (right, up, left, down)
        def FindDirection(startPosition : tuple):
            checkedPositions = [[startPosition, 0]]
            times = 0
            again = True
            while again :
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
                                    self.canvas(2, (lastPosition[0], lastPosition[1])) #display on canvas
                                    break
                            if position == lastPosition : #if the position is the destination then stop
                                break
                    route.reverse() #make the route the correct order
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
                
                
                # if len(possibleDirections) >= 3 :
                #     furthestDistanceIndex = EstimateFurthestSide(possibleDirections, endPosition)
                #     possibleDirections.pop(furthestDistanceIndex) #dont add the furthest one

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
        
        def SendDirection(route) :
            for item in route :
                ArduinoTalk.Write(item)
        route = FindDirection(currentPosition)
        SendDirection(route)





