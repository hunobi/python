import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def mean(A):
    return round(A.mean(), 2)


def var(A):
    return round(A.var(ddof=1), 2)


def std(A):
    return round(A.std(ddof=1), 2)


def get_item_not_range(A,p):
    tmp = []
    for item in A:
        if item < p[0] or item > p[1]:
            tmp.append(item)
    return tmp


def wartosci_typowe_1(A):
    return (round(mean(A)-std(A),2), round(mean(A)+std(A),2))


def procent_wartosci_typowe_1(A):
    p = wartosci_typowe_1(A)
    amount = float(len(A))
    tmp = get_item_not_range(A, p)
    return str(round(((amount-len(tmp))/amount)*100.0, 2))+"%"


def wartosci_typowe_2(A):
    return (round(mean(A)-2*std(A),2), round(mean(A)+2*std(A),2))


def procent_wartosci_typowe_2(A):
    p = wartosci_typowe_2(A)
    amount = float(len(A))
    tmp = get_item_not_range(A, p)
    return str(round(((amount-len(tmp))/amount)*100.0, 2))+"%"


def kwantyl(A,n):
    st = None
    if n == 1:
        st = 0.25
    elif n == 2:
        st = 0.5
    elif n == 3:
        st = 0.75
    else:
        return None
    return round(np.quantile(A, st), 2)


def odchylenie_cwiartkowe(A):
    return round((kwantyl(A, 3)-kwantyl(A, 1))/2.0, 2)


def przedzial_kwartylowy_1(A):
    return (round(kwantyl(A,2)-odchylenie_cwiartkowe(A),2), round(kwantyl(A,2)+odchylenie_cwiartkowe(A),2))


def przedzial_kwartylowy_2(A):
    return (round(kwantyl(A,1)-3*odchylenie_cwiartkowe(A),2), round(kwantyl(A,3)+(3*odchylenie_cwiartkowe(A)), 2))


dane_1 = np.array([43.8,27.5,46.6,34.3,28.4,24.4,30.6,29.3,43.2,33.7,27.2,39.2,28.0,53.9,37.0,25.3,54.8,35.0,37.7,33.1,31.6,38.5,36.8,29.3,33.4,46.9,30.5,27.1,32.5,31.4,40.6,30.1,33.6,42.4,36.7,44.1,38.2,35.2,37.8,50.3,43.1,35.0,32.5,40.8,52.4,36.8,29.4,47.2,52.7,35.8,31.2,51.0,36.0,36.0,46.1,51.8,49.7,39.8,26.4,41.1,38.0,45.6,44.1,34.8,33.3,39.7,40.9,36.3,31.8,40.9])
dane_2 = np.array([43,40,41,69,39,41,48,48,55,42,59,35,51,49,50,51,45,40,51,66,38,44,65,44,42,36,41,50,37,51,34,44,44,41,49,41,39,37,48,45,43,45,43,40,39,47,48,60,41,41,49,36,44,42,57,39,43,39,37,77,46,49,51,46,42,45,43,58,42,42])


data = {
    "Dane_1": [],
    "Dane_2": [],
}

#liczenie średniej
data['Dane_1'].append(mean(dane_1))
data['Dane_2'].append(mean(dane_2))

#liczenie wariancji
data['Dane_1'].append(var(dane_1))
data['Dane_2'].append(var(dane_2))


#liczenie odchylenia
data['Dane_1'].append(std(dane_1))
data['Dane_2'].append(std(dane_2))


#liczenie przedzialu wartosci typowej 1
data['Dane_1'].append(wartosci_typowe_1(dane_1))
data['Dane_2'].append(wartosci_typowe_1(dane_2))


#liczenie procentu wartosci typowych 1
data['Dane_1'].append(procent_wartosci_typowe_1(dane_1))
data['Dane_2'].append(procent_wartosci_typowe_1(dane_2))


#liczenie przedzialu wartosci typowej 2
data['Dane_1'].append(wartosci_typowe_2(dane_1))
data['Dane_2'].append(wartosci_typowe_2(dane_2))


#liczenie procentu wartosci typowych 2
data['Dane_1'].append(procent_wartosci_typowe_2(dane_1))
data['Dane_2'].append(procent_wartosci_typowe_2(dane_2))


#wyznaczanie wartosci odstajacych
data['Dane_1'].append(get_item_not_range(dane_1, wartosci_typowe_2(dane_1)))
data['Dane_2'].append(get_item_not_range(dane_2, wartosci_typowe_2(dane_2)))


