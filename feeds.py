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
        status = "Connected"
        print '[+] Opening Alenvault reputation list. Status: ' + status
    except Exception, e:
        status = "ERROR: " + str(e)

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
