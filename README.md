The Forager
============

Threat Intelligence hunter-gatherer: Fetches intel from various open-source feeds and formats them into new-line separated files for each feed. Also provides functionality to search through gathered indicators efficiently.
 
NOTE:
The script creates a file for malicious IP addresses and a file for malicious domains for EACH feed in feeds.py, and then places them in a folder entitled "intel" 


Feeds
--------

(Invoked with --feeds)

* 'list' -- Lists all feeds and allows user to choose a single feed to update. 
* 'update' -- Updates all feed modules listed in Forager

Hunting 
---------

(Invoked with --hunt)

* '-f [file path]' Provides the capability to search through the intel directory results for a specific list of indicators
* '-s [IPv4 address]' Searches through intel directory for a single IP address

Extract
--------

(Invoked with --extract)

* Reads in a file and extracts IP address and domain indicators
* Places the extracted indicators into the intel directory 
