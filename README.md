# SaltBox

## Purpose
This project is developed as part of an integration for [Home Assistant](https://github.com/home-assistant/home-assistant).

## Usage

    from saltbox import SaltBox

    router_host = '192.168.1.1'

    router = SaltBox(router_host, 'username', 'password')
    clients = router.get_online_clients()
    router.logout()
