import requests
from . import exceptions
from . import utils

TIMEOUT = 5.0

class SaltBox:
    def __init__(self, host, username, password):
        self.host = utils.clean_host(host)
        self.username = utils.hash_string(username)
        self.password = utils.hash_string(password)
        self.session = None

    def get_online_clients(self):
        try:
            self._login()
            url = 'http://{}/clients.htm?t={}'.format(self.host, utils.timestamp())
            httoken = self._get_httoken(url)

            headers = {'Referer': url}
            query = '_tn={}&_t={}'.format(httoken, utils.timestamp())
            url = 'http://{}/cgi/cgi_clients.js?{}'.format(self.host, query)
            res = self.session.get(url, headers=headers, timeout=TIMEOUT)
            self._logout()

            js_code = res.text
            client_info = utils.extract_online_client_info(js_code)

            clients = utils.format_online_clients(client_info)
            return clients
        except exceptions.RouterLoginException as e:
            raise
        except Exception as e:
            message = 'The router is not reachable.'
            raise exceptions.RouterNotReachableException(message)

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
        res = self.session.post(url, headers=headers, data=data, timeout=TIMEOUT)
        if 'login.htm' in res.url:
            self.session = None
            message = 'Login failed. Credentials might be invalid or another client might be logged in to the router interface.'
            raise exceptions.RouterLoginException(message)

    def _logout(self):
        url = "http://{}/index.htm".format(self.host)
        httoken = self._get_httoken(url)

        url = 'http://{}/logout.cgi'.format(self.host)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://{}/index.htm'.format(self.host)
        }
        data = { 'httoken': httoken }
        res = self.session.post(url, headers=headers, data=data, timeout=TIMEOUT)
        self.session = None

    def _get_httoken(self, url):
        if self.session == None:
            self._login()
        res = self.session.get(url, timeout=TIMEOUT)
        return utils.get_httoken_from_html(res.content)
