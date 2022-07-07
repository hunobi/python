import math
import numpy as np
import random as r
from fractions import Fraction

#--------------------------------------------------

matrix = [
            [ 4, -2, 4, -2,  8],
            [ 3, 2, 4, 2,   7 ],
            [ 2, 4, 2, 1,   10],
            [ 2, -2, 4, 2,  2 ]
         ]


# --------------------------------------------------
def getColumn(data, number):
    temp = []
    for item in data:
        temp.append(item[number])
    return temp


def getRow(data, number):
    return data[number]


def UkladRownan(matrix):
  
    def Wyznacznik(matrix):
        return np.linalg.det(matrix)

    def BudujMacierz(matrix, WW, n):
        M = []
        for row in range(len(matrix)):
            temp = []
            for col in range(len(matrix)):
                if col == n:
                    temp.append(WW[row])
                else:
                    temp.append(matrix[row][col])
            M.append(temp)
        return M

    WyrazyWolne = getColumn(matrix, len(matrix[0])-1)
    M = []
    for row in matrix:
        temp = []
        i = len(row) - 1
        for col in range(i):
            temp.append(row[col])
        M.append(temp)

    Wyznaczniki = []
    Result = []
    Wyznacznik_Glowny = Wyznacznik(M)
    
    if Wyznacznik_Glowny != 0:
        for i in range(0, len(M)):
            Wyznaczniki.append(Wyznacznik(BudujMacierz(M, WyrazyWolne, i)))
        for i in Wyznaczniki:
            Result.append(i / Wyznacznik_Glowny)
        return Result
    else:
        return "Brak rozwiązania"


np.seterr(all='warn')

for i in matrix:
    print(i)

print("\nResults\n")
num = 1
for i in UkladRownan(matrix):
    print("x%s:\t %0.5f\t=>\t%s" % (str(num), i, Fraction(i).limit_denominator()))
    num = num + 1

