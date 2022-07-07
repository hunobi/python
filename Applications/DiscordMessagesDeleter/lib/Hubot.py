import requests
import time

class Hubot:
    def __init__(self, token, config):
        #basic config
        self.session_token = token
        self.user_id = None
        self.channel_id = None
        self.message_type = config['message_type']
        self.skip_pinned = config['skip_pinned']
        self.date = config['date']
        self.limit = config['limit']
        #authorization
        self.headers = {'authorization': self.session_token}
        #var
        self.Channels = []
        self.Messages = []


    def run(self):
        try:
            self.get_user_id()
            self.delete_messages()
        except Exception as e:
            print('\n',str(e),end="\n")

    def get_user_id(self):
        url = 'https://discord.com/api/v9/users/@me'
        res = requests.get(url, headers=self.headers)
        if res.status_code != 200: raise ConnectionError("http code", res.status_code)
        data = res.json()
        self.user_id = data['id']

    def get_server(self):
        url = 'https://discord.com/api/v9/users/@me/guilds'

    def get_server_channels(self, server_id):
        url = 'https://discord.com/api/v9/guilds/{0}}/channels'.format(server_id)

    def get_priv_channels(self):
        url = 'https://discord.com/api/v9/users/@me/channels'

    def delete_messages(self):
        def get_count_messages(channel_id, user_id):
            url = 'https://discord.com/api/v9/channels/{0}/messages/search?author_id={1}'.format(channel_id,user_id)
            res = requests.get(url, headers=self.headers)
            if res.status_code != 200: 
                print(res.content)
            data = res.json()
            return data['total_results']

        def delete_request(channel_id, msg_id):
            url = 'https://discord.com/api/v9/channels/{0}/messages/{1}'.format(channel_id, msg_id)
            res = requests.delete(url, headers=self.headers)
            if res.status_code == 204: return True
            elif res.status_code == 429:
                penalty = res.json()['retry_after']
                if penalty > 0.5:
                    self.sleep(res.json()['retry_after']-0.5)
            return False

        def load_messages(url, channel_id, user_id, limit=100, last_message_id=None):
            if last_message_id is None:
                url = url.format(channel_id, limit)
            else:
                url = url.format(channel_id, last_message_id,limit )
            res = requests.get(url, headers=self.headers)
            if res.status_code != 200: return print(res.status_code)
            data = res.json()
            Msgs = []
            Last_ID = ''
            for message in data:
                if message['type'] != 3 and message['author']['id'] == user_id:
                    if not (self.skip_pinned and message['pinned']):
                        msg = {
                            'id': message['id'],
                            'content': message['content'],
                            'pinned' : message['pinned'],
                            'embeds': message['embeds'],
                            'timestamp': message['timestamp'],
                            'attachments': message['attachments']
                        }
                        Msgs.append(msg)
                Last_ID = message['id']
            return [Msgs, Last_ID]
            

        length_all = get_count_messages(self.channel_id, self.user_id)
        count = 0

        url_first = 'https://discord.com/api/v9/channels/{0}/messages?limit={1}'
        url_next = 'https://discord.com/api/v9/channels/{0}/messages?before={1}&limit={2}'
        
        memory = None
        self.sleep()
        while count < length_all:
            if memory is None: 
                memory = load_messages(url_first, self.channel_id, self.user_id, 100)
            else: 
                memory = load_messages(url_next, self.channel_id, self.user_id, 100, memory[1])
            
            self.sleep()

            results = len(memory[0])
            if results < 1: continue

            i = 0
            while results > 0:
                flag = delete_request(self.channel_id, memory[0][i]['id'])
                if flag:
                    count += 1
                    i+=1
                    results-=1
                    print(count, '/', length_all, end='\r')
                self.sleep()

    def sleep(self, sec=0.5):
        time.sleep(sec)