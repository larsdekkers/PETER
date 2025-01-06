import math
class Navigation :
    def __init__(self, mapCanvas : list, startPosition : tuple, startAngle : int, canvas):
        self.mapCanvas : list = mapCanvas
        self.position : tuple = startPosition
        self.angle : int = startAngle
        self.canvas = canvas
    
    def GoTo(self, coords : tuple) :
        #oke f*ck dit is pittig, idee om een versie van A* te implementeren.
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
                    lastPosition = checkedPositions[-1][0]
                    route = [lastPosition]
                    for i in range(endDistance) :
                        nextDistance = endDistance - i 
                        for side in range(sides) : # get all positions around the current position
                            if side == 0 :
                                position = [lastPosition[0] + 1, lastPosition[1]]
                            elif side == 1 :
                                position = [lastPosition[0], lastPosition[1] + 1]
                            elif side == 2 :
                                position = [lastPosition[0] - 1, lastPosition[1]]
                            elif side == 3 :
                                position = [lastPosition[0], lastPosition[1] - 1]
                            
                            for item in range(len(checkedPositions)) :
                                if checkedPositions[item][0] == position and checkedPositions[item][1] == nextDistance :
                                    lastPosition = checkedPositions[item][0]
                                    route.append(lastPosition)
                                    self.canvas(2, (lastPosition[0], lastPosition[1]))
                                    break
                            if position == lastPosition :
                                break

                        
                
                for side in range(sides) : # get all positions around the current position
                    if side == 0 :
                        nextPosition = [position[0] + 1, position[1]]
                    elif side == 1 :
                        nextPosition = [position[0], position[1] + 1]
                    elif side == 2 :
                        nextPosition = [position[0] - 1, position[1]]
                    elif side == 3 :
                        nextPosition = [position[0], position[1] - 1]
                    if (self.mapCanvas[nextPosition[0]][nextPosition[1]] == 1 or self.mapCanvas[nextPosition[0]][nextPosition[1]] == 2) and nextPosition[0] >= 0 and nextPosition[1] >= 0 and nextPosition[0] < len(self.mapCanvas[0]) -1 and nextPosition[1] < len(self.mapCanvas) - 1:
                        possibleDirections.append(nextPosition)
                
                
                # if len(possibleDirections) >= 3 :
                #     furthestDistanceIndex = EstimateFurthestSide(possibleDirections, endPosition)
                #     possibleDirections.pop(furthestDistanceIndex) #dont add the furthest one

                if len(possibleDirections) >= 2 : # if there are 2 or more directions left remove 1 more
                    furthestDistanceIndex = EstimateFurthestSide(possibleDirections, endPosition)
                    possibleDirections.pop(furthestDistanceIndex)

                for item in range(len(possibleDirections)) :
                    oldamount = len(checkedPositions)
                    finalitem = oldamount
                    for i in range(oldamount) :
                        if possibleDirections[item] == checkedPositions[i][0] :
                            if checkedPositions[i][1] > oldDistance + 1 :
                                checkedPositions[i][1] = oldDistance + 1
                            finalitem = i
                            break
                    if oldamount == finalitem :
                        checkedPositions.append([possibleDirections[item], oldDistance + 1])


                if list(endPosition) not in [x[0] for x in checkedPositions] :
                    times += 1
                else :
                    again = False
                    GetRoute()
        FindDirection(currentPosition)





