#!/usr/bin/env python
import os

domain = 'codex.so'
cmd = 'whois ' + domain + '| grep -E \'Registry Expiry Date\: .*\''
os.system(cmd)
