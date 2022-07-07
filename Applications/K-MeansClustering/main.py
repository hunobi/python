# Hubert Koloska ; K-Srednich

from HubDraw import HubDraw
import random
import math
from numpy.core.fromnumeric import mean

class Point:
    def __init__(self,x,y,color=HubDraw.Colors.Black):
        self.X = x
        self.Y = y
        self.Symbol = HubDraw.Marker.Circle
        self.Color = color
    
    def getSymbol(self):
        return self.Symbol

    def getColor(self):
        return self.Color

    def setColor(self, newColor):
        self.Color = newColor


class Group:
    def __init__(self, point, color, symbol = HubDraw.Marker.Star):
        self.Values = []
        self.Color = color
        self.Center = point
        self.Center_symbol = symbol
    
    def updateValues(self, allPoints):
        self.Values = []
        for point in allPoints:
            if(point.Color == self.Color):
                self.Values.append(point)
    
    def getColor(self):
        return self.Color

class Spiral:
    def __init__(self):
        self.values = []
        self.atr_className = []
        self.atr_type = []
        self.groups = []
        self.hub_plot = HubDraw()

    def euclidean_distance(self, A, B) -> float:
        return math.sqrt(math.pow(A.X -B.X,2)+math.pow(A.Y-B.Y,2))

    def K_Srednich(self, k=4, iters = 100):
        if k < 1: raise ValueError('Wrong "k" value')
        if k>len(HubDraw.Colors.All): raise ValueError('Max "k" is:\t',str(len(HubDraw.Colors.All)))
        self.groups = []
        index_point = []
        for i in range(k):
            index = random.randint(0, len(self.values)-1)
            while(index in index_point):
                index = random.randint(0,len(self.values)-1)
            index_point.append(index)
            tmp = self.values[index]
            tmp.setColor(HubDraw.Colors.All[i])
            self.groups.append(Group(tmp, color=HubDraw.Colors.All[i]))
        
        for i in range(iters):
            print("Iteracja:",i+1)
            for point in self.values:
                distance = []
                for group in self.groups:
                    distance.append(self.euclidean_distance(point, group.Center))
                mini = min(distance)
                mini_index = distance.index(mini)
                near_group = self.groups[mini_index]
                point.setColor(near_group.Color)
            
            for group in self.groups:
                group.updateValues(self.values)
                if len(group.Values) > 0:
                    ox = []
                    oy = []
                    for item in group.Values:
                        ox.append(item.X)
                        oy.append(item.Y)
                    ox_m = mean(ox)
                    oy_m = mean(oy)
                    group.Center = Point(ox_m, oy_m, group.Color)
            self.hub_plot.wykres_czysc()
            for item in self.values:
                self.hub_plot.wykres_punkty_rysuj(item.X, item.Y, color=item.getColor(), marker=item.getSymbol(), markersize = 6)
            for group in self.groups:
                self.hub_plot.wykres_punkty_rysuj(group.Center.X, group.Center.Y, marker=group.Center_symbol, color=group.getColor(), markersize=12, label=group.getColor())
            self.hub_plot.set_animation(0.01)

    def Show(self):
        #self.hub_plot.wykres_czysc()
        #for item in self.values:
        #    self.hub_plot.wykres_punkty_rysuj(item.X, item.Y, color=item.getColor(), marker=item.getSymbol(), markersize = 6)
        #for group in self.groups:
        #    self.hub_plot.wykres_punkty_rysuj(group.Center.X, group.Center.Y, marker=group.Center_symbol, color=group.getColor(), markersize=12)
        self.hub_plot.legenda()
        self.hub_plot.wykres_wyswietl()

    def load(self, varFile, classFile):
        def wykryj_separator(line):
            s = ['\t', ' ', ';', '|', '::']
            for sep in s:
                if len(line.split(sep)) > 1:
                    return sep
            raise ValueError('Brak seperatora')
        
        # 1 - wczytuje wartosci
        with open(varFile, 'r') as file:
            items = file.readlines()
            for item in items:
                tmp = item.strip().split(wykryj_separator(item))
                new_tmp = []
                for item in tmp:
                    if item == '': continue
                    else: new_tmp.append(item)
                if len(new_tmp) < 2 : continue
                self.values.append( Point(float(new_tmp[0]), float(new_tmp[1])) )
            file.close()

        # 2 - wczytuje nazwy atrybutow i sprawdzam czy atrybut jest symbolem
        with open(classFile, 'r') as file:
            items = file.readlines()
            for item in items:
                tmp = item.strip().split(wykryj_separator(item))
                new_tmp = []
                for item in tmp:
                    if item == '': continue
                    else: new_tmp.append(item)
                if len(new_tmp) < 2 : continue
                self.atr_className.append(new_tmp[0])
                self.atr_type.append(new_tmp[1])
            file.close()


if __name__ == "__main__":
    spirala = Spiral()
    spirala.load('spirala.txt', 'spirala-type.txt')
    spirala.Show()
    spirala.K_Srednich(k=4, iters=20)
    spirala.Show()
