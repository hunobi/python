''' 
opis: Plik zawiera pomocnicze klasy zawierające funkcje wielokrotnie wykorzystywane w programach
'''
import numpy as np
from statistics import mode

'''
Klasa Unit jest reprezentacja osobnika zawierajacego genotypy fenotypy oraz przystosowanie
'''  
class Unit:
    def __init__(self) -> None:
        self.Genotype_X = None
        self.Phenotype_X = None
        self.Genotype_Y = None
        self.Phenotype_Y = None
        self.Adaptation = None


'''
Klasa Converters zawiera funkcje do konwertowania wartości w systemach binarnym, dziesiętnym oraz kodzie graya
'''  
class Converters:
    # kod dziesietny do kodu binarnego
    def dec_to_bin(n) -> str: return f"{bin(n)[2:]}"

    # system dziesietny na kod graya
    def dec_to_gray(dec) -> str:
        dec ^= (dec >> 1)
        return Converters.dec_to_bin(dec)

    # kod binarny na system dziesietny
    def bin_to_dec(b) -> int: return int(b,2)

    # binarny na kod graya
    def bin_to_gray(b) -> str:
        dec = Converters.bin_to_dec(b)
        dec ^= (dec >> 1)
        return Converters.dec_to_bin(dec)

    # kod graya na kod binarny
    def gray_to_bin(g) -> str:
        dec = Converters.bin_to_dec(g)
        mask = dec
        while mask !=0:
            mask >>= 1
            dec ^=mask
        return Converters.dec_to_bin(dec)
    # kod graya na system dziesietny
    def gray_to_dec(g) -> int:
        b = Converters.gray_to_bin(g)
        return Converters.bin_to_dec(b)



'''
Klasa Genetics zawiera funkcje do odwzorowania operacji genetycznych, takich jak mutacja, krzyzowanie
'''      
class Genetics:
    # mutuje gen z pewnym prawdopodobienstwem, zwraca zmutowany gen
    def mutation(genotype, probability) -> str:
        temp = ""
        for bit in genotype:
            flaga = np.random.random() < probability
            if flaga:
                if bit == "0": temp = temp + "1"
                else: temp = temp + "0"
            else: temp = temp + bit
        return temp

    # krzyzowanie genotypu miedzy osobnikiem A i B, zwraca dwa nowe warianty genotypow (AB,BA)
    def genetic_crossing(unit_a, unit_b, genotype_size) -> tuple:
        size = np.random.randint(2,genotype_size//1.5)
        unit_a_left, unit_a_right = unit_a[:size], unit_a[size:]
        unit_b_left, unit_b_right = unit_b[:size], unit_b[size:]
        return (unit_b_left+unit_a_right), (unit_a_left+unit_b_right)



'''
Klasa Other zawiera pozostale funkcje wykorzystywane w programie, np obliczanie fenotypu, generowanie genotypu nowemu osobnikowi itd
'''  
class Other:
    # funkcja do wyrownywania bitow do rozmiaru genotypu
    def align_the_length_of_the_bits(bits, genotype_size) -> str:
        while len(bits) != genotype_size:
            bits = "0"+bits
        return bits
    # generowanie genotypu dla nowego osobnika 
    def generate_new_unit(genotype_size) -> str:
        temp = ""
        for i in range(genotype_size): temp = temp + str(np.random.randint(0,2))
        return temp

    # obliczanie fenotypu dla konkretnego genotypu w podanym zakresie przeszukiwan
    def compute_phenotype(genotype, field, genotype_size):
        return field[0] + ((field[1]-field[0])*Converters.gray_to_dec(genotype))/(2**genotype_size-1)
    
    # zwraca najczesciej pojawiajaca sie wartosc w zbiorze (dominanta)
    def dominant(arr): return mode(arr)