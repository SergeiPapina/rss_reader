import climage

from image_to_ascii import ImageToAscii
from PIL import Image
from simshow import simshow

# imagePath is for path of the image you want to convert to Ascii
# outputFile is for the file path of where the generated Ascii art
# should be stored keep None if you don't want to store it in a .txt file
#ImageToAscii(imagePath="17feb8db333cd7844b90c628fc62c22b.jpg", outputFile="output.txt")
ImageToAscii(imagePath="17feb8db333cd7844b90c628fc62c22b.jpg")



# converts the image to print in terminal
# with 8 color encoding and palette tango
output = climage.convert('17feb8db333cd7844b90c628fc62c22b.jpg', palette='gruvbox', is_256color=False, is_truecolor=True)
#output = climage.convert('17feb8db333cd7844b90c628fc62c22b.jpg', palette='linuxconsole', is_256color=False, is_truecolor=True)

# prints output on console.
print(output)

img = Image.open('17feb8db333cd7844b90c628fc62c22b.jpg')
img.show()

simshow('17feb8db333cd7844b90c628fc62c22b.jpg')  # display from local file
#simshow('http://mathandy.com/escher_sphere.png')  # display from url
