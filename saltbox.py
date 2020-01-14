import requests
import utils
from py_mini_racer import py_mini_racer

class SaltBox:
    def __init__(self, host, username, password):
        self.host = host
        self.username = utils.hash_string(username)
        self.password = utils.hash_string(password)
        self.session = None


    def get_online_clients(self, retry_allowed=True):
        if self.session == None:
            self._login()

        try:
            url = '{}/clients.htm?t={}'.format(self.host, utils.timestamp())
            httoken = self._get_httoken(url)

            headers = {'Referer': url}
            query = '_tn={}&_t={}'.format(httoken, utils.timestamp())
            url = '{}/cgi/cgi_clients.js?{}'.format(self.host, query)
            res = self.session.get(url, headers=headers)

            js_code = res.text
            ctx = py_mini_racer.MiniRacer()
            ctx.eval(js_code)
            client_info = ctx.eval('online_client')
            clients = utils.format_online_clients(client_info)
            return clients
        except:
            self.session = None
            if retry_allowed:
                return self.get_online_clients(retry_allowed=False)
            raise Exception('Could not get online clients')

    def _login(self):
        self.session = requests.Session()

        url = "{}/login.htm".format(self.host)
        httoken = self._get_httoken(url)

        url = '{}/login.cgi'.format(self.host)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': '{}/login.htm'.format(self.host)
        }
        data = {
            'usr': self.username,
            'pws': self.password,
            'httoken': httoken
        }
        res = requests.post(url, headers=headers, data=data)
        if 'login.htm' in res.url:
            self.session = None
            raise Exception('Login failed')
        self.session.cookies = res.history[0].cookies

    def _get_httoken(self, url):
        if self.session == None:
            self._login()
        res = self.session.get(url)
        return utils.get_httoken_from_html(res.content)
