#
# Purpose: Import module for pulling and formatting
#          all necessary intelligence feeds
#

from urllib2 import urlopen
import re


## Pull updates from Malc0de
def malc0de_update():
    malcode_file = open('malc0de-ip-blacklist', 'w+')
    url = urlopen('http://malc0de.com/bl/IP_Blacklist.txt')
    print '[*] Connected to Malc0de database, retrieving latest entries..'
    text = url.readlines()
    for line in text:
        if '/' in line:
            pass
        else:
            malcode_file.write(line)
    malcode_file.close()

    print '[+] Malc0de entries retrieved'


## Pull updates from Malware Domain List
def MDL_update():
    text = urlopen('http://www.malwaredomainlist.com/hostslist/hosts.txt').readlines()
    mylist = []
    hostlist = []

    ## Iterate through lines gathered from MDL to format each line ##
    for line in text:
        mylist.append(line)
    newstr = ''.join(mylist)  # Makes each line a part of $mylist ##
    pat = re.compile('127.0.0.1\s([^\#\r\n]*)')   # Matches anything  after localhost
    for match in pat.findall(newstr):  # Searches for match from our ocmpiled regex
        hostlist.append(match)   # Then appends it to our host list

    hoststr = ''.join(hostlist)
    formatted = re.sub(r" ", "\n", hoststr) # Uses regex to substitute a whitespace for a new line
    file = open('MDL-domains', 'w+')
    file.write(formatted)

    ## Gathering IP Addresses ##
    mdl_ip = urlopen('http://www.malwaredomainlist.com/hostslist/ip.txt').read()
    print '[*] Connected to malwaredomainlist.com..'

    ip_file = open('MDL-IP', 'w+')  # Opening iP file to save entries #
    ip_file.write(mdl_ip)
    print '[+] MDL entries retrieved!'


## Pulls updates from Files.Dontneedcoffee.com
def fdnc_update():
    urls = ['http://files.dontneedcoffee.com/tracking/AnglerEK/domains.txt',
            'http://files.dontneedcoffee.com/tracking/AnglerRU8080/domains.txt',
            'http://files.dontneedcoffee.com/tracking/AnglerMiu/domains.txt',
            'http://files.dontneedcoffee.com/tracking/Neutrino/domains.txt',
            'http://files.dontneedcoffee.com/tracking/NuclearPack/domains.txt',
            'http://files.dontneedcoffee.com/tracking/StyxKein/domains.txt',
            'http://files.dontneedcoffee.com/tracking/Styx/domains.txt',
            'http://files.dontneedcoffee.com/tracking/Magnitude/domains.txt',
            'http://files.dontneedcoffee.com/tracking/Grandsoft/domains.txt',
            'http://files.dontneedcoffee.com/tracking/WhiteHole/domains.txt',
            'http://files.dontneedcoffee.com/tracking/FakeCodecRotator/domains.txt',
            'http://files.dontneedcoffee.com/tracking/Sakura_KovtZaccess/domains.txt',
            'http://files.dontneedcoffee.com/tracking/BrowLockCyber/domains.txt',
            'http://files.dontneedcoffee.com/tracking/Goon/domains.txt',
            'http://files.dontneedcoffee.com/tracking/Sutra2NP/domains.txt',
            'http://files.dontneedcoffee.com/tracking/SweetOrange/domains.txt']

    counter = 1

    for url in urls:
        print '[*] Fetching %s' %url
        text = urlopen(url).readlines()
        domain_pattern = re.compile("\;([^\;]+\.[^\;]+)\;")
        iPpat = re.compile(r"\;([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)")
        hostlist = []
        iplist = []
        ipcount = 0

        ### Fetching domain names from each line ###
        for line in text:
            rawhost = domain_pattern.findall(line)
            host = ', '.join(rawhost)
            hostlist.append(host)
        domains = '\n'.join(hostlist)

        ### Now fetching IP addresses ###
        for line in text:
            rawhost_ip = iPpat.findall(line)
            host_ip = ', '.join(rawhost_ip)
            if host_ip in iplist:
                pass
            else:
                iplist.append(host_ip)
                ipcount += 1
        ip_adds = '\n'.join(iplist)

        print '[+] Gathered %d malicious IP addresses from %s' %(ipcount, url)

        if counter == 1:
            domains_file = 'AnglerEK-domains'
            ip_file = 'AnglerEK-ip'
        elif counter == 2:
            domains_file = 'AnglerRU8080-domains'
            ip_file = 'AnglerRU8080-ip'
        elif counter == 3:
            domains_file = 'Miuref-domains'
            ip_file = 'Miuref-ip'
        elif counter == 4:
            domains_file = 'Neutrino-domains'
            ip_file = 'Neutrino-ip'
        elif counter == 5:
            domains_file = 'NuclearPack-domains'
            ip_file = 'NuclearPack-ip'
        elif counter == 6:
            domains_file = 'StyxKein-domains'
            ip_file = 'StyxKein-ip'
        elif counter == 7:
            domains_file = 'Styx-domains'
            ip_file = 'Styx-ip'
        elif counter == 8:
            domains_file = 'Magnitude-domains'
            ip_file = 'Magnitude-ip'
        elif counter == 9:
            domains_file = 'Grandsoft-domains'
            ip_file = 'Grandsoft-ip'
        elif counter == 10:
            domains_file = 'WhiteHole-domains'
            ip_file = 'WhiteHole-ip'
        elif counter == 11:
            domains_file = 'FakeCodecRotator-domains'
            ip_file = 'FakeCodecRotator-ip'
        elif counter == 12:
            domains_file = 'Sakura_KovtZaccess-domains'
            ip_file = 'Sakura_KovtZaccess-ip'
        elif counter == 13:
            domains_file = 'BrowLockCyber-domains'
            ip_file = 'BrowLockCyber-ip'
        elif counter == 14:
            domains_file = 'Goon-domains'
            ip_file = 'Goon-ip'
        elif counter == 15:
            domains_file = 'Sutra2NP-domains'
            ip_file = 'Sutra2NP-ip'
        elif counter == 16:
            domains_file = 'SweetOrange-domains'
            ip_file = 'SweetOrange-ip'

        file = open(ip_file, 'w+')
        file.write(ip_adds)
        file.close()
        file = open(domains_file, 'w+')
        file.write(domains)
        file.close()

        print '...Writing information to file.'
        counter += 1

    print '[+] Files.dontneedcoffee entries retrieved'


