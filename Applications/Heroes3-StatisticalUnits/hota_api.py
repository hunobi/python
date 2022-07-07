import json, requests, os

def download_file(url, path):
    with requests.get(unit['imageUrl']) as res:
        if res.status_code == 200:
            res.raise_for_status()
            with open(path, 'wb') as f:
                for chunk in res.iter_content(chunk_size=8192): f.write(chunk)
            print("[ok]\t", url)
        else:
            print("[err]\t",url)
        return res.status_code


if __name__ == "__main__":
    url = "http://51.15.192.116:4500/creature/{0}"
    cities = ["castle","rampart","tower","inferno","necropolis","dungeon","stronghold","fortress","conflux","cove"]
    db = {}
    for city in cities:
        res = requests.get(url.format(city))
        db[city] = []
        if res.status_code == 200:
            data = res.json()
            os.makedirs(city, exist_ok=True)
            for unit in data:
                dmg = unit['damage'].split(' ')[0].split('-')
                if len(dmg) > 1: dmg = {'min': int(dmg[0]), 'max': int(dmg[1])}
                else: dmg = {'min': int(dmg[0]), 'max': int(dmg[0])}
                unit['damage'] = dmg
                path = city+'/'+unit['id']+'.gif'
                if download_file(unit['imageUrl'],path) == 200:
                    unit['imageUrl'] = path
                else:
                    unit['imageUrl'] = ""
                db[city].append(unit)

    json.dump(db, open("db.json", 'w'))
                
