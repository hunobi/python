# Hubert Koloska - Siec Hopfielda
import os
import random
import matplotlib.pyplot as plt

# wczytanie bitmapy testowe
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

# wczytanie bitmapy wzorcowej
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

def wyswietl(A, B):
    plt.subplot(1,2,1)
    plt.title("Bitmapa testowa")
    plt.imshow(A,cmap='binary', interpolation='nearest')
    plt.subplot(1,2,2)
    
    plt.title("Bitmapa po naprawie")
    plt.imshow(B,cmap='binary', interpolation='nearest')

    plt.suptitle("Siec Hopfielda")
    plt.show()


class HopfieldNetwork:
    def __init__(self, n=5, m=5, random_weights=False):
        self.Size = (n,m)
        self.Weights = self.init_weights_matrix(random_weights)
        self.Bitmaps_learned = []
        self.Bitmaps_raw = []
    
    # tworze poczatkowe wagi
    def init_weights_matrix(self, random_weights):
        ans = []
        size = self.Size[0] * self.Size[1]
        for i in range(size):
            temp = []
            for j in range(size):
                if random_weights: temp.append(random.random()/100)
                else: temp.append(0)
            ans.append(temp)
        return ans

    # tworze wektor [-1;1] z bitmapy
    def get_vector_from_bitmap(self, bitmap) -> list:
        v = []
        for i in bitmap:
            for j in i:
                if j == 0:v.append(-1)
                else:v.append(1)
        return v
    # tworze bitmape na podstawie vectora [-1;1]
    def get_bitmap_from_vector(self, vector) -> list:
        b = []
        temp = []
        i = 0
        for item in vector:
            if i == self.Size[0]:
                i = 0
                b.append(temp)
                temp = []
            if item == 1: temp.append(1)
            else: temp.append(0)
            i = i + 1
        b.append(temp)
        return b
    # dodaje bitmape do sieci
    def add_single_raw_bitmap(self, bitmap) -> None:
        self.Bitmaps_raw.append(bitmap)
    
    # dodaje bitmapy do sieci
    def add_multi_raw_bitmaps(self, bitmaps) -> None:
        for bitmap in bitmaps:
            self.Bitmaps_raw.append(bitmap)

    # proces uczenia sie bitmap wzorcowych
    def learn(self, wsp_uczenia=None) -> list:
        size = self.Size[0]*self.Size[1]
        if wsp_uczenia is None: wsp_uczenia=1/size
        for bitmap in self.Bitmaps_raw:
            vector = self.get_vector_from_bitmap(bitmap)
            learning = []
            for i in range(size):
                temp = []
                for j in range(size):
                    if i == j: temp.append(0)
                    else:
                        y_i, y_j = vector[i], vector[j]
                        last = self.Weights[i][j]
                        ans = last + wsp_uczenia * y_i * y_j
                        temp.append(ans)
                learning.append(temp)
            self.Bitmaps_learned.append(learning)
        for bitmap in self.Bitmaps_learned:
            for i in range(size):
                for j in range(size):
                    self.Weights[i][j] = self.Weights[i][j] + bitmap[i][j]
        return self.Weights


    # uruchomienie pracy sieci - naprawa testowej bitmapy
    def run(self, bitmap_test):
        def sgn(a):
            return (a > 0) - (a < 0)
        # proces naprawiania
        vector = None
        last = None
        while last is None or last != vector:
            if vector is None: vector = self.get_vector_from_bitmap(bitmap_test)
            else: vector = last
            vector_repair = []
            size = len(vector)
            for i in range(size):
                suma = 0        
                for j in range(size):
                    if i == j: continue
                    w = self.Weights[i][j]
                    y_i = vector[j]
                    suma = suma + (w * y_i)
                vector_repair.append(sgn(suma))
            last = vector_repair
        # odtwarzam i zwracam naprawiony obraz
        return self.get_bitmap_from_vector(vector)     

if __name__ == "__main__":    
    testowa = load_bitmap_test('bitmaps/test.txt')
    wzorce = load_bitmap_wz('bitmaps')

    m,n = len(testowa[0]), len(testowa)
    
    hobfield = HopfieldNetwork(m,n, False)   # false - wagi startowe to 0, true - wagi startowe sa losowane
    hobfield.add_multi_raw_bitmaps(wzorce)
    hobfield.learn()
    ans = hobfield.run(testowa)   # tutaj dostaje naprawiona bitmape
    wyswietl(testowa, ans)
    print(ans)