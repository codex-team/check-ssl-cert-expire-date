# -*- coding: utf-8 -*-

import socket
import ssl
import datetime
import requests
import sys
from pywhois import whois
from config import DOMAINS, DAYS_LIMIT_CERT, DAYS_LIMIT_DOMAIN, APITOKEN, CHATID

date_fmt = r'%b %d %H:%M:%S %Y %Z'
MESSAGE_CERTIFICATE_EXPIRED = "⚠️ SSL expired on {}"
MESSAGE_HOSTNAME_MISMATCH = "⚠️ SSL hostname mismatch on {}"
MESSAGE_EXCEPTION = "⚠️ SSL exception on {}: {}"


def send_message(text):
    """
    Send message to the Telegram via API
    :param text: message
    """
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(APITOKEN)
    data = {
        'text': text,
        'chat_id': CHATID,
        'disable_web_page_preview': True
    }
    requests.post(url, json=data)


def ssl_expiry_datetime(hostname):
    """
    Get SSL expiration date
    Source link: https://serverlesscode.com/post/ssl-expiration-alerts-with-lambda/
    :param hostname: hostname
    :return datetime object or None
    """
    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )

    # 3 second timeout because Lambda has runtime limitations
    conn.settimeout(3.0)

    try:
        conn.connect((hostname, 443))
        ssl_info = conn.getpeercert()
    except ssl.SSLError as e:
        if e.verify_code == 10:
            send_message(MESSAGE_CERTIFICATE_EXPIRED.format(hostname))
        elif e.verify_code == 62:
            send_message(MESSAGE_HOSTNAME_MISMATCH.format(hostname))
        else:
            send_message(MESSAGE_EXCEPTION.format(hostname, e.verify_message))
        return None

    # Parse the string from the certificate into a Python datetime object
    return datetime.datetime.strptime(ssl_info['notAfter'], date_fmt)


def check_ssl_time_left(domain):
    """
    Count days left and generate a warning message
    :param domain: domain
    :return:
    """
    cert_expire_at = ssl_expiry_datetime(domain)
    if cert_expire_at is not None:
        time_left = cert_expire_at - datetime.datetime.now()
        message = 'SSL cert for {} has {}'.format(domain, days_left_to_format_string(time_left))
        if time_left.days <= DAYS_LIMIT_CERT:
            message = '{}'.format(message)
            send_message(message)
        print(message)


def days_left_to_format_string(timedelta):
    """
    Calculate days left from timedelta and return string message
    :param timedelta: timedelta object
    :return: string message with the days left
    """
    return '{} day{} left'.format(timedelta.days,  ('s', '')[timedelta.days == 1])


if not APITOKEN:
    print('No APITOKEN was found in config file.')
    exit()


for domain in DOMAINS:
    try:
        check_ssl_time_left(domain)
        w = whois.whois(domain)           
        expdays = 'Expiration date for {} has {}'.format(domain, days_left_to_format_string(w.expiration_date-datetime.datetime.now()))
        print(expdays)
        if (w.expiration_date-datetime.datetime.now()).days <= DAYS_LIMIT_DOMAIN:
            send_message(w.expiration_date)    
    except Exception as e:
        print("Unexpected error:", e)
