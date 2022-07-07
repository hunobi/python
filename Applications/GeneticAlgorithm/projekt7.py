'''
numer_projektu: 7
'''
import matplotlib.pyplot as plt
import numpy as np

from Utils import Unit
from Utils import Other
from Utils import Genetics
# funkcja celu
def f(x): return 1 - (1/(x+1)) - (x/2)
#def f(x): return np.sin(x/10)*np.sin(x/200)

# glowna funkcja algorytmu genetycznego z mozliwoscia wyboru czy chcemy minimalizowac czy maksymalizowac
def genetic_algorithm(iterations, genotype_size, search_field, minimization = False):
    # prawdopodobienstwo zajscia mutacji na genie
    probability = 1/genotype_size
    # utworzenie glownego osobnika
    main_unit = Unit()
    main_unit.Genotype_X = Other.generate_new_unit(genotype_size)
    for generation in range(iterations):
        # utworzenie nowego osobnika z genotypem tego glownego
        new_unit = Unit()
        new_unit.Genotype_X = main_unit.Genotype_X
        new_unit.Genotype_X = Genetics.mutation(new_unit.Genotype_X, probability)
        # obliczenie fentypu oraz wartosc funkcji przystosowania dla glownego osobnika
        main_unit.Phenotype_X = Other.compute_phenotype(main_unit.Genotype_X, search_field, genotype_size)
        main_unit.Adaptation = f(main_unit.Phenotype_X)
        # obliczenie fentypu oraz wartosc funkcji przystosowania dla nowego osobnika
        new_unit.Phenotype_X = Other.compute_phenotype(new_unit.Genotype_X, search_field, genotype_size)
        new_unit.Adaptation = f(new_unit.Phenotype_X)
        # w zaleznosci czy minimalizujemy czy maksymalizujemy, podmieniamy glownego osobnika jezeli nowy osobnik jest lepszy
        if minimization:
            if new_unit.Adaptation < main_unit.Adaptation: main_unit = new_unit
        else:
            if new_unit.Adaptation > main_unit.Adaptation: main_unit = new_unit
    # zwracamy najlepszy wynik po N iteracjach algorytmu
    return main_unit.Genotype_X, main_unit.Phenotype_X, main_unit.Adaptation

if __name__ == "__main__":
# konfiguracja
    #x_range = [0,100]
    x_range = [0,1]
    genotype_size = 32
    simulation_repetitions = 10000
    minimization = False
# wywolanie
    results = []
    only_x = []
    only_y = []
    the_best = None
    for rep in range(simulation_repetitions):
        gen, ans_x, ans_adaptation = genetic_algorithm(100, genotype_size, x_range, minimization)
        # sprawdzanie najlepszego wyniku
        if the_best is None: the_best = (ans_x,ans_adaptation)
        else:
            if minimization:
                if ans_adaptation < the_best[1]: the_best = (ans_x,ans_adaptation)
            else:
                 if ans_adaptation > the_best[1]: the_best = (ans_x,ans_adaptation)
        # zapisanie wartosci do listy
        results.append((ans_x,ans_adaptation))
        only_x.append(ans_x)
        only_y.append(ans_adaptation)
    
# rysowanie
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    x = np.linspace(x_range[0], x_range[1])
    y = f(x)
    ax1.set_title("Wykres funkcji celu")
    ax1.grid(True)
    ax1.plot(x,y)
    ax2.set_title("Rozłożenie punktów na wykresie")
    ax2.grid(True)
    ax2.plot(x,y)
    for i in results: ax2.plot(i[0],i[1], '.b', label="Wyniki" if i == results[0] else "")
    
    # wyzanczenie najlepszego wyniku i wyroznienie go na wykresie
    the_best_x = Other.dominant(only_x)
    the_best_y = f(the_best_x)
    ax2.plot(the_best_x, the_best_y, 'Dm', label="Najczęściej")
    ax2.plot(the_best[0], the_best[1], 'xr', label="Najlepszy")
    ax2.legend()
    # histogram punktów x
    ax3.hist(only_x, range= [min(only_x),max(only_x)])
    ax3.set_title("Histogram fenotypów")
    ax3.grid(True)
    # histogram wartosci funkcji celu (y)
    ax4.hist(only_y, range= [min(only_y),max(only_y)])
    ax4.set_title("Histogram wartości przystosowania")
    ax4.grid(True)

    fig.suptitle("Najlepszy wynik: f({0}) = {1}".format(the_best[0],the_best[1]))
    
    print(gen,the_best[0],the_best[1])
    
    # pokazanie wynikow
    plt.show()
    