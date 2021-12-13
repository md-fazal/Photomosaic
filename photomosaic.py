from PIL import Image
import glob
import math


def initialze_pixelarr(img, width, height):
    """
    produces a 2d list containing image pixel in format (r,g,b)
    goes from left to right and top to bottom covering each pixel

    tuple -> list
    """

    L = []
    for i in range(height):
        M = []
        for j in range(width):
            M.append(img.getpixel((j,i)))
        L.append(M)
    return L

def pixellate(img, w1, h1):
    """ pixellate the image where size of each visible quare is w1*h1
        img object -> img object
    """
    w, h = img.size
    img = img.resize((w1, h1))
    return img.resize((w//2,h//2))

def image_average(img):
    """produces the average rgb value for an image in form of (r, g, b)
    img_obj -> tuple
    """
    img = img.resize((10,10))
    width, height = img.size
    rgb_avg = [0, 0, 0]
    for i in range(height):
        for j in range(width):
            rgb = img.getpixel((j,i))
            rgb_avg[0] += rgb[0]//(height*width)
            rgb_avg[1] += rgb[1]//(height*width)
            rgb_avg[2] += rgb[2]//(height*width)
    return tuple(rgb_avg)

def color_distance(rgb1, rgb2):
    """ takes two tuple in the form (r, g, b) and produces the color distance between those
        tuple -> int 
    """
    distance = abs(math.sqrt((rgb1[0] - rgb2[0])**2 + (rgb1[1] - rgb2[1])**2 + (rgb1[2] - rgb2[2])**2))
    return distance

#open input image
img = Image.open("input image4.jpg").convert("RGB")

#length and with of each tile
tile_w = 30
tile_h = 30
img = pixellate(img,tile_w, tile_h)
w, h = img.size
rgbarr = initialze_pixelarr(img, w, h)

#load source images
source_img_list = []
img_avgrgb = []
#path where source images are located
path1 = "D:/Fazal/faces/*"
count = 0
for file in glob.iglob(path1):
    try:
        source_img = Image.open(file).convert("RGB")
        source_img_list.append(source_img)
        img_avgrgb.append(image_average(source_img))
    except:
        pass

for y in range((h//tile_h)):
    y = y*tile_h
    for x in range((w//tile_w)):
        x = x*tile_w
        try:
            color1 = img.getpixel((x,y))
            least_distance = color_distance(color1, image_average(source_img_list[0]))
            count = 0
            for image in source_img_list:
                color2 = img_avgrgb[source_img_list.index(image)]
                d = color_distance(color1, color2)
                if least_distance > d:
                    least_distance = d
                    index = count
                count += 1  
            img.paste(source_img_list[index].resize((tile_w,tile_h)), (x, y))
        except:
            print(y)
    img.show()

img.save("result")
img.show()