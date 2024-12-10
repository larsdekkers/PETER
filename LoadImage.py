from PIL import Image
def Load(imageName : str) -> list:
    "returns a nested list with rbg values [y][x](r,g,b)"
    image = Image.open(f'C:/Users/2007080801/OneDrive - Rodenborch College/Math/Peter/{imageName}')

    pixels = list(image.getdata()) #get data in a list
    width, height = image.size
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)] # convert to nested list

   #remove the opacity
    for row in range(len(pixels)) :
        for item in range(len(pixels[row])) :
            pixels[row][item] = pixels[row][item][:-1]
    return pixels
