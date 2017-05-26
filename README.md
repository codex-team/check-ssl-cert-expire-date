# SSL certs expire date checker
Python-script for checking certs life time for domains.

## Requirements
- requests

## Install

1. Clone this rep

2. Set up config.py

3. Set up autorun

Edit cron
```bash
crontab -e
```

To run script at 8 am every day add this line
```bash
0 8 * * * python3 /root/check-ssl-cert-expire-date/main.py
```
