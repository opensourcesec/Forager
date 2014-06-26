__author__ = 'pendrak0n'
#
# Purpose: Tools for gathering IP addresses, domain names, URL's, etc..
#

from time import sleep
import re
import sys
import urllib2
from os import chdir


def connect(url):
    try:
        f = urllib2.urlopen(url).readlines()
        return f
    except:
        sys.stderr.write('[!] Failed to access %s' % url)
        sys.exit(0)


def regex(type):
    if type == 'ip':
        pattern = re.compile('((?:(?:[12]\d?\d?|[1-9]\d|[1-9])\.){3}(?:[12]\d?\d?|[\d+]{1,2}))')
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
            for i in ioc:
                if i in ioc_list:
                    pass
                else:
                    ioc_list.append(i)
                    count += 1

    print '[+] Gathered %d indicators from %s' % (count, url)
    return ioc_list


def add2file(filename, ioc_list):
    f = open(filename, 'w+')

    for ioc in ioc_list:
        f.write(ioc + '\n')
    f.close()


def extract(filename):
    ip_patt = regex('ip')
    host_patt = regex('domain')

    ip_list = []
    domain_list = []

    f = open(filename, "r").readlines()
    for line in f:
        ipaddr = ip_patt.findall(line)
        for i in ipaddr:
            if i in ip_list:
                pass
            else:
                ip_list.append(i)

        domains = host_patt.findall(line)
        for i in domains:
            if i in domain_list:
                pass
            else:
                domain_list.append(i)

    chdir('intel/')

    add2file(filename + '_ip', ip_list)
    print '[+] Wrote IP indicators to %s_ip' % filename

    add2file(filename + '_domain', domain_list)
    print '[+] Wrote Domain indicators to %s_domain' % filename