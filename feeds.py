__author__ = 'y0xda'
#
# Purpose: Import module for pulling and formatting
#          all necessary intelligence feeds
#

from tools import gather, regex, add2file

ip_addr = regex('ip')
domains = regex('domain')

class FeedModules:
    ## Malc0de
    def malc0de_update(self):
        iocs = gather('http://malc0de.com/bl/IP_Blacklist.txt', ip_addr)
        add2file('Malc0de-ip', iocs)


    ## Malware Domain List
    def MDL_update(self):
        iocs = gather('http://www.malwaredomainlist.com/hostslist/ip.txt', ip_addr)
        host_ioc = gather('http://www.malwaredomainlist.com/hostslist/hosts.txt', domains)

        add2file('MDL-ip', iocs)
        add2file('MDL-domains', host_ioc)


    ## Feodo Tracker
    def feodo_update(self):
        iocs = gather('https://feodotracker.abuse.ch/blocklist/?download=ipblocklist', ip_addr)
        host_ioc = gather('https://feodotracker.abuse.ch/blocklist/?download=domainblocklist', domains)

        add2file('Feodo-ip', iocs)
        add2file('Feodo-domains', host_ioc)


    #reputation.alienvault.com
    def alienvault_update(self):
        iocs = gather('https://reputation.alienvault.com/reputation.generic', ip_addr)
        add2file('Alienvault-ip', iocs)


    ## DShield High Pri suspicious domain list
    def dshield_high_update(self):
        host_iocs = gather('http://www.dshield.org/feeds/suspiciousdomains_High.txt', domains)
        add2file('DShield-HighPri-Domains', host_iocs)


    ## Spyeye Tracker
    def spyeye_tracker_update(self):
        iocs = gather('https://spyeyetracker.abuse.ch/blocklist.php?download=ipblocklist', ip_addr)
        host_ioc = gather('https://spyeyetracker.abuse.ch/blocklist.php?download=domainblocklist', domains)

        add2file('SpyEye-ip', iocs)
        add2file('SpyEye-domains', host_ioc)


    ## Zeus Tracker
    def zeus_tracker_update(self):
        iocs = gather('https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist', ip_addr)
        host_ioc = gather('https://zeustracker.abuse.ch/blocklist.php?download=domainblocklist', domains)

        add2file('Zeus-ip', iocs)
        add2file('Zeus-domains', host_ioc)


    ## Palevo Tracker
    def palevo_tracker_update(self):
        iocs = gather('https://palevotracker.abuse.ch/blocklists.php?download=ipblocklist', ip_addr)
        host_ioc = gather('https://palevotracker.abuse.ch/blocklists.php?download=domainblocklist', domains)

        add2file('Palevo-ip', iocs)
        add2file('Palevo-domains', host_ioc)


    ## OpenBL
    def openbl_update(self):
        iocs = gather('http://www.openbl.org/lists/base.txt', ip_addr)
        add2file('OpenBL-ip', iocs)


    ## MalwareDomains
    def malwaredomains_update(self):
        iocs = gather('http://mirror1.malwaredomains.com/files/domains.txt', domains)
        add2file('Malwaredomains', iocs)


    ## NoThink Honeypots -- DNS Traffic
    def nothink_malware_dns_update(self):
        iocs = gather('http://www.nothink.org/blacklist/blacklist_malware_dns.txt', ip_addr)
        host_ioc = gather('http://www.nothink.org/blacklist/blacklist_malware_dns.txt', domains)

        add2file('NoThink-DNS-IP', iocs)
        add2file('NoThink-DNS-Domains', host_ioc)


    ## NoThink Honeypots -- HTTP Traffic
    def nothink_malware_http_update(self):
        iocs = gather('http://www.nothink.org/blacklist/blacklist_malware_http.txt', ip_addr)
        host_iocs = gather('http://www.nothink.org/blacklist/blacklist_malware_http.txt', domains)

        add2file('NoThink-HTTP-IP', iocs)
        add2file('NoThink-HTTP-Domains', host_iocs)


    ## NoThink Honeypots -- IRC Traffic
    def nothink_malware_irc_update(self):
        iocs = gather('http://www.nothink.org/blacklist/blacklist_malware_irc.txt', ip_addr)
        add2file('NoThink-IRC', iocs)

    ## Tor Exit Node List	
    def Tor_Exit_Nodes_update(self):
	iocs = gather('https://onionoo.torproject.org/details?type=relay&running=true', ip_addr)
		
	add2file('TorExitNodes', iocs)