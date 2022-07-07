'''
numer_projektu: 9
'''

import matplotlib.pyplot as plt
import numpy as np

from Utils import Unit
from Utils import Other
from Utils import Genetics

# funkcja celu - funkcja ktora bedzie poddana optymalizowaniu
def f(x,y): return x**2 + x*y + 2*x + y**2

def generate_population(p_size, gen_size, search_field) -> list:
    population = []
    for i in range(p_size):
        u = Unit()
        u.Genotype_X = Other.generate_new_unit(gen_size)
        u.Genotype_Y = Other.generate_new_unit(gen_size)
        u.Phenotype_X = Other.compute_phenotype(u.Genotype_X, search_field, gen_size)
        u.Phenotype_Y = Other.compute_phenotype(u.Genotype_Y, search_field, gen_size)
        u.Adaptation = f(u.Phenotype_X, u.Phenotype_Y)
        population.append(u)
    return population

def genetic_algorithm(iterations, genotype_size, population_size ,search_field, minimalization = True) -> Unit:
    probability = 1/genotype_size # prawdopodobienstwo wystapienia mutacji
    parent_limit = population_size//2 # limit rodzicow, sztywno ustawiony na polowe populacji
    main_population = generate_population(population_size, genotype_size, search_field) # generowanie populacji poczatkowej
    for generation in range(iterations):
        new_population = [] 
        # eliminacja najslabszych osobnikow i pozostawienie tylko tylu ile wynosi wartosc parent_limit
        for i in range(parent_limit): 
            temp_units = [i for i in main_population]
            values = [i.Adaptation for i in main_population]
            index = None
            if minimalization: index = values.index(min(values))
            else: index = values.index(max(values))
            new_population.append(temp_units[index])
            main_population.pop(index)
        
        # proces krzyzowania parami, 1z2, 3z4... tworząc pary (AB, BA), (CD,DC)
        crossed = [] # tutaj przechowuje krzyzowane nowe osobniki
        i = 0
        while i < len(new_population):
            if i+1 >= len(new_population): # jezeli zostanie bez pary to krzyzowanie nastepuje ostatni-pierwszy
                last = new_population[-1]
                first = new_population[0]
                x0, _ = Genetics.genetic_crossing(last.Genotype_X, first.Genotype_X, genotype_size)
                y0, _ = Genetics.genetic_crossing(last.Genotype_Y, first.Genotype_Y, genotype_size)
                temp_0 = Unit()
                temp_0.Genotype_X = x0
                temp_0.Genotype_Y = y0
                crossed.append(temp_0)
                break
            A = new_population[i]
            B = new_population[i+1]
            (x0, x1) = Genetics.genetic_crossing(A.Genotype_X, B.Genotype_X, genotype_size)
            (y0, y1) = Genetics.genetic_crossing(A.Genotype_Y, B.Genotype_Y, genotype_size)
            
            temp_1 = Unit()
            temp_1.Genotype_X = x0
            temp_1.Genotype_Y = y0

            temp_2 = Unit()
            temp_2.Genotype_X = x1
            temp_2.Genotype_Y = y1

            crossed.append(temp_1)
            crossed.append(temp_2)
            i+=2
        
        # koniec krzyzowania
        main_population = new_population + crossed # poloczenie populacji najlepszych rodzicow z nowymi krzyzowkami
        
        # proces mutacji i wyliczania fenotypow oraz wyliczenia oceny przynaleznosci 
        for unit in main_population:
            unit.Genotype_X = Genetics.mutation(unit.Genotype_X, probability) # mutajca genotypu X
            unit.Genotype_Y = Genetics.mutation(unit.Genotype_Y, probability) # mutacja genotypu Y
            unit.Phenotype_X = Other.compute_phenotype(unit.Genotype_X, search_field, genotype_size) # wyliczenie fenotypu X
            unit.Phenotype_Y = Other.compute_phenotype(unit.Genotype_Y, search_field, genotype_size) # wyliczenie fenotypu Y
            unit.Adaptation = f(unit.Phenotype_X, unit.Phenotype_Y) # dokonanie oceny jednostki
    # wybranie najlepszego osobnika z ostatecznej populacji po N iteracjach
    the_best = Unit()
    if minimalization: the_best.Adaptation = np.inf
    else: the_best.Adaptation = -np.inf

    for u in main_population:
        if minimalization:
            if u.Adaptation < the_best.Adaptation: the_best = u
        else:
            if u.Adaptation > the_best.Adaptation: the_best = u
    return the_best


if __name__ == "__main__":
    # konfiguracja
    xy_range = [-4,2]
    genotype_size = 32
    population_size = 10
    simulation_repetitions = 10000 
    # wywolanie
    ans_x = []
    ans_y = []
    ans_ad = []
    results = []
    the_best = None
    minimalize = True
    for gen in range(simulation_repetitions):
        result = genetic_algorithm(50, genotype_size, population_size, xy_range, minimalization = minimalize)
        results.append(result)
        ans_x.append(result.Phenotype_X)
        ans_y.append(result.Phenotype_Y)
        ans_ad.append(result.Adaptation)
        if the_best is None: the_best = result
        else: 
            if minimalize: 
                if result.Adaptation < the_best.Adaptation: the_best = result 
            else:
                if result.Adaptation > the_best.Adaptation: the_best = result 
    # rysowanie
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    x = np.linspace(xy_range[0], xy_range[1])
    y = np.linspace(xy_range[0], xy_range[1])
    x,y = np.meshgrid(x,y)
    z = f(x,y)
    ax1.contour(x,y,z)
    ax1.set_title("Rozkład punktów na wykresie")
    for res in results: ax1.plot(res.Phenotype_X, res.Phenotype_Y, 'og', label="Wyniki" if res == results[0] else "")
    dom_x = Other.dominant(ans_x)
    dom_y = Other.dominant(ans_y)
    dom_ad = Other.dominant(ans_ad)
    ax1.plot(dom_x, dom_y, '*b', label = "Najczęstsze")
    ax1.plot(the_best.Phenotype_X, the_best.Phenotype_Y, 'xr', label = "Najlepsze")
    ax1.legend()
    

    ax2.set_title("Histogram dla przystosowania (f(x,y)={0})".format(round(dom_ad,5)))
    ax2.hist(ans_ad, range=[min(ans_ad),max(ans_ad)])

    ax3.set_title("Histogram dla wartości X (x={0})".format(round(dom_x,5)))
    ax3.hist(ans_x, range=[min(ans_x),max(ans_x)])
    
    ax4.set_title("Histogram dla wartości Y (y={0})".format(round(dom_y,5)))
    ax4.hist(ans_y, range=[min(ans_y),max(ans_y)])
    
    print("Genotyp X:\t{0}\nGenotyp Y:\t{1}\nFenotyp X:\t{2}\nFenotyp Y:\t{3}\nPrzystosowanie:\t{4}"
        .format(the_best.Genotype_X,the_best.Genotype_Y, the_best.Phenotype_X, the_best.Phenotype_Y, the_best.Adaptation))
    
    plt.show()