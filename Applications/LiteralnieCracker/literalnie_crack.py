import json, requests

def get_sid(url):
    res = requests.get(url)
    js = json.loads(res.text[1:])
    return js['sid']

def get_password(url, sid):
    send_post(url+'&sid='+sid,"40")
    response = send_get(url+'&sid='+sid)
    temp = response.split('42["slowo",')[1]
    json_str = ""
    flag = False
    for i in temp:
        if i == "{": flag = True
        if flag:json_str += i
        if i == "}": break
    json_obj = json.loads(json_str)
    return json_obj['word']

def send_post(url, code):
    res = requests.post(url, data=code)
    return res.text

def send_get(url):
    res = requests.get(url)
    return res.text

if __name__ == "__main__":
    url = "https://serwer.literalnie.fun/socket.io/?EIO=4&transport=polling&t=NyeTiu6"
    sid = get_sid(url)
    word = get_password(url,sid)
    print("Password:\t",word)
    input("--end--")