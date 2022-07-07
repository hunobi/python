import matplotlib.pyplot as plt

class HubDraw:
    class Colors:
        Black = 'black'
        Blue = 'blue'
        Cyan = 'cyan'
        Green = 'green'
        Red = 'red'
        White = 'white'
        Yellow = 'yellow'
        All = [Blue, Cyan, Green, Red, Yellow]

    class Marker:
        Null = 'None'
        Point = '.'
        Circle = 'o'
        Star = '*'
        Diamond = 'D'
        Square = 's'

    class LineStyle:
        Null = 'None'
        Solid = '-'
        Dashed = '--'
        Dotted = ':'
        Dash_Dot = '-.'

    def wykres_czysc(self, ax=None):
        if ax is None: plt.cla()
        else: ax.cla()
    
    def wykres_linie_rysuj(self, X, Y, ax=None, label="", color=Colors.Blue, marker=Marker.Null,linestyle=LineStyle.Solid):
        if ax is None: plt.plot(X,Y, label=label, color=color,marker=marker, linestyle=linestyle)
        else: ax.plot(X,Y, label=label, color=color,marker=marker, linestyle=linestyle)
    
    def wykres_punkty_rysuj(self, X, Y, ax=None, label="", markersize=6,color=Colors.Red, marker=Marker.Point, linestyle=LineStyle.Null):
        if ax is None: plt.plot(X,Y,label=label,color=color,marker=marker,linestyle=linestyle, markersize=markersize)       
        else: ax.plot(X,Y,label=label,color=color,marker=marker,linestyle=linestyle, markersize=markersize)
        
    def legenda(self, ax=None):
        if ax is None: plt.legend()
        else: ax.legend()
    
    def pokaz_siatke(self, flag, ax=None):
        if ax is None: plt.grid(flag)
        else: ax.grid(flag)

    def xName(self, name, ax=None):
        if ax is None: plt.xlabel(name)
        else: ax.set_xlabel(name)
    
    def yName(self, name, ax=None):
        if ax is None:  plt.ylabel(name)
        else: ax.set_ylabel(name)

    def wykres_wyswietl(self):
        plt.show()

    def set_animation(self, s):
        plt.pause(s)

    def create_subplots(self, a, b):
        return plt.subplots(a,b)
