#
# Purpose: Import module for pulling and formatting
#          all necessary intelligence feeds
#

from urllib2 import urlopen
import re
from tools import gather, regex

## Pull updates from Malc0de
def malc0de_update():
    ip_addr = regex('ip')
    iocs = gather('http://malc0de.com/bl/IP_Blacklist.txt', ip_addr)
    f = open('Malc0de-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    print '[+] Malc0de entries retrieved'


## Pull updates from Malware Domain List
def MDL_update():
    ip_addr = regex('ip')
    hostname = regex('domain')
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
    ip_addr = regex('ip')
    hostname = regex('domain')
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
    ip_addr = regex('ip')
    iocs = gather('https://reputation.alienvault.com/reputation.generic', ip_addr)

    f = open('Alienvault-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    print '[+] Alienvault indicators retrieved'


## Pulls updates from DShield High Pri suspicious domain list
def dshield_high_update():
    hostname = regex('domain')
    iocs = gather('http://www.dshield.org/feeds/suspiciousdomains_High.txt', hostname)

    f = open('DShield-HighPri-Domains', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    print '[+] DShield HIGH priority suspicious domains updated!'


## Pulls updates from Spyeye Tracker
def spyeye_tracker_update():
    hostname = regex('domain')
    ip_addr = regex('ip')

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
    hostname = regex('domain')
    ip_addr = regex('ip')

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
    hostname = regex('domain')
    ip_addr = regex('ip')

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


##Pulls Angler EK FDNC
def fdnc_angler_update():
    hostname = regex('domain')
    ip_addr = regex('ip')

    # Grab IP's from FDNC tracker
    iocs = gather('http://files.dontneedcoffee.com/tracking/AnglerEK/domains.txt', ip_addr)
    # Grab the Domains from FDNC Tracker
    host_ioc = gather('http://files.dontneedcoffee.com/tracking/AnglerEK/domains.txt', hostname)

    f = open('AnglerEK-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    f = open('AnglerEK-domains', 'w+')
    for domain in host_ioc:
        f.write(domain + '\n')
    f.close()

    print '[+] Angler Exploit Kit domain and IP entries retrieved'

##Pulls Angler EK RU:8080 FDNC
def fdnc_angler8080_update():
    hostname = regex('domain')
    ip_addr = regex('ip')

    # Grab IP's from FDNC tracker
    iocs = gather('http://files.dontneedcoffee.com/tracking/AnglerRU8080/domains.txt', ip_addr)
    # Grab the Domains from FDNC Tracker
    host_ioc = gather('http://files.dontneedcoffee.com/tracking/AnglerRU8080/domains.txt', hostname)

    f = open('Angler8080EK-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    f = open('Angler8080EK-domains', 'w+')
    for domain in host_ioc:
        f.write(domain + '\n')
    f.close()

    print '[+] Angler 8080 Exploit Kit domain and IP entries retrieved'

##Pulls BlackHole EK FDNC
def fdnc_Blackhole_update():
    hostname = regex('domain')
    ip_addr = regex('ip')

    # Grab IP's from FDNC tracker
    iocs = gather('http://files.dontneedcoffee.com/tracking/BHEK/domains.txt', ip_addr)
    # Grab the Domains from FDNC Tracker
    host_ioc = gather('http://files.dontneedcoffee.com/tracking/BHEK/domains.txt', hostname)

    f = open('BlackholeEK-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    f = open('BlackholeEK-domains', 'w+')
    for domain in host_ioc:
        f.write(domain + '\n')
    f.close()

    print '[+] BlackHole Exploit Kit domain and IP entries retrieved'

##Pulls BlackOS EK FDNC
def fdnc_BlackOS_update():
    hostname = regex('domain')
    ip_addr = regex('ip')

    # Grab IP's from FDNC tracker
    iocs = gather('http://files.dontneedcoffee.com/tracking/BlackOS/domains.txt', ip_addr)
    # Grab the Domains from FDNC Tracker
    host_ioc = gather('http://files.dontneedcoffee.com/tracking/BlackOS/domains.txt', hostname)

    f = open('BlackOS-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    f = open('BlackOS-domains', 'w+')
    for domain in host_ioc:
        f.write(domain + '\n')
    f.close()

    print '[+] BlackOS domain and IP entries retrieved'

##Pulls FlashPack EK FDNC
def fdnc_FlashPack_update():
    hostname = regex('domain')
    ip_addr = regex('ip')

    # Grab IP's from FDNC tracker
    iocs = gather('http://files.dontneedcoffee.com/tracking/FlashPack/domains.txt', ip_addr)
    # Grab the Domains from FDNC Tracker
    host_ioc = gather('http://files.dontneedcoffee.com/tracking/FlashPack/domains.txt', hostname)

    f = open('FlashPack-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    f = open('FlashPack-domains', 'w+')
    for domain in host_ioc:
        f.write(domain + '\n')
    f.close()

    print '[+] FlashPack domain and IP entries retrieved'

##Pulls Goon EK FDNC
def fdnc_GoonEK_update():
    hostname = regex('domain')
    ip_addr = regex('ip')

    # Grab IP's from FDNC tracker
    iocs = gather('http://files.dontneedcoffee.com/tracking/Goon/domains.txt', ip_addr)
    # Grab the Domains from FDNC Tracker
    host_ioc = gather('http://files.dontneedcoffee.com/tracking/Goon/domains.txt', hostname)

    f = open('GoonEK-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    f = open('GoonEK-domains', 'w+')
    for domain in host_ioc:
        f.write(domain + '\n')
    f.close()

    print '[+] Goon Exploit Kit domain and IP entries retrieved'

##Pulls GrandSoft EK FDNC
def fdnc_GrandsoftEK_update():
    hostname = regex('domain')
    ip_addr = regex('ip')

    # Grab IP's from FDNC tracker
    iocs = gather('http://files.dontneedcoffee.com/tracking/Grandsoft/domains.txt', ip_addr)
    # Grab the Domains from FDNC Tracker
    host_ioc = gather('http://files.dontneedcoffee.com/tracking/Grandsoft/domains.txt', hostname)

    f = open('GrandsoftEK-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    f = open('GrandsoftEK-domains', 'w+')
    for domain in host_ioc:
        f.write(domain + '\n')
    f.close()

    print '[+] Grandsoft Exploit Kit domain and IP entries retrieved'


    ##Pulls Magnitude EK FDNC
def fdnc_MagnitudeEK_update():
    hostname = regex('domain')
    ip_addr = regex('ip')

    # Grab IP's from FDNC tracker
    iocs = gather('http://files.dontneedcoffee.com/tracking/Magnitude/domains.txt', ip_addr)
    # Grab the Domains from FDNC Tracker
    host_ioc = gather('http://files.dontneedcoffee.com/tracking/Magnitude/domains.txt', hostname)

    f = open('MagnitudeEK-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    f = open('MagnitudeEK-domains', 'w+')
    for domain in host_ioc:
        f.write(domain + '\n')
    f.close()

    print '[+] Magnitude Exploit Kit domain and IP entries retrieved'


        ##Pulls Neutrino EK FDNC
def fdnc_NeutrinoEK_update():
    hostname = regex('domain')
    ip_addr = regex('ip')

    # Grab IP's from FDNC tracker
    iocs = gather('http://files.dontneedcoffee.com/tracking/Neutrino/domains.txt', ip_addr)
    # Grab the Domains from FDNC Tracker
    host_ioc = gather('http://files.dontneedcoffee.com/tracking/Neutrino/domains.txt', hostname)

    f = open('NeutrinoEK-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    f = open('NeutrinoEK-domains', 'w+')
    for domain in host_ioc:
        f.write(domain + '\n')
    f.close()

    print '[+] Neutrino Exploit Kit domain and IP entries retrieved'



        ##Pulls Nuclear EK FDNC
def fdnc_NuclearEK_update():
    hostname = regex('domain')
    ip_addr = regex('ip')

    # Grab IP's from FDNC tracker
    iocs = gather('http://files.dontneedcoffee.com/tracking/NuclearPack/domains.txt', ip_addr)
    # Grab the Domains from FDNC Tracker
    host_ioc = gather('http://files.dontneedcoffee.com/tracking/NuclearPack/domains.txt', hostname)

    f = open('NuclearEK-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    f = open('NuclearEK-domains', 'w+')
    for domain in host_ioc:
        f.write(domain + '\n')
    f.close()

    print '[+] Nuclear Exploit Kit domain and IP entries retrieved'



        ##Pulls SweetOrange EK FDNC
def fdnc_SweetOrangeEK_update():
    hostname = regex('domain')
    ip_addr = regex('ip')

    # Grab IP's from FDNC tracker
    iocs = gather('http://files.dontneedcoffee.com/tracking/SweetOrange/domains.txt', ip_addr)
    # Grab the Domains from FDNC Tracker
    host_ioc = gather('http://files.dontneedcoffee.com/tracking/SweetOrange/domains.txt', hostname)

    f = open('SweetOrangeEK-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    f = open('SweetOrangeEK-domains', 'w+')
    for domain in host_ioc:
        f.write(domain + '\n')
    f.close()

    print '[+] SweetOrange Exploit Kit domain and IP entries retrieved'

        ##Pulls Styx EK FDNC
def fdnc_StyxEK_update():
    hostname = regex('domain')
    ip_addr = regex('ip')

    # Grab IP's from FDNC tracker
    iocs = gather('http://files.dontneedcoffee.com/tracking/Styx/domains.txt', ip_addr)
    # Grab the Domains from FDNC Tracker
    host_ioc = gather('http://files.dontneedcoffee.com/tracking/Styx/domains.txt', hostname)

    f = open('StyxEK-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    f = open('StyxEK-domains', 'w+')
    for domain in host_ioc:
        f.write(domain + '\n')
    f.close()

    print '[+] Styx Exploit Kit domain and IP entries retrieved'

        ##Pulls FakeCodec EK FDNC
def fdnc_FakeCodecEK_update():
    hostname = regex('domain')
    ip_addr = regex('ip')

    # Grab IP's from FDNC tracker
    iocs = gather('http://files.dontneedcoffee.com/tracking/FakeCodecRotator/domains.txt', ip_addr)
    # Grab the Domains from FDNC Tracker
    host_ioc = gather('http://files.dontneedcoffee.com/tracking/FakeCodecRotator/domains.txt', hostname)

    f = open('FakeCodecEK-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    f = open('FakeCodecEK-domains', 'w+')
    for domain in host_ioc:
        f.write(domain + '\n')
    f.close()

    print '[+] FakeCodec Exploit Kit domain and IP entries retrieved'

        ##Pulls StyxPL EK FDNC
def fdnc_StyxPLEK_update():
    hostname = regex('domain')
    ip_addr = regex('ip')

    # Grab IP's from FDNC tracker
    iocs = gather('http://files.dontneedcoffee.com/tracking/Sakura_KovtZaccess/domains.txt', ip_addr)
    # Grab the Domains from FDNC Tracker
    host_ioc = gather('http://files.dontneedcoffee.com/tracking/Sakura_KovtZaccess/domains.txt', hostname)

    f = open('StyxPLEK-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    f = open('StyxPLEK-domains', 'w+')
    for domain in host_ioc:
        f.write(domain + '\n')
    f.close()

    print '[+] Styx PL Exploit Kit domain and IP entries retrieved'


        ##Pulls BAD TDS FDNC
def fdnc_BadTDS_update():
    hostname = regex('domain')
    ip_addr = regex('ip')

    # Grab IP's from FDNC tracker
    iocs = gather('http://files.dontneedcoffee.com/tracking/Sutra2NP/domains.txt', ip_addr)
    # Grab the Domains from FDNC Tracker
    host_ioc = gather('http://files.dontneedcoffee.com/tracking/Sutra2NP/domains.txt', hostname)

    f = open('BadTDS-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    f = open('BadTDS-domains', 'w+')
    for domain in host_ioc:
        f.write(domain + '\n')
    f.close()

    print '[+] Bad TDS domain and IP entries retrieved'


        ##Pulls BrowLock Cyber FDNC
def fdnc_Browlock_update():
    hostname = regex('domain')
    ip_addr = regex('ip')

    # Grab IP's from FDNC tracker
    iocs = gather('http://files.dontneedcoffee.com/tracking/BrowLockCyber/domains.txt', ip_addr)
    # Grab the Domains from FDNC Tracker
    host_ioc = gather('http://files.dontneedcoffee.com/tracking/BrowLockCyber/domains.txt', hostname)

    f = open('BrowLock-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    f = open('BrowLock-domains', 'w+')
    for domain in host_ioc:
        f.write(domain + '\n')
    f.close()

    print '[+] BrowLock Cyber domain and IP entries retrieved'



## Pulls updates
def openbl_update():
    ip_addr = regex('ip')
    iocs = gather('http://www.openbl.org/lists/base.txt', ip_addr)

    f = open('OpenBL-ip', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    print '[+] Retrieved last 90 days of blacklisted IP addresses from OpenBL'


def maldomains_update():
    hostname = regex('domain')
    iocs = gather('http://mirror1.malwaredomains.com/files/domains.txt', hostname)

    f = open('Maldomains', 'w+')
    for ioc in iocs:
        f.write(ioc + '\n')
    f.close()

    print '[+] Retrieved latest entries from malwaredomains!'