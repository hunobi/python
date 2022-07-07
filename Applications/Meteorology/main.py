import math

# p0 - bazowe ciśnienie na 0 n.p.m
# h - wysokość nad poziomem morza
# t_o - temperatura otoczenia
def cisnienie(p0, h, t):
  return p0 * math.exp(-((0.02897*9.80665)/(8.3144598 * (t+273.15)))*h)

# t_o , t_w = temperatura otoczenia, wilgotna
# h - wysokość nad poziomem morza
# p0 - bazowe ciśnienie na 0 n.p.m
def wilgoc(t_o, t_w, h, p0):
  p = p0 * math.exp(-((0.02897*9.80665)/(8.3144598 * (t_o+273.15)))*h)
  E = math.exp(((17.27*t_o)/(t_o+237.3))+1.8091)
  E_p = math.exp(((17.27*t_w)/(t_w+237.3))+1.8091)
  e = E_p - 7.9446*(10**-4) * (t_o-t_w)*p
  return e/E

# H - Wilgotność z zakresu [0,1]
# t_o - temperatura otoczenia [st. C]
def punkt_rosy(H, t_o):
  return math.pow(H,1/8) * (112 + (0.9 * t_o)) + (0.1*t_o) - 112

# p0 - bazowe ciśnienie na 0 n.p.m
# p  - ciśnienie w miejscowosci
# t_o - temperatura otoczenia
def wysokosc(p0, p, t_o):
  right = -((0.02897*9.80665)/(8.3144598 * (t_o+273.15)))
  left = math.log(p / p0)
  return left/right

# t_o - temperatura otoczenia   [C]
# p  - ciśnienie w miejscowosci [hPA]
# h - wysokosc npm  [m]
# err - blad [0.0004]
def stopien_baryczny(t_o, p, h, err):
   b = (8000/p)*(1+err*t_o)
   p_t = p + (h/b)
   t =  h/100* 0.6
   p_sr = (p+p_t)/2
   return (8000/p_sr)*(1+err*((t+t_o)/2))

# t_o - temperatura otoczenia   [C]
# p  - ciśnienie w miejscowosci [hPA]
# h - wysokosc npm  [m]
# err - blad [0.0004]
def cisnienie_wzgledne(t_o, p, h, err):
  st = stopien_baryczny(t_o, p, h, err)
  return p + (h/st)

# t_o - temperatura otoczenia   [C]
# t_w - mokra temperatura otoczenia   [C]
# p0  - ciśnienie bazowe 0m npm [hPA]
# h - wysokosc npm  [m]
# err - blad [0.0004]
def test(t_o, t_w, h, p0, err):
     H = wilgoc(t_o,t_w,h,p0)
     rosa = punkt_rosy(H, t_o)
     p = cisnienie(p0, h, t_o)
     return (H, rosa, p, cisnienie_wzgledne(t_o, p, h, err))