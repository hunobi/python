from requests.api import request
from lib.Hubot import Hubot

if __name__ == "__main__":

    config = {
        'message_type' : {
            'text': True,
            'link': True,
            'files': {
                'image': True,
                'video': True,
                'audio': True,
                'application': True
            }
        },
        'skip_pinned' : True,
        'date': [None, None],
        'limit': 100
    }

    hubocik = Hubot('YOUR_SESSION_ID', config)
    hubocik.channel_id = "ROOM-ID"
    import time
    start = time.time()
    hubocik.run()
    print('\nKoniec',end="\n")
    end =time.time() - start
    print("="*10)
    print("sec:", end)
    print(len(hubocik.Messages))