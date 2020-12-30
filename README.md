# SaltBox

## Important Note
The Salt integration has been removed from Home Assistant because this project relies on web scraping.

## Purpose
This project is developed as part of an integration for [Home Assistant](https://github.com/home-assistant/home-assistant).

## Usage

    from saltbox import SaltBox

    router_host = '192.168.1.1'

    router = SaltBox(router_host, 'username', 'password')
    clients = router.get_online_clients()

## Limits
It seems that the Salt router will stop responding once a certain number of requests have been handled (somewhere between 500 and 1000). It will start responding again after a reboot.

If you try this tool out, I would appreciate feedback on this issue.