## Pulls updates from Feodo Tracker
def feodo_update():
    # Grab the Domains from Feodo Tracker
    file = open('Feodo-domain-blacklist', 'w+')
    url = urlopen('https://feodotracker.abuse.ch/blocklist/?download=domainblocklist')
    print '[*] Accessing Feodo Tracker domain list, retrieving latest entries..'
    text = url.readlines()
    for line in text:
        if '#' in line:
            pass
        else:
            file.write(line)
    file.close()

    # Grab IP's from Feodo Tracker
    file = open('Feodo-ip-blacklist', 'w+')
    url = urlopen('https://feodotracker.abuse.ch/blocklist/?download=ipblocklist')
    print '[*] Accessing Feodo Tracker IP blacklist, retrieving latest entries..'
    text = url.readlines()
    for line in text:
        if '#' in line:
            pass
        else:
            file.write(line)
    file.close()

    print '[+] Feodo Tracker domain and IP entries retrieved'


## Pulls updates from reputation.alienvault.com
def alienvault_update():
    ip_list = []
    av_pat = re.compile(r'(^.*)\s#')
    try:
        feed = urlopen("https://reputation.alienvault.com/reputation.generic").readlines()
        status = "Connected!"
        print '[*] Opening Alenvault reputation list. Status: ' + status
    except Exception, e:
        status = "[-] ERROR: " + str(e)

    for line in feed:
        if line.startswith('#') or line.startswith('\n'):
            pass
        else:
            host = av_pat.findall(line)  # Find all IP's in a given line using regex
            host_ip = ', '.join(host)  # join hosts into a list of strings
            ip_list.append(host_ip)  # add hosts to new list

    ip_adds = '\n'.join(ip_list)  # Join all hosts into new string separated by lines

    file = open('Alienvault_ip', 'w+')
    for line in ip_adds:
        file.write(line)
    file.close()


## Pulls updates from DShield High Pri suspicious domain list
def dshield_high_update():
    try:
        feed = urlopen("http://www.dshield.org/feeds/suspiciousdomains_High.txt").readlines()
        status = "Connected"
        print '[+] Opening DShield Suspicious Domain list. Status: ' + status
    except Exception, e:
        status = "ERROR: " + str(e)

    ipfile = open('Dshield_suspicious_HIGHPRI', 'w+')

    for line in feed:
        if line.startswith('#') or line.startswith('\n') or 'Site' in line:
            pass
        else:
            ipfile.write(line)

    print '[+] DShield HIGH priority suspicious domains updated!'
    ipfile.close()


