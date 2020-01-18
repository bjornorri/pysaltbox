import hashlib
import base64
import time
import re
from bs4 import BeautifulSoup

def timestamp():
    return int(round(time.time() * 1000))

def hash_string(str):
    md5 = hashlib.md5(str.encode('utf-8')).hexdigest()
    sha = hashlib.sha512(md5.encode('utf-8')).hexdigest()
    return sha

def clean_host(str):
    return str.split('//')[-1]


def get_httoken_from_html(html):
    seed = get_httoken_seed_from_html(html)
    token = base64.b64decode(seed).decode('utf-8')
    return token

def get_httoken_seed_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    img_tags = soup.find_all('img')
    for tag in img_tags:
        if tag['src'].startswith('data:'):
            return tag['src'][78:]
    raise Exception('Could not get httoken seed from html')

def extract_online_client_info(str):
    regex = 'var\s*online_client\s*=\s*(\[[\s\S]*?\])'
    res = re.search(regex, str)
    info_str = res.group(1)
    info = eval(info_str)
    return info

def format_online_clients(data):
    clients = []
    chunk_size = 8
    for i in range(0, len(data), chunk_size):
        info = data[i:i+chunk_size]
        client = {
            'name': info[0],
            'ip': info[1],
            'mac': info[2],
            'interface': info[4],
            'ipv6_gua': info[5],
            'ipv6_lla': info[6],
        }
        clients.append(client)
    return clients
