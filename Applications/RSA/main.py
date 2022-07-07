import random, decimal

# FUNKCJE POMOCNICZE

# algorytm do znajdowania największego wspólnego dzielnika
def nwd(a, b): 
        a = abs(a)
        b = abs(b)
        while b > 0:  
            a, b = b, a % b
        return a

# rozszerzony algorytm euklidesa
def nwd_rozszerzony(a, b): 
    if a == 0 :  return b,0,1       
    gcd,x1,y1 = nwd_rozszerzony(b%a, a) 
    x = y1 - (b//a) * x1 
    y = x1 
    return gcd,x,y

# sprawdza czy liczba n jest liczba pierwsza
def czy_pierwsza(n):
        ans, i = [], 2
        pom = decimal.Decimal(n).sqrt() 
        pom = int(str(pom).split('.')[0])
        while n != 1:
            if i == pom: break
            if n%i == 0:
                n = int(n/i)
                ans.append(i)
            else: i+=1
        flag = len(ans) > 0
        return not flag

# losuje liczbe pierwsza z podanego przedzialu        
def wylosuj_liczbe_pierwsza(a,b):
        n = random.randint(a,b)
        if n%2==0: n+=1
        while not czy_pierwsza(n): n += 2
        return n 

# GŁÓWNE FUNKCJE ALGORYTMU
def generuj_pare_kluczy(rozmiar):
    mini, maksi = 2**rozmiar, 2**(rozmiar+1) # tworze zakres dla liczby pierszej [2^rozmiar,2^(rozmiar+1)]
    p = wylosuj_liczbe_pierwsza(mini, maksi) # losowanie liczby p
    print("p:",p, flush=True)
    q = wylosuj_liczbe_pierwsza(mini, maksi) # losowanie liczby q
    print("q:",q,flush=True)
    n = p*q # iloczyn liczb pierwszych p i q
    print("n:",n,flush=True)
    phi = (p-1)*(q-1) # obliczenie wartosci phi
    print("phi:",phi,flush=True)
    e = random.randint(3,n) # wybieranie liczby e względnie pierwszej do phi
    while not nwd(e, phi) == 1: e=random.randint(3,n)
    d = nwd_rozszerzony(e, phi)[1] # wyznaczenie liczby d
    while True:  # tutaj sprawdzam poprawnosc liczb e i d i wybieram ponownie jesli cos jest nie tak 
        if d > 1 and (e*d)%phi == 1: break
        e=random.randint(3,n)
        while not nwd(e, phi) == 1: e=random.randint(3,n)
        d = nwd_rozszerzony(e, phi)[1]
    print("e:",e,flush=True)
    print("d:",d,flush=True)
    return (e,n),(d,n) # zwraca klucze


def szyfrowanie(klucz_publiczny, wiadomosc):
    szyfr = []
    e,n = klucz_publiczny
    wiadomosc = wiadomosc.encode("utf8")
    for bajt in wiadomosc:
        szyfr.append(pow(bajt,e,n))
    return szyfr

def deszyfrowanie(klucz_prywatny, szyfr):
    wiadomosc = bytearray(b"")
    d,n = klucz_prywatny
    for kod in szyfr:
        wiadomosc.append(pow(kod,d,n))
    return wiadomosc.decode()


if __name__ == "__main__":
    print("\n=============\n")
    klucz_publiczny, klucz_prywatny = generuj_pare_kluczy(32) 
    print("\n=============\n")
    print("Klucz publiczny:", klucz_publiczny)
    print("Klucz prywatny:", klucz_prywatny)
    tekst = "Jakieś hasło!"
    szyfr = szyfrowanie(klucz_publiczny, tekst)
    znowu_tekst = deszyfrowanie(klucz_prywatny, szyfr)
    print("Tekst:", tekst)
    print("Zakodowany tekst:",[i for i in tekst.encode("utf8")])
    print("Szyfr:", szyfr)
    print("Odszyfrowany tekst:", znowu_tekst)
    print("\n=============\n")
