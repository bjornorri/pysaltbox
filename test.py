from saltbox import SaltBox
from time import sleep

router_host = '192.168.1.1'

router = SaltBox(router_host, 'admin', '6gKv6Y4GX2Be')

for i in range(1, 100000):
    try:
        clients = router.get_online_clients()
        print('{} was successful'.format(i))
    except Exception:
        print('{} was unsuccessful'.format(i))
    sleep(1.0)
