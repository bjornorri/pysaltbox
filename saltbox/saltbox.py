import requests
from . import utils

class SaltBox:
    def __init__(self, host, username, password):
        self.host = utils.clean_host(host)
        self.username = utils.hash_string(username)
        self.password = utils.hash_string(password)
        self.session = None


    def get_online_clients(self, retry_allowed=True):
        if self.session == None:
            self._login()

        try:
            url = 'http://{}/clients.htm?t={}'.format(self.host, utils.timestamp())
            httoken = self._get_httoken(url)

            headers = {'Referer': url}
            query = '_tn={}&_t={}'.format(httoken, utils.timestamp())
            url = 'http://{}/cgi/cgi_clients.js?{}'.format(self.host, query)
            res = self.session.get(url, headers=headers)

            js_code = res.text
            client_info = utils.extract_online_client_info(js_code)

            clients = utils.format_online_clients(client_info)
            return clients
        except:
            self.session = None
            if retry_allowed:
                return self.get_online_clients(retry_allowed=False)
            raise Exception('Could not get online clients')

    def logout(self):
        url = "http://{}/index.htm".format(self.host)
        httoken = self._get_httoken(url)

        url = 'http://{}/logout.cgi'.format(self.host)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://{}/index.htm'.format(self.host)
        }
        data = { 'httoken': httoken }
        res = self.session.post(url, headers=headers, data=data)
        self.session = None

    def _login(self):
        self.session = requests.Session()

        url = "http://{}/login.htm".format(self.host)
        httoken = self._get_httoken(url)

        url = 'http://{}/login.cgi'.format(self.host)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://{}/login.htm'.format(self.host)
        }
        data = {
            'usr': self.username,
            'pws': self.password,
            'httoken': httoken
        }
        res = requests.post(url, headers=headers, data=data)
        if 'login.htm' in res.url:
            self.session = None
            message = 'Login failed. Credentials might be invalid or another client might be logged in to the router interface.'
            raise Exception(message)
        self.session.cookies = res.history[0].cookies

    def _get_httoken(self, url):
        if self.session == None:
            self._login()
        res = self.session.get(url)
        return utils.get_httoken_from_html(res.content)
