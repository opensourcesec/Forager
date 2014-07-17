__author__ = 'pendrak0n'
#
# Purpose: Tools for gathering IP addresses, domain names, URL's, etc..
#

from time import sleep
from os import chdir
from xlrd import open_workbook, sheet
import re
import sys
import urllib2
import pdfConverter
import unicodedata


def connect(url):
    try:
        f = urllib2.urlopen(url).readlines()
        return f
    except:
        sys.stderr.write('[!] Failed to access %s\n' % url)
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
    source = '/'.join(regex('domain').findall(url))
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

    print '[+] Gathered %d items from %s' % (count, source)
    return ioc_list


def add2file(filename, ioc_list):
    f = open(filename, 'w+')

    for ioc in ioc_list:
        f.write(ioc + '\n')
    f.close()


def extract(filename):
    if filename[-3:] == 'pdf':
        print '[*] Pulling indicators from PDF'
        f = pdfConverter.convert_pdf_to_txt(filename)
    elif filename[-3:] == 'xls' or filename[-4:] == 'xlsx':
        f = open_workbook(filename)

        datalist = []
        vallist = []
        asciilist = []
        sheet = f.sheet_by_index(0)
        cols = sheet.ncols

        for i in range(cols):
            collist = sheet.col(i)
            datalist = collist + datalist
            for cell in datalist:
                val = cell.value
                if len(val) < 2:
                    pass
                else:
                    vallist.append(val)

        for item in vallist:
            ascii_val = unicodedata.normalize('NFKD', item).encode('ascii', 'ignore')
            asciilist.append(ascii_val)
        f = ', '.join(asciilist)
    else:
        f = open(filename, "r").read()
    ip_patt = regex('ip')
    host_patt = regex('domain')

    ip_list = []
    domain_list = []

    ipaddr = ip_patt.findall(f)
    for i in ipaddr:
        if i in ip_list:
            pass
        else:
            ip_list.append(i)

    domains = host_patt.findall(f)
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