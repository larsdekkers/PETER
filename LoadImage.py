from PIL import Image
def Load(imageName : str) -> list:
    "returns a nested list with rbg values [y][x](r,g,b)"
    image = Image.open(f'C:/Users/2007080801/OneDrive - Rodenborch College/Math/Peter/{imageName}') #change path for it to work for you

    pixels = list(image.getdata()) #get color data in a flat list
    width, height = image.size
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)] # convert to nested list to return

   #remove the opacity because it is not needed
    for row in range(len(pixels)) :
        for item in range(len(pixels[row])) :
            pixels[row][item] = pixels[row][item][:-1] #remove the last element of all items
    return pixels
