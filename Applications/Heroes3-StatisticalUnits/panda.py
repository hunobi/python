import matplotlib.pyplot as plt
import pandas as pd
data = pd.read_json("units.json")
cities = list(set(data['town']))
total_cost = []
total_population = []
total_hp = []
total_avg_dmg = []
total_speed = []
total_random_dmg = []
total_attack = []
total_defense=[]

population_bonus = 2
for city in cities:
    city_units = data[data['town']==city]
    upgraded_units = city_units[[lvl.find('+')>-1 for lvl in city_units['level']]]
    city_population = upgraded_units['growth']*population_bonus + upgraded_units['growth-bonus']
    city_cost = city_population * upgraded_units['valueMoney']
    total_cost.append(city_cost.sum())
    help = upgraded_units['growth'] + upgraded_units['growth-bonus']
    total_population.append(city_population.sum())
    total_hp.append((upgraded_units['health']*help).sum())
    total_avg_dmg.append((upgraded_units['damage-avg']*help).sum()) # tu uwzględnic double ataki
    total_speed.append((upgraded_units['speed']*help).sum())
    total_random_dmg.append(((upgraded_units['damage-max']-upgraded_units['damage-min'])*help).sum())
    total_attack.append((help * upgraded_units['attack']).sum())
    total_defense.append((help * upgraded_units['defense']).sum())

print(cities)
print(total_cost)
tmp = pd.DataFrame({
    #"total_cost":total_cost, 
   # "total_population": total_population,
    "total_hp": total_hp,
    "total_avg_dmg": total_avg_dmg,
    "total_speed": total_speed,
    "total_rng_dmg":total_random_dmg,
    "total_attack":total_attack,
    "total_defense": total_defense,
    "town": cities
    }, 
    index=cities)
print(tmp)
print(tmp.corr())
print(tmp.sort_values(by=['total_rng_dmg']))
srednie = {}
for i in tmp.iloc:
    print(i)
    temp = []
    for j in tmp.iloc:
        val = 0
        if i['total_hp'] <j['total_hp']: val+=1
        if i['total_avg_dmg'] <j['total_avg_dmg']: val+=1
        if i['total_speed'] <j['total_speed']: val+=1
        if i['total_attack'] <j['total_attack']: val+=1
        if i['total_defense'] <j['total_defense']: val+=1
        if i['total_rng_dmg'] >j['total_rng_dmg']: val+=1
        temp.append(val)
    srednie[i['town']] = temp
sr = pd.DataFrame(srednie,index=cities)
print(sr)
tmp.plot.bar(rot=0, grid=True)
plt.show()