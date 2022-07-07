# Hubert Koloska - Sterownik Rozmyty Takagi-Sugeno

from matplotlib import pyplot as plt, patches
import matplotlib as mpl
import numpy as np

class Rotation:
    Right_Max = 20
    Right_Weak = 10
    Straight = 0
    Left_Weak = -10
    Left_Min = -20
    Range = [-20,20]
    Values = [-20,-10,0,10,20]
    def check(x):
        if x <= Rotation.Left_Min: return Rotation.Left_Min
        elif x > Rotation.Left_Min and x <= Rotation.Left_Weak: return Rotation.Left_Weak
        elif x > Rotation.Left_Weak and x <= Rotation.Straight: return Rotation.Straight
        elif x > Rotation.Straight and x <= Rotation.Right_Weak: return Rotation.Right_Weak
        elif x > Rotation.Right_Weak: return Rotation.Right_Max

class OX:
    Right_Far = 70
    Right_Easy = 30
    Near = 0 
    Left_Easy = -30
    Left_Far = -70
    Range = [-100,100]
    Values = [-70,-30,0,30,70]
    def check(x):
        if x <= OX.Left_Far: return OX.Left_Far
        elif x > OX.Left_Far and x <= OX.Left_Easy: return OX.Left_Easy
        elif x > OX.Left_Easy and x <= OX.Near: return OX.Near
        elif x > OX.Near and x <= OX.Right_Easy: return OX.Right_Easy
        elif x > OX.Right_Easy: return OX.Right_Far


class OY:
    Down_Far = -80
    Down_Weak = -40
    Down_Top = -20
    Range = [-100,0]
    Values=[-80, -40, -20]
    def check(x):
        if x <= OY.Down_Far: return OY.Down_Far
        elif x > OY.Down_Far and x <= OY.Down_Weak: return OY.Down_Weak
        elif x > OY.Down_Weak and x <= OY.Down_Top: return OY.Down_Top
        elif x > OY.Down_Top: return OY.Down_Top

class Angles:
    Right_Strong = 60
    Right_Weak = 20
    Straight = 0 
    Left_Weak = -20
    Left_Strong = -60
    Range = [-180,180]
    Values = [-60,-20,0,20,60]
    def check(x):
        if x <= Angles.Left_Strong: return Angles.Left_Strong
        elif x > Angles.Left_Strong and x <= Angles.Left_Weak: return Angles.Left_Weak
        elif x > Angles.Left_Weak and x <= Angles.Straight: return Angles.Straight
        elif x > Angles.Straight and x <= Angles.Right_Weak: return Angles.Right_Weak
        elif x > Angles.Right_Weak: return Angles.Right_Weak
    

class Car:
    def __init__(self, x=0, y=0, angle = 0) -> None:
        self.X = x
        self.Y = y
        self.Angle = angle

class Rule:
    def __init__(self, x, y, angle, res) -> None:
        self.X = x
        self.Y = y
        self.Angle = angle
        self.Output = res
        self.Activity = -np.inf
    
    def compute_activity(self, ox, oy, an):
        #val = OX.Values
        #ran = abs(OX.Range[0]) + OX.Range[1]
        sigma = 2#ran/len(val)
        ans_X = np.exp(-1*np.power((ox-OX.check(self.X))/sigma,2))
        
        #val = Angles.Values
        #ran = abs(Angles.Range[0]) + Angles.Range[1]
        sigma = 2#ran/len(val)
        ans_Ang = np.exp(-1*np.power((an-Angles.check(self.Angle))/sigma,2))
        
        sigma = 2
        ans_Y = np.exp(-1*np.power((oy-OY.check(self.Y))/sigma,2))

        self.Activity = ans_X * ans_Ang * ans_Y

    def to_list(self):
        return [self.X, self.Angle, self.Output]