#wyznaczenie wspolczynnika zmiennosci
data['Dane_1'].append(round(std(dane_1)/mean(dane_1),2))
data['Dane_2'].append(round(std(dane_2)/mean(dane_2),2))


#wyznaczenie min
data['Dane_1'].append(np.min(dane_1))
data['Dane_2'].append(np.min(dane_2))


#wyznaczenie max
data['Dane_1'].append(np.max(dane_1))
data['Dane_2'].append(np.max(dane_2))


#wyznaczenie rozstepu
data['Dane_1'].append(np.max(dane_1)-np.min(dane_1))
data['Dane_2'].append(np.max(dane_1)-np.min(dane_2))


#wyznaczenie Q1
data['Dane_1'].append(kwantyl(dane_1, 1))
data['Dane_2'].append(kwantyl(dane_2, 1))


#wyznaczenie Q2
data['Dane_1'].append(kwantyl(dane_1, 2))
data['Dane_2'].append(kwantyl(dane_2, 2))


#wyznaczenie Q3
data['Dane_1'].append(kwantyl(dane_1, 3))
data['Dane_2'].append(kwantyl(dane_2, 3))


#wyznaczenie Q
data['Dane_1'].append(odchylenie_cwiartkowe(dane_1))
data['Dane_2'].append(odchylenie_cwiartkowe(dane_2))


#wyznaczenie Q1-3Q
data['Dane_1'].append(round(kwantyl(dane_1, 1) - 3 * odchylenie_cwiartkowe(dane_1), 2))
data['Dane_2'].append(round(kwantyl(dane_2, 1) - 3 * odchylenie_cwiartkowe(dane_2), 2))



#wyznaczenie Q3+3Q
data['Dane_1'].append(round(kwantyl(dane_1, 3) + 3 * odchylenie_cwiartkowe(dane_1), 2))
data['Dane_2'].append(round(kwantyl(dane_2, 3) + 3 * odchylenie_cwiartkowe(dane_2), 2))



#przedzial kwartylowy 1
data['Dane_1'].append(przedzial_kwartylowy_1(dane_1))
data['Dane_2'].append(przedzial_kwartylowy_1(dane_2))


#przedzial kwartylowy 2
data['Dane_1'].append(przedzial_kwartylowy_2(dane_1))
data['Dane_2'].append(przedzial_kwartylowy_2(dane_2))


#wartosci odstajace
data['Dane_1'].append(get_item_not_range(dane_1, przedzial_kwartylowy_2(dane_1)))
data['Dane_2'].append(get_item_not_range(dane_2, przedzial_kwartylowy_2(dane_2)))


#nadanie indeksów w tabeli
df = pd.DataFrame(data, index=['średnia',
                               'wariancja',
                               'odchylenie_std',
                               'przedzial_wartosci_1',
                               'procent_wartosci_1',
                               'przedzial_wartosci_2',
                               'procent_wartosci_2',
                               'wartosci_odstajace',
                               'wsp zmiennosci',
                               'min',
                               'max',
                               'rozstep',
                               'Q1',
                               'Q2',
                               'Q3',
                               'odchylenie_cwiartkowe_Q',
                               'Q1-3Q',
                               'Q3+3Q',
                               'przedzial_kwartylowy_1',
                               'przedzial_kwartylowy_2',
                               'wartosci_odstajace'
                               ])

#ustawia zeby wypisac wszystkie kolumny
pd.set_option('display.max_columns', None)
#wypisuje
print(df)

#siatka
x = [i for i in range(0, 70)]
srednia = [data['Dane_1'][0] for i in x]
plt.plot(x, dane_1, label="Masa")
plt.plot(x, dane_2, label="Wytrzymalosc")
plt.plot(x, srednia, label="średnia masy")
plt.legend(loc="upper left")
plt.xlabel("Próbka")
plt.ylabel("Wartość")
plt.show()




# pomoc w zaleznosci


zaleznosc = {}


n=0
for i in dane_1:
    zaleznosc[i] = dane_2[n]
    n=n+1

w = []
m = []

for i in zaleznosc:
    if i >= data['Dane_1'][0]:
        w.append(zaleznosc[i])
    else:
        m.append(zaleznosc[i])


print("Wiekszych jest {0} a suma: {1}".format(len(w), sum(w)))
print("Mniejszych jest {0} a suma: {1}".format(len(m), sum(m)))
