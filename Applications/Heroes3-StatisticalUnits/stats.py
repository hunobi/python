import json, math
import matplotlib.pyplot as plt
import numpy as np

def moc(atak, obrona, dmg, hp, speed):
    return math.sqrt(1+(atak+obrona+hp+speed))*dmg

def moc2(atak, obrona, dmg, hp, speed, dyst):
    if dyst: return math.sqrt(1+((atak+obrona+hp+speed))*1.5)*dmg
    return math.sqrt(1+(atak+obrona+hp+speed))*dmg


if __name__ == "__main__":
    data = json.load(open('db.json', 'r'))
    units = []
    for city in data:
        for unit in data[city]:
            unit['damage-avg'] = (unit['damage']['min']+unit['damage']['max'])/2.0
            unit['damage-min'] = unit['damage']['min']
            unit['damage-max'] = unit['damage']['max']
            unit.pop("damage")
            g_tmp = unit['growth'].split(' ')
            unit['growth'] = int(g_tmp[0])
            if len(g_tmp)>1:
                g_tmp = int(g_tmp[1].replace('(','').replace(')',''))
                unit['growth-bonus'] = g_tmp
            else:  unit['growth-bonus'] = 0
            units.append(unit)
    print(units)
    json.dump(units, open('units.json', 'w'))
    '''
    groups = {}
    for unit in units:
        if unit['level'] in groups:
            groups[unit['level']].append(unit)
        else:
            groups[unit['level']] = []
            groups[unit['level']].append(unit)

    group_name = "7+"
    bar_width = 0.35
    
    names = [unit['name'] for unit in groups[group_name]]
    dmg = [unit['damage']['mean'] for unit in groups[group_name]]
    hp = [unit['health'] for unit in groups[group_name]]
    speed = [unit['speed'] for unit in groups[group_name]]
    cost = [unit['valueMoney'] for unit in groups[group_name]]
    values = [unit['aiValue'] for unit in groups[group_name]]
    myValues = [round(moc(unit['attack'],unit['defense'],unit['damage']['mean'],unit['health'],unit['speed']),2) for unit in groups[group_name]]

    city_names = [city for city in data]
    city_powers = [sum([unit['aiValue'] for unit in data[city]]) for city in data]
    city_myPower = [sum([round(moc(unit['attack'],unit['defense'],unit['damage']['mean'],unit['health'],unit['speed']),2) for unit in data[city]]) for city in data]
    city_cost = [sum([unit['valueMoney'] for unit in data[city]]) for city in data]
    print(city_names)
    print(city_powers)

   
    x = np.arange(len(city_names))
    fig, ax = plt.subplots()
    #gr1 = ax.bar(x-bar_width/2, values, width=bar_width, label="Orginal power")
    #gr2 = ax.bar(x+bar_width/2, myValues, width=bar_width, label="My power")
    gr1 = ax.bar(x-bar_width/2, city_powers, width=bar_width, label="City power (orginal)")
    gr2 = ax.bar(x+bar_width/2, city_myPower, width=bar_width, label="City power (my alg)")

    ax.set_xticks(x, city_names)
    ax.legend()
    ax.bar_label(gr1, padding=3)
    ax.bar_label(gr2, padding=3)
    fig.tight_layout()
    plt.show()
    '''