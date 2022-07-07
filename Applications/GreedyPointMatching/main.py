# Algorytm zachłannego dopasowania punktu
import math
import matplotlib.pyplot as plt
import os

def miara_manhatan(x1,y1, x2, y2):
    return abs(x1-x2) + abs(y1-y2)

def miara_euklides(x1,y1,x2,y2):
    return math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))

def miara_niepodobienstwa(BA, BB) -> float:
    BC = []
    for x_1 in range(len(BA)):
        temp = []
        for y_1 in range(len(BA[x_1])):
            if BA[x_1][y_1] == 1:
                odl_min = math.inf
                if BB[x_1][y_1] == 1:
                    odl_min = 0
                    continue
                for x_2 in range(len(BB)):
                    for y_2 in range(len(BB[x_2])):
                        if BB[x_2][y_2] == 1:
                            odl_akt = miara_euklides(x_1,y_1, x_2, y_2)                            
                            odl_min = min(odl_min, odl_akt)
                temp.append(odl_min)
            else:
                temp.append(0)
        BC.append(temp)
    miara = 0
    for i in BC:
        miara = miara + sum(i)
    return miara

def miara_podobienstwa_obustronnego(BA,BB) -> float:
    return (-1 * miara_niepodobienstwa(BA,BB)) - miara_niepodobienstwa(BB,BA)

def wyswietl(A, B, miara):
    plt.subplot(1,2,1)
    plt.title("Bitmapa testowa")
    plt.imshow(A,cmap='binary', interpolation='nearest')
    plt.subplot(1,2,2)
    
    plt.title("Bitmapa wzorcowa")
    plt.imshow(B,cmap='binary', interpolation='nearest')

    plt.suptitle("Miara: " + str(miara))
    plt.show()


def load_bitmap_test(path):
    ans = []
    with open(path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.replace("\n", "")
            line = line.split(' ')
            line = [int(i) for i in line]
            ans.append(line)
    return ans

def load_bitmap_wz(path):
    ans = []
    files = os.listdir(path)
    for file in files:
        if file != "test.txt":
            data = []
            with open(path+'/'+file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.replace("\n", "")
                    line = line.split(' ')
                    line = [int(i) for i in line]
                    data.append(line)
            ans.append(data)
    return ans


if __name__ == "__main__":

    testowa = load_bitmap_test('bitmaps/test.txt')
    wzorce = load_bitmap_wz('bitmaps')
    
    ans = []
    for item in wzorce:
        ans.append(miara_podobienstwa_obustronnego(testowa, item))
    
    miara = max(ans)
    index = ans.index(miara)
    print(ans)
    wyswietl(testowa, wzorce[index], miara)

