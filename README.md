<h1>Purpose:</h1>
<p>Quickly create multiple websites (http and https) after a standard Apache installation to get rolling right away!</p>
<h1>Target audience:</h1>
<p>Web developers or systems administrators who want to quickly set up multiple websites on a freshly installed Apache web server for development or testing purposes.</p>
<h1>Under the hood:</h1>
<p><span style="line-height: 20.7999992370605px;">Developed and tested on a vanilla Ubuntu system.</span></p>
<p>End results: Quickly set up multiple websites as&nbsp;Named Virtual Hosts.</p>
<p>This script needs you to supply&nbsp;two parameters:</p>
<ul>
<li>The webserver home directory where to place the websites (defaults to /var/www/)</li>
<li>The domains you want to be created.
<ul>
<li>Important note: use domain names without including&nbsp;'www'. i.e. domain1.com ,&nbsp;not www.domain1.com</li>
</ul>
</li>
</ul>
<p>This script will do the following:&nbsp;</p>
<ul>
<li>Create the Apache site conf file for each website (/etc/apache2/sites-available)
<ul>
<li>domain1.com will be permanently redirected to www.domain1.com</li>
</ul>
</li>
<li>Auto&nbsp;create self-signed SSL keys for each website (/etc/apache2/ssl)</li>
<li>Create web home directories with barebones index.html<br /> &nbsp;</li>
<li>Auto enables Apache SSL module</li>
<li>Auto enables both HTTP and HTTPS&nbsp;websites<br /> &nbsp;</li>
<li>Add the domains to your /etc/hosts and couple them to 127.0.1.1 (in the localhost range 127.0.0.0/8).</li>
</ul>
<p><ins>How to run</ins></p>
<pre>chmod u+x setup_domains.py
sudo ./setup_domains.py -h  (view the help screen for the switches you need to set)<br />   -w WEBDIR, --webdir WEBDIR Location of webserver home directory, defaults to /var/www<br />   -d DOMAINS [DOMAINS ...], --domains DOMAINS [DOMAINS ...]<br />       List of domains, defaults to domain1.com domain2.com.<br />       Don't include the 'www.' prefix since that will be taken care of.<br /><br />sudo ./setup_domains.py -w /var/www -d domain1.com domain2.com<br /><br />--or--<br /><br />Look at example.py for how to incorporate the function into your own script</pre>
