After a standard Apache installation, run this script to quickly set up multiple websites to be hosted by the server.

This script will:

1) Ask for the home directory where all websites directories will go under. (default '/var/www')

2) Set up simple templated website for each website www.domain.com with permanent redirect from domain.com (i.e. http://jared.com redirected to http://www.jared.com)

3) Use and enable a minimal Named VirtualHost configuration for each website inside Apache config directory (default '/etc/apache2/sites-available')

4) Each website has their own access.log and error.log

5) Create and install self-signed SSL key for each website and enable HTTPS.

