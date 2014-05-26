__author__ = 'pendrak0n'
#
# Purpose: Import module for pulling and formatting
#          all necessary intelligence feeds
#

from tools import gather, regex

ip_addr = regex('ip')
hostname = regex('domain')


## Pull updates from Malc0de
def malc0de_update():
    iocs = gather('http://malc0de.com/bl/IP_Blacklist.txt', ip_addr)
    f = open('Malc0de-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    print '[+] Malc0de entries retrieved'


## Pull updates from Malware Domain List
def MDL_update():
    iocs = gather('http://www.malwaredomainlist.com/hostslist/ip.txt', ip_addr)
    host_ioc = gather('http://www.malwaredomainlist.com/hostslist/hosts.txt', hostname)

    f = open('MDL-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    f = open('MDL-domains', 'w+')
    for domain in host_ioc:
        f.write(domain + '\n')
    f.close()

    print '[+] MDL entries retrieved!'


## Pulls updates from Feodo Tracker
def feodo_update():
    iocs = gather('https://feodotracker.abuse.ch/blocklist/?download=ipblocklist', ip_addr)
    host_ioc = gather('https://feodotracker.abuse.ch/blocklist/?download=domainblocklist', hostname)

    f = open('Feodo-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    f = open('Feodo-domains', 'w+')
    for domain in host_ioc:
        f.write(domain + '\n')
    f.close()

    print '[+] Feodo Tracker indicators retrieved'


## Pulls updates from reputation.alienvault.com
def alienvault_update():
    iocs = gather('https://reputation.alienvault.com/reputation.generic', ip_addr)

    f = open('Alienvault-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    print '[+] Alienvault indicators retrieved'


## Pulls updates from DShield High Pri suspicious domain list
def dshield_high_update():
    iocs = gather('http://www.dshield.org/feeds/suspiciousdomains_High.txt', hostname)

    f = open('DShield-HighPri-Domains', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    print '[+] DShield HIGH priority suspicious domains updated!'


## Pulls updates from Spyeye Tracker
def spyeye_tracker_update():
    # Grab IP's from Spyeye Tracker
    iocs = gather('https://spyeyetracker.abuse.ch/blocklist.php?download=ipblocklist', ip_addr)
    # Grab the Domains from Spyeye Tracker
    host_ioc = gather('https://spyeyetracker.abuse.ch/blocklist.php?download=domainblocklist', hostname)

    f = open('SpyEye-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    f = open('SpyEye-domains', 'w+')
    for domain in host_ioc:
        f.write(domain + '\n')
    f.close()

    print '[+] Spyeye Tracker domain and IP entries retrieved'


## Pulls updates from Zeus Tracker
def zeus_tracker_update():
    # Grab IP's from Zeus Tracker
    iocs = gather('https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist', ip_addr)
    # Grab the Domains from Zeus Tracker
    host_ioc = gather('https://zeustracker.abuse.ch/blocklist.php?download=domainblocklist', hostname)

    f = open('Zeus-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    f = open('Zeus-domains', 'w+')
    for domain in host_ioc:
        f.write(domain + '\n')
    f.close()

    print '[+] Zeus domain and IP entries retrieved'


## Pulls updates from Palevo Tracker
def palevo_tracker_update():
    # Grab IP's from Palevo Tracker
    iocs = gather('https://palevotracker.abuse.ch/blocklists.php?download=ipblocklist', ip_addr)
    # Grab the Domains from Palevo Tracker
    host_ioc = gather('https://palevotracker.abuse.ch/blocklists.php?download=domainblocklist', hostname)

    f = open('Palevo-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    f = open('Palevo-domains', 'w+')
    for domain in host_ioc:
        f.write(domain + '\n')
    f.close()

    print '[+] Palevo domain and IP entries retrieved'


## Pulls updates
def openbl_update():
    iocs = gather('http://www.openbl.org/lists/base.txt', ip_addr)

    f = open('OpenBL-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    print '[+] Retrieved last 90 days of blacklisted IP addresses from OpenBL'


def maldomains_update():
    iocs = gather('http://mirror1.malwaredomains.com/files/domains.txt', hostname)

    f = open('Maldomains', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    print '[+] Retrieved latest entries from malwaredomains!'
