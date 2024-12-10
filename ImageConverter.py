import LoadImage
colors = [(0,0,0)]
Colors = {}
def Load(imageName : str) -> list:
    "takes an image to output a list of numbers with asociated colors, these numbers make up the entire image. after running the list of colors can be optained via Colors"
    newList = []
    finalList = []
    image = LoadImage.Load(imageName) #get a nested list of the image

    imageRowAmount = len(image) #get the height of the image
    imageRowSize = len(image[0]) # get the width of the image
    image = [i for x in image for i in x] #very short way to flatten list
    for pixel in image :
        if pixel not in colors : # check if the color already exists
            colors.append(pixel)       

        index = colors.index(pixel) # find the number which corelates with the color
        newList.append(index) # add to the list of numbers

    #re-nest the list
    itemNumber = 0
    #reformat to a nested list and rotate it to its correct orientation
    for row in range(imageRowAmount) :
        finalList.append([]) #add the row
        for place in range(imageRowSize) :
            finalList[row].append(newList[itemNumber]) # add the item to the row
            itemNumber += 1
    finalList = list(zip(*finalList)) # rotate the list back to the original orientation

    for x in range(len(finalList)) :
        finalList[x] = list(finalList[x]) # make all parts of the list a list, not a tuple
        

    for color in range(len(colors)) :
        Colors[f"{color}"] = list(colors[color]) #the list of colors inside the image
    

    return finalList
