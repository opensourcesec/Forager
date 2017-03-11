__author__ = 'byt3smith'
#
# Purpose: Tools for gathering IP addresses, domain names, URL's, etc..
#

from time import sleep
from os import chdir, path
from xlrd import open_workbook, sheet
import re
import sys
import urllib.request, urllib.error, urllib.parse
from . import pdf_converter
import unicodedata
from colorama import Fore, Back, Style, init

init(autoreset=True) ## Initialize colorama

def connect(url):
    try:
        f = urllib.request.urlopen(url).readlines()
        return f
    except:
        sys.exit(0)


def regex(ioc_type):
    ioc_patts = {
        "ip":b"((?:(?:[12]\d?\d?|[1-9]\d|[1-9])(?:\[\.\]|\.)){3}(?:[12]\d?\d?|[\d+]{1,2}))",
        "domain":b"([A-Za-z0-9]+(?:[\-|\.][A-Za-z0-9]+)*(?:\[\.\]|\.)(?:com|net|edu|ru|org|de|uk|jp|br|pl|info|fr|it|cn|in|su|pw|biz|co|eu|nl|kr|me))",
        "md5":b"\W([A-Fa-f0-9]{32})(?:\W|$)",
        "sha1":b"\W([A-Fa-f0-9]{40})(?:\W|$)",
        "sha256":b"\W([A-Fa-f0-9]{64})(?:\W|$)",
        "email":b"[a-zA-Z0-9_]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?!([a-zA-Z0-9]*\.[a-zA-Z0-9]*\.[a-zA-Z0-9]*\.))(?:[A-Za-z0-9](?:[a-zA-Z0-9-]*[A-Za-z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?",
        "URL":b"((?:http|ftp|https)\:\/\/(?:[\w+?\.\w+])+[a-zA-Z0-9\~\!\@\#\$\%\^\&\*\(\)_\-\=\+\\\/\?\.\:\;]+)",
        "yara":b"(rule\s[\w\W]{,30}\{[\w\W\s]*\})"
    }

    try:
        pattern = re.compile(ioc_patts[ioc_type])
    except re.error:
        print('[!] Invalid type specified.')
        sys.exit(0)

    return pattern


def gather(url, rex):
    ioc_list = []
    count = 0
    f = connect(url)
    sleep(2)
    for line in f:
        if line.startswith(b"/") or line.startswith(b"#") or line.startswith(b"\n"):
            pass
        else:
            ioc = rex.findall(line)
            for i in ioc:
                if i in ioc_list:
                    pass
                else:
                    ioc_list.append(i)
                    count += 1

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
            f.write(ioc.decode("utf-8") + '\n')
        f.close()


def extract(filename):
    ### Determine filetype to define how IOCs are processed
    if filename[-3:] == 'pdf':
        f = bytes(pdf_converter.convert_pdf_to_txt(filename), 'utf-8')
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
        f = bytes(', '.join(asciilist))
    else:
        f = bytes(open(filename, "r").read(), 'utf-8')

    ### Setup patterns for extraction
    ip_patt = regex('ip')
    host_patt = regex('domain')
    md5_patt = regex('md5')
    sha1_patt = regex('sha1')
    sha256_patt = regex('sha256')
    yara_patt = regex('yara')

    ### Declare temp list vars to store IOCs
    ip_list = []
    domain_list = []
    md5_list = []
    sha1_list = []
    sha256_list = []
    yara_list = []

    ### Iterate over lists of matched IOCs
    ipaddr = ip_patt.findall(f)
    for i in ipaddr:
        # Remove brackets if defanged
        i = re.sub(b'\[\.\]', b'.', i)

        if i in ip_list:
            pass
        else:
            ip_list.append(i)

    domains = host_patt.findall(f)
    for i in domains:
        # Remove brackets if defanged
        i = re.sub(b'\[\.\]', b'.', i)

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

    sha1_hash = sha1_patt.findall(f)
    for i in sha1_hash:
        if i in sha1_list:
            pass
        else:
            sha1_list.append(i)

    sha256_hash = sha256_patt.findall(f)
    for i in sha256_hash:
        if i in sha1_list:
            pass
        else:
            sha256_list.append(i)

    yara_rules = yara_patt.findall(f)
    for i in yara_rules:
        if i in yara_list:
            pass
        else:
            yara_list.append(i)


    ### Create _ioc file
    chdir('data/intel/')
    base = path.basename(filename)
    base_noext = path.splitext(base)[0]

    banner = '''
+-------------------+
|       RESULTS     |
+-------------------+'''
    print(banner)

    ### Write IOCs to files
    with open(base_noext + '_ioc', 'w+') as f:
        for i in ip_list:
            f.write(i.decode("utf-8") + '\n')
        f.write("\n")
        print('IPv4 Addresses [' + (Fore.GREEN + '%d' % (len(ip_list)) + Fore.RESET if len(ip_list) > 0 else Fore.RED + '%d' % (len(ip_list)) + Fore.RESET) + ']')

        for d in domain_list:
            f.write(d.decode("utf-8") + '\n')
        f.write("\n")
        print('Domain Names [' + (Fore.GREEN + '%d' % (len(domain_list)) + Fore.RESET if len(domain_list) > 0 else Fore.RED + '%d' % (len(domain_list)) + Fore.RESET) + ']')

        for m in md5_list:
            f.write(m.decode("utf-8") + '\n')
        f.write("\n")
        print('MD5 Hashes [' + (Fore.GREEN + '%d' % (len(md5_list)) + Fore.RESET if len(md5_list) > 0 else Fore.RED + '%d' % (len(md5_list)) + Fore.RESET) + ']')

        for y in yara_list:
            f.write(y.decode("utf-8") + '\n')
        f.write("\n")
        print('YARA Rules [' + (Fore.GREEN + '%d' % (len(yara_list)) + Fore.RESET if len(yara_list) > 0 else Fore.RED + '%d' % (len(yara_list)) + Fore.RESET) + ']')

        for s1 in sha1_list:
            f.write(s1.decode("utf-8") + '\n')
        f.write("\n")
        print('SHA1 Hashes [' + (Fore.GREEN + '%d' % (len(sha1_list)) + Fore.RESET if len(sha1_list) > 0 else Fore.RED + '%d' % (len(sha1_list)) + Fore.RESET) + ']')

        for s2 in sha256_list:
            f.write(s2.decode("utf-8") + '\n')
        f.write("\n")
        print('SHA256 Hashes [' + (Fore.GREEN + '%d' % (len(sha256_list)) + Fore.RESET if len(sha256_list) > 0 else Fore.RED + '%d' % (len(sha256_list)) + Fore.RESET) + ']')

    print(Fore.GREEN + "\n[+]" + Fore.RESET + " IOCs written to %s" % base_noext + '_ioc!')


def update_progress(progress):
    barLength = 20  # Modify this value to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = Fore.RED + "Halt!\r\n"
    if progress >= .999:
        progress = 1
        status = Fore.GREEN + " Complete!\r\n"
    block = int(round(barLength*progress))
    text = "\r[*] Progress: [{0}] {1}% {2}".format("#"*block + "-"*(barLength-block), round(progress*100), status)
    sys.stdout.write(text)
    sys.stdout.flush()