## Pulls updates from Spyeye Tracker
def spyeye_tracker_update():
    # Grab the Domains from Spyeye Tracker
    file = open('Spyeye-domain-blacklist', 'w+')
    url = urlopen('https://spyeyetracker.abuse.ch/blocklist.php?download=domainblocklist')
    print '[*] Accessing Spyeye Tracker domain list, retrieving latest entries..'
    text = url.readlines()
    for line in text:
        if '#' in line:
            pass
        else:
            file.write(line)
    file.close()

    # Grab IP's from Spyeye Tracker
    file = open('Spyeye-ip-blacklist', 'w+')
    url = urlopen('https://spyeyetracker.abuse.ch/blocklist.php?download=ipblocklist')
    print '[*] Accessing Spyeye Tracker IP blacklist, retrieving latest entries..'
    text = url.readlines()
    for line in text:
        if '#' in line:
            pass
        else:
            file.write(line)
    file.close()

    print '[+] Spyeye Tracker domain and IP entries retrieved'


## Pulls updates from Zeus Tracker
def zeus_tracker_update():
    # Grab the Domains from Zeus Tracker
    file = open('Zeus-domain-blacklist', 'w+')
    url = urlopen('https://zeustracker.abuse.ch/blocklist.php?download=domainblocklist')
    print '[*] Accessing Zeus Tracker domain list, retrieving latest entries..'
    text = url.readlines()
    for line in text:
        if '#' in line:
            pass
        else:
            file.write(line)
    file.close()

    # Grab IP's from Zeus Tracker
    file = open('Zeus-ip-blacklist', 'w+')
    url = urlopen('https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist')
    print '[*] Accessing Zeus Tracker IP blacklist, retrieving latest entries..'
    text = url.readlines()
    for line in text:
        if '#' in line:
            pass
        else:
            file.write(line)
    file.close()

    print '[+] Zeus domain and IP entries retrieved'


## Pulls updates from Palevo Tracker
def palevo_tracker_update():
    # Grab the Domains from Palevo Tracker
    file = open('Palevo-domain-blacklist', 'w+')
    url = urlopen('https://palevotracker.abuse.ch/blocklists.php?download=domainblocklist')
    print '[*] Accessing Palevo Tracker domain list, retrieving latest entries..'
    text = url.readlines()
    for line in text:
        if '#' in line:
            pass
        else:
            file.write(line)
    file.close()

    # Grab IP's from Palevo Tracker
    file = open('Palevo-ip-blacklist', 'w+')
    url = urlopen('https://palevotracker.abuse.ch/blocklists.php?download=ipblocklist')
    print '[*] Accessing Palevo Tracker IP blacklist, retrieving latest entries..'
    text = url.readlines()
    for line in text:
        if '#' in line:
            pass
        else:
            file.write(line)
    file.close()

    print '[+] Palevo domain and IP entries retrieved'


## Pulls updates
def openbl_update():
    feed = "http://www.openbl.org/lists/base.txt"
    iplist = []
    try:
        addrs = urlopen(feed).readlines()
        status = "Connected!"
        print '[+] Attempting to reach the OpenBL server. Status: ' + status
    except Exception, e:
        status = "[-] ERROR: " + str(e)
        print status

    for line in addrs:
        if line.startswith('#') or line.startswith('\n'):
            pass
        else:
            iplist.append(line)  # add hosts to new list

    file = open('OpenBL-ip', 'w+')
    for item in iplist:
        file.write(item)
    file.close()

    print '[+] Retrieved last 90 days of blacklisted IP addresses from OpenBL'


def maldomains_update():
    domainlist = []
    feedurl = 'http://mirror1.malwaredomains.com/files/domains.txt'
    try:
        feed = urlopen(feedurl).readlines()
        status = "Connected!"
        print '[*] Opening Malware Domains blacklist. Status: ' + status
    except Exception, e:
        status = "[-] ERROR: " + str(e)

    for line in feed:
        if line.startswith('#') or line.startswith('\n'):
            pass
        else:
            split_mdl = re.split(r'\t+', line.lstrip('\t'))
            if unicode(split_mdl[0]).isnumeric():
                split_mdl.pop(0)
            domain = split_mdl[0] + '\n'
            domainlist.append(domain)

    file = open('MalDomains', 'w+')
    for item in domainlist:
        file.write(item)
    file.close()

    print '[+] Retrieved latest entries from %s!' % feedurl