class FuzzyDriver:
    def __init__(self, config) -> None:
        self.Settings = config
        self.Car = Car(np.random.uniform(self.Settings['x']['min']+30,self.Settings['x']['max']-30),
                    np.random.uniform(self.Settings['y']['min']+30,self.Settings['y']['max']-30),
                    np.random.uniform(self.Settings['angle']['min'],self.Settings['angle']['max']))
        self.Rules = []
        self.Results = [0,1,2]
    
    def add_rule(self, rule):
        self.Rules.append(rule)

    def get_decision(self, val):
        n = 1#5
        val = round(val * 1, 2)
        if np.isnan(val): return -20
        else: return Rotation.check(val)
        if val <= -20/n or np.isnan(val): return -20
        elif val > -20/n and val <= -10/n: return -10
        elif val >-10/n and val < 10/n: return 0
        elif val >= 10/n and val <= 20/n: return 10
        else: return 20
        '''
        if val <= -20: return -20
        elif val > -20 and val <= -1: return -10
        elif val >-1 and val <= 1: return 0
        elif val > 1 and val <= 20: return 10
        else: return 20
        '''
    def run(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        win = False
        while True:
            if self.Car.X <= -100 or self.Car.X >= 100 or self.Car.Y >= 0 or self.Car.Y<=-100:
                print("Przegrana")
                break
            if (self.Car.X>=-30 and self.Car.Y >-10) and (self.Car.X<=30 and self.Car.Y >-10):
                print("Wygrana")
                win = True
                break
            activity = []
            output = []
            ans = 0
            
            for rule in fd.Rules:
                rule.compute_activity(self.Car.X, self.Car.Y, self.Car.Angle)
                output.append(rule.Output)
                activity.append(rule.Activity)
            m = sum(activity)
            suma = 0
            for i in range(len(activity)):
                suma = suma + activity[i]*output[i]
            ans = suma / m
            dec = self.get_decision(ans)
            if self.Car.Angle + dec > 180.0:
                self.Car.Angle = -(180 - dec)
            elif self.Car.Angle + dec < -180:
                self.Car.Angle = 180 + dec
            else: self.Car.Angle = self.Car.Angle + dec

            self.Car.X, self.Car.Y = self.find_next_position(self.Car.X, self.Car.Y, self.Settings['move'], self.Car.Angle)       
            # rysowanie
            plt.xlim([self.Settings['x']['min'],self.Settings['x']['max']])
            plt.xlabel("x")
            plt.ylim([self.Settings['y']['min'],self.Settings['y']['max']])
            plt.ylabel("y")
            plt.title("Car: ({0},{1}) ; {2} st".format(round(self.Car.X,2), round(self.Car.Y,2), round(self.Car.Angle,2)))
            plt.grid(True)
                # rysowanie parkingu
            p = patches.Rectangle((self.Settings['ramp']['left'],self.Settings['ramp']['up']),width=self.Settings['ramp']['right']*2,height=self.Settings['ramp']['down'], angle=0, color="blue", alpha=0.25)

            # rysowanie samochodu
            s = patches.Rectangle((self.Car.X-self.Settings['car']['right']/2,self.Car.Y),width=self.Settings['car']['right'],height=self.Settings['car']['down'], angle=-self.Car.Angle, color="red", alpha=0.50)
            plt.plot(self.Car.X, self.Car.Y, '*r')
            
            # dodanie do wykresu
            ax.add_patch(p)
            ax.add_patch(s)
            print("Car: ({0},{1}) ; {2} st ; decyzja: {3} ; wartosc: {4}".format(round(self.Car.X,2), round(self.Car.Y,2), round(self.Car.Angle,2), dec, ans))
            plt.pause(0.5)
            plt.cla()
        return win

    
    def find_next_position(self, x,y, step, angle):
        wsp = 0
        abs_angle = abs(angle)
        alfa, beta = 0,0
        if abs_angle <= 90: 
            wsp = 90
            alfa = wsp - abs_angle
            beta = 180 - (90+alfa)
        if abs_angle > 90 and abs_angle <= 180: 
            wsp = 180
            beta = wsp - abs_angle
            alfa = 180 - (90+beta)
        fig_h = np.cos(beta*np.pi/180) * step
        fig_x = np.cos(alfa*np.pi/180) * step
        ans_x, ans_y = x,y
        # x
        if angle == 90.0: ans_x = x + step
        elif angle == -90.0: ans_x = x - step
        else:
            if angle > 0.0 and angle < 180.0:ans_x = x + fig_x
            elif angle < 0.0 and angle > -180.0: ans_x = x - fig_x
        # y
        if abs_angle == 0: ans_y = y + step
        elif abs_angle == 180: ans_y = y - step
        elif abs_angle == 90.0: ans_y = y
        elif abs_angle > 90: ans_y = y - fig_h
        else: ans_y = y + fig_h
        # return
        return (ans_x, ans_y)


if __name__ == "__main__":
    config = {
        "x":
        {
            "max": 100.0,
            "min": -100.0,
            "range": 200.0
        },
        "y":
        {
            "max": 0.0,
            "min": -100.0,
            "range": 100.0
        },
        "ramp":
        {
            "left": -30.0,
            "right": 30.0,
            "up": 0.0,
            "down":-10.0
        },
        "car":
        {
            "right": 5.0,
            "down":-5.0
        },
        "rotation":
        {
            "min": -20.0,
            "max": 20.0
        },
        "angle":
        {
            "min": -180.0,
            "max": 180.0,
            "range": 360.0
        },
        "move": 5.0
    }

    data = []
    with open('data.txt', 'r') as file:
        temp = file.readlines()
        for line in temp:
            line.replace('\n', '')
            t = line.split(',')
            s = [float(i) for i in t]
            data.append(s)


    fd = FuzzyDriver(config)
    #1
    #fd.add_rule(Rule(OX.Right_Far,Angles.Right_Strong, Rotation.Right_Max))
    nauczone_zasady = {}
    for i in OX.Values:
        nauczone_zasady[str(i)] = {}
        for j in OY.Values:
            nauczone_zasady[str(i)][str(j)] = {}
            for k in Angles.Values:
                nauczone_zasady[str(i)][str(j)][str(k)] = Rule(i,j,k,0)
    
    
    for dana in data:
        x,y,k = OX.check(dana[0]),OY.check(dana[1]),Angles.check(dana[2])
        temp = Rule(x,y,k, dana[3])
        temp.compute_activity(dana[0],dana[1],dana[2])
        if nauczone_zasady[str(x)][str(y)][str(k)].Activity < temp.Activity:
            nauczone_zasady[str(x)][str(y)][str(k)].X = temp.X
            nauczone_zasady[str(x)][str(y)][str(k)].Y = temp.Y
            nauczone_zasady[str(x)][str(y)][str(k)].Angle = temp.Angle
            nauczone_zasady[str(x)][str(y)][str(k)].Activity = temp.Activity
            nauczone_zasady[str(x)][str(y)][str(k)].Output = temp.Output
    
    for i in OX.Values:
        for j in OY.Values:
            for k in Angles.Values:
                if nauczone_zasady[str(i)][str(j)][str(k)].Activity != -np.inf:
                    fd.add_rule(nauczone_zasady[str(i)][str(j)][str(k)])

    suma = 0
    for r in fd.Rules:
        if r.Activity > -np.inf: suma += 1
        print(r.X, r.Y, r.Angle, r.Output ,r.Activity)
    print(suma, "/" ,len(fd.Rules))

    #for osobnik in data:
    #    fd.add_rule(Rule(osobnik[0],osobnik[1], osobnik[2], osobnik[3]))
    '''
        for i in OY.Values:
            for j in OX.Values:
                for k in Angles.Values:
                    suma = suma + 1
    '''

    fd.run()

