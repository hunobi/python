from PIL import Image
from matplotlib import pyplot as plt
import numpy as np

def f(px):return np.sqrt(np.power(255-px[0],2)+np.power(255-px[1],2)+np.power(255-px[2],2))

def rysuj_funkcje(img):
    size = img.size
    x = [i for i in range(size[0])]
    y = [i for i in range(size[1])]
    z = []
    X, Y = np.meshgrid(x,y)
    for i in range(size[0]):
        temp = []
        for j in range(size[1]):
            rgb = img.getpixel((i,j))
            temp.append(f(rgb))
        z.append(temp)

    Z = (np.matrix(z)).T

    
    ax = plt.axes(projection='3d')
    #ax.contour3D(X,Y,z,round(np.sqrt(size[0]*size[1])))
    ax.plot_surface(X,Y,Z,rstride=1, cstride=1,cmap='viridis', edgecolor='none')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()

def kompresja(img:Image, k=2) -> Image:
    def get_neighbor(start:tuple, distance:int, size:tuple):
        ans = []
        for i in range(distance):
            for j in range(distance):
                if start[0]+i < size[0] and start[1]+j < size[1]:
                    ans.append((start[0]+i,start[1]+j))
        return ans
    size = (img.size[1], img.size[0])
    img_org = np.array(img)
    new_img = np.array(img)

    for i in range(0,size[0], k//2):
        for j in range(0, size[1],k//2):
            pixels = []
            for pos in get_neighbor((i,j),k, size): 
                pixels.append(img_org[pos[0]][pos[1]])
            px_size = len(pixels)
            r = sum([pixels[i][0] for i in range(px_size)])//px_size
            g = sum([pixels[i][1] for i in range(px_size)])//px_size
            b = sum([pixels[i][2] for i in range(px_size)])//px_size
            for pos in pixels:new_img[i][j] = (r,g,b)       
    return Image.fromarray(new_img)

class Filters:
    def Negative(img) -> Image:
        img_array = np.array(img)
        img_new = np.array(img)
        size = (img.size[1], img.size[0])
        for i in range(size[0]):
            for j in range(size[1]):
                pixels = [255-px for px in img_array[i][j]]
                img_new[i][j] = tuple(pixels)
        return Image.fromarray(img_new)
    def Gray(img, mode=0):
        img_array = np.array(img)
        img_new = np.array(img)
        size = (img.size[1], img.size[0])
        for i in range(size[0]):
            for j in range(size[1]):
                g = 0
                if mode == 1:
                    g = (0.299*int(img_array[i][j][0]) + 0.587*int(img_array[i][j][1]) + 0.114*int(img_array[i][j][2]))
                else:
                    g = (int(img_array[i][j][0]) + int(img_array[i][j][1]) + int(img_array[i][j][2]))/3
                pixels = [g,g,g]
                img_new[i][j] = tuple(pixels)
        return Image.fromarray(img_new)
    
    def BlackAndWhite(img) -> Image:
        img_array = np.array(img)
        img_new = np.array(img)
        size = (img.size[1], img.size[0])
        for i in range(size[0]):
            for j in range(size[1]):
                pixels = []
                #for px in img_array[i][j]:
                #    if px < 255-px: pixels.append(0)
                #    else: pixels.append(255)
                if img_array[i][j][1] < 255-img_array[i][j][1]: pixels = [0,0,0]
                else: pixels = [255,255,255]
                img_new[i][j] = tuple(pixels)
        return Image.fromarray(img_new)

if __name__ == "__main__":
    img = Image.open("kot.jpg").convert("RGB")
    #img_k = kompresja(img,10)
    img_k = Filters.Gray(img)
    img_k.save("gray4.jpg")
