Target audience: 
Web developers or systems administrators who want to quickly set up multiple websites on Apache web server for development or testing purposes.

After a standard Apache web server installation, run this script to quickly set up multiple websites (Named Virtual Hosts)

This script will do the following:

Ask where to place the websites' home directories (defaults to /var/www/)
Ask for all the domains you want to be created at once.
   [use domain names like: domain1.com  (not www.domain1.com)]

Create the Apache site conf file for each website (/etc/apache2/sites-available)
Create self-signed SSL keys for each website (/etc/apache2/ssl)
Create web home directories with barebones index.html

Auto enables Apache SSL module
Auto enables the websites

Adds the domains to your /etc/hosts and couple them to 127.0.1.1 (in the localhost range 127.0.0.0/8).

