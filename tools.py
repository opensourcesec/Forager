__author__ = 'pendrak0n'
#
# Purpose: Tools for gathering IP addresses, domain names, URL's, etc..
#

from time import sleep
import re
import sys
import urllib2


def connect(url):
    try:
        f = urllib2.urlopen(url).readlines()
        return f
    except:
        sys.stderr.write('[!] Failed to access %s' % url)
        sys.exit(0)


def regex(type):
    if type == 'ip':
        pattern = re.compile('((?:[12]\d?\d?\.){3}[12]\d?\d?)')
    elif type == 'domain':
        pattern = re.compile('([a-z0-9]+(?:[\-|\.][a-z0-9]+)*\.[a-z]{2,5}(?:[0-9]{1,5})?)')
    else:
        print '[!] Invalid type specified.'
        sys.exit(0)
    return pattern


def gather(url, rex):
    ioc_list = []
    count = 0
    f = connect(url)
    sleep(2)
    for line in f:
        if line.startswith('/') or line.startswith('#') or line.startswith('\n'):
            pass
        else:
            ioc = rex.findall(line)
            ioc = ''.join(ioc)
            if ioc in ioc_list:
                pass
            else:
                ioc_list.append(ioc)
                count += 1

    print '[+] Gathered %d indicators from %s' % (count, url)
    return ioc_list