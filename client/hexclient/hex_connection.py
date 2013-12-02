import json
import requests

class HexCommunicationError(Exception):
    pass

class HexConnection(object):
    "Takes care of talking with the hex server"

    def __init__(self, hex_server='http://localhost:6543'):
        self.hex_server = hex_server

    def setup(self, password):
        return self.api_request('/api/setup', 'post', data={'password': password})

    def authenticate(self, name, animal):
        response = self.api_request("/api/users/authenticate", 'post',
                data={'name': name, 'spirit_animal': animal})
        return response['result'] == 'OK'

    def get_user(self, name):
        return self.api_request("/api/users/%s" % name, 'get')

    def get_users(self):
        return self.api_request('/api/users', 'get')

    def create_user(self, name, animal):
        return self.api_request("/api/users", "post", 
                {'name': name, 'spirit_animal': animal})

    def create_spell(self, user_name, animal, name, setup=None, loop=None):
        return self.api_request('/api/spells', 'post',
                {'user_name': user_name, 'spirit_animal': animal, 'name': name, 
                'setup': setup, 'loop': loop})

    def run_spell(self):
        return self.api_request('/api/spells/run', 'get')
        
    jsonHeaders = {
        "Content-Type": 'application/json', 
        'Accept': 'application/json'
    }

    def api_request(self, path, method, data=None):
        methods = {
            'get': requests.get,
            'post': requests.post
        }
        response = methods[method](self.hex_server + path, 
                data=json.dumps(data), headers=self.jsonHeaders)
        if response.status_code != 200:
            raise HexCommunicationError()
        return json.loads(response.content)

if __name__ == '__main__':
    hc = HexConnection()
    hc.get_users()['users']
    hc.get_user('chris')['user']
    assert hc.authenticate('chris', 'eerie bison') == True
