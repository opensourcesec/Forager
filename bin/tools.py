__author__ = 'byt3smith'
#
# Purpose: Tools for gathering IP addresses, domain names, URL's, etc..
#

from time import sleep
from os import chdir, path
from xlrd import open_workbook, sheet
import re
import sys
import urllib2
import pdfConverter
import unicodedata
from colorama import Fore, Back, Style, init

init(autoreset=True) ## Initialize colorama

def connect(url):
    try:
        f = urllib2.urlopen(url).readlines()
        return f
    except:
        #sys.stdout.write('[!] Could not connect to: %s\n' % url)
        sys.exit(0)


def regex(ioc_type):
    if ioc_type == 'ip':
        pattern = re.compile("((?:(?:[12]\d?\d?|[1-9]\d|[1-9])\.){3}(?:[12]\d?\d?|[\d+]{1,2}))")
    elif ioc_type == 'domain':
        pattern = re.compile("([a-z0-9]+(?:[\-|\.][a-z0-9]+)*\.(?:[a-z]{2,5}))")
    elif ioc_type == 'md5':
        pattern = re.compile("([A-Fa-f0-9]{32})")
    elif ioc_type == 'sha1':
        pattern = re.compile("\b([A-Fa-f0-9]{40})\b")
    elif ioc_type == 'sha256':
        pattern = re.compile("\b([A-Fa-f0-9]{64})\b")
    elif ioc_type == 'email':
        pattern = re.compile("[a-zA-Z0-9_]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?!([a-zA-Z0-9]*\.[a-zA-Z0-9]*\.[a-zA-Z0-9]*\.))(?:[A-Za-z0-9](?:[a-zA-Z0-9-]*[A-Za-z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?")
    elif ioc_type == 'URL':
        pattern = re.compile("((?:http|ftp|https)\:\/\/(?:[\w+?\.\w+])+[a-zA-Z0-9\~\!\@\#\$\%\^\&\*\(\)_\-\=\+\\\/\?\.\:\;]+)")
    elif ioc_type == 'yara':
        pattern = re.compile("(rule\s[\w\W]{,30}\{[\w\W\s]*\})")
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
        patt = regex('ip')
        test = patt.match(ioc_list[0])
        if test is None:
            f = open(filename, 'a+')
        else:
            f = open(filename, 'w+')

        for ioc in ioc_list:
            f.write(ioc + '\n')
        f.close()


def extract(filename):
    if filename[-3:] == 'pdf':
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
    yara_patt = regex('yara')

    ip_list = []
    domain_list = []
    md5_list = []
    yara_list = []

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

    yara_rules = yara_patt.findall(f)
    for i in yara_rules:
        if i in yara_list:
            pass
        else:
            yara_list.append(i)


    chdir('intel/')
    base = path.basename(filename)
    base_noext = path.splitext(base)[0]

    with open(base_noext + '_ioc', 'w+') as f:
        for i in ip_list:
            f.write(i + '\n')
        print(Fore.GREEN + '\n[+]' + Fore.RESET),
        print 'Wrote %d IP indicators to %s_ioc' % (len(ip_list), base_noext)
        for d in domain_list:
            f.write(d + '\n')
        print(Fore.GREEN + '[+]' + Fore.RESET),
        print 'Wrote %d Domain indicators to %s_ioc' % (len(domain_list), base_noext)
        for m in md5_list:
            f.write(m + '\n')
        print(Fore.GREEN + '[+]' + Fore.RESET),
        print 'Wrote %d MD5 hashes to %s_ioc' % (len(md5_list), base_noext)
        for y in yara_list:
            f.write(y + '\n')
        print(Fore.GREEN + '[+]' + Fore.RESET),
        print 'Wrote %d YARA rules to %s_ioc' % (len(yara_list), base_noext)

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
