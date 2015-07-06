After a standard Apache installation, run this script to quickly set up multiple websites to be hosted by the server.

This script will:

1) Ask for the home directory where all websites directories will go under. (default '/var/www')

2) Set up simple templated website for each website www.domain.com with permanent redirect from domain.com (i.e. http://jared.com redirected to http://www.jared.com)

3) Use and enable a minimal Named VirtualHost configuration for each website inside Apache config directory (default '/etc/apache2/sites-available')

4) Each website has their own access.log and error.log

5) Create and install self-signed SSL key for each website and enable HTTPS.

=======================================

Under the hood:  (What is done)
At end of /etc/hosts
127.0.1.2 domain1.com www.domain1.com
127.0.1.3 domain2.com www.domain2.com

------------------------------------

Commands to run:
apache2ctl stop/start/restart
service apache2 stop/start/restart
a2enmod
a2dismod
a2ensite
a2dissite
a2enconf
a2disconf

------------------------------------

After apt-get install apache2

Set a default ServerName
echo "ServerName localhost" >> /etc/apache2/conf-available/fqdn.conf
a2enconf fqdn

Create directories:
/var/www/www.domain1.com
/var/www/www.domain2.com

Put in index.html in respective directories:
<HTML>This is www.domain1.com<HTML>
<HTML>This is www.domain2.com<HTML>

------------------------------------

Pre-configure SSL for each sites:

a2enmod ssl
mkdir /etc/apache2/ssl

sudo openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout  \
/etc/apache2/ssl/www.domain1.com.apache.key -out /etc/apache2/ssl/www.domain1.com.apache.crt

sudo openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout  \
/etc/apache2/ssl/www.domain2.com.apache.key -out /etc/apache2/ssl/www.domain2.com.apache.crt

------------------------------------
 
Set up web config for each site:

Set up website config file  (including redirecting domain1.com to www.domain1.com)

/etc/apache2/sites-available/www.domain1.com.conf

<VirtualHost *:80>
  DocumentRoot /var/www/www.domain1.com
  ServerName www.domain1.com
  ErrorLog ${APACHE_LOG_DIR}/www.domain1.com-error_log
  CustomLog ${APACHE_LOG_DIR}/www.domain1.com-access_log common
</VirtualHost>

<VirtualHost *:80>
  ServerAlias domain1.com
  RedirectMatch permanent ^/(.*) http://www.domain1.com/$1
</VirtualHost>

<IfModule mod_ssl.c>
 <VirtualHost *:443>
  ServerName www.domain1.com
  DocumentRoot /var/www/www.domain1.com

  # Enable SSL for this virtual host.
  SSLEngine on
  SSLCertificateFile /etc/apache2/ssl/www.domain1.com.apache.crt
  SSLCertificateKeyFile /etc/apache2/ssl/www.domain1.com.apache.key
 </VirtualHost>
</IfModule>

<IfModule mod_ssl.c>
 <VirtualHost *:443>
  ServerAlias domain1.com
  RedirectMatch permanent ^/(.*) https://www.domain1.com/$1
 </VirtualHost>
</IfModule>

a2ensite www.domain1.com
a2ensite www.domain2.com

service apache2 restart

