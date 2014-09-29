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
        #sys.stdout.write('[!] Could not connect to: %s\n' % url)
        sys.exit(0)


def regex(ioc_type):
    if ioc_type == 'ip':
        pattern = re.compile("[^a-zA-Z0-9\.]((?:(?:[12]\d?\d?|[1-9]\d|[1-9])\.){3}(?:[12]\d?\d?|[\d+]{1,2}))")
    elif ioc_type == 'domain':
        pattern = re.compile("([a-z0-9]+(?:[\-|\.][a-z0-9]+)*\.(?:com|net|ru|org|de|uk|jp|br|pl|info|fr|it|cn|in|su|pw|biz))")
    elif ioc_type == 'md5':
        pattern = re.compile("([A-Fa-f0-9]{32})")
    elif ioc_type == 'sha1':
        pattern = re.compile("\b([A-Fa-f0-9]{40})\b")
    elif ioc_type == 'sha256':
        pattern = re.compile("\b([A-Fa-f0-9]{64})\b")
    elif ioc_type == 'email':
        pattern = re.compile("[a-zA-Z0-9_]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?!([a-zA-Z0-9]*\.[a-zA-Z0-9]*\.[a-zA-Z0-9]*\.))(?:[A-Za-z0-9](?:[a-zA-Z0-9-]*[A-Za-z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?")
    elif ioc_type == 'URL':
        pattern = re.compile("((?:http|ftp|https)\:\/\/(?:[\w+?\.\w+])+[a-zA-Z0-9\~\!\@\#\$\%\^\&\*\(\)_\-\=\+\\\/\?\.\:\;\'\,]+)")
    else:
        print '[!] Invalid type specified.'
        sys.exit(0)
    return pattern


def gather(url, rex):
    ioc_list = []
    count = 0
    f = connect(url)
    #source = '/'.join(regex('domain').findall(url))
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

    #print 'Gathered %d items from %s' % (count, source)
    return ioc_list


def add2file(filename, ioc_list):
    if len(ioc_list) == 0:
        pass
    else:
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
    md5_patt = regex('md5')

    ip_list = []
    domain_list = []
    md5_list = []

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

    md5_hash = md5_patt.findall(f)
    for i in md5_hash:
        if i in md5_list:
            pass
        else:
            md5_list.append(i)

    chdir('intel/')

    add2file(filename + '_ip', ip_list)
    print 'Wrote %d IP indicators to %s_ip' % (len(ip_list), filename)

    add2file(filename + '_domain', domain_list)
    print 'Wrote %d Domain indicators to %s_domain' % (len(domain_list), filename)

    add2file(filename + '_md5', md5_list)
    print 'Wrote %d MD5 hashes to %s_md5' % (len(md5_list), filename)

def update_progress(progress):
    barLength = 20  # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt!\r\n"
    if progress >= .999:
        progress = 1
        status = "Complete!\r\n"
    block = int(round(barLength*progress))
    text = "\r[*] Progress: [{0}] {1}% {2}".format("#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()
