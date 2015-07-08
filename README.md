<h1>Purpose:</h1>

<p>Quickly create multiple websites (http and https) after a standard Apache installation to get rolling right away!</p>

<h1>Target audience:</h1>

<p>Web developers or systems administrators who want to quickly set up multiple websites on a freshly installed Apache web server for development or testing purposes.</p>

<h1>Under the hood:</h1>

<p>End results: Quickly set up multiple websites as&nbsp;Named Virtual Hosts.</p>

<p>This script will do the following:</p>

<ul>
	<li>Ask where to place the websites&#39; home directories (defaults to /var/www/)</li>
	<li>Ask for all the domains you want to be created at once.
	<ul>
		<li>Use domain names without using &#39;www&#39;: domain1.com ,&nbsp;not www.domain1.com<br />
		&nbsp;</li>
	</ul>
	</li>
	<li>Create the Apache site conf file for each website (/etc/apache2/sites-available)
	<ul>
		<li>domain1.com will be permanently redirected to www.domain1.com</li>
	</ul>
	</li>
	<li>Auto&nbsp;create self-signed SSL keys for each website (/etc/apache2/ssl)</li>
	<li>Create web home directories with barebones index.html<br />
	&nbsp;</li>
	<li>Auto enables Apache SSL module</li>
	<li>Auto enables the websites<br />
	&nbsp;</li>
	<li>Adds the domains to your /etc/hosts and couple them to 127.0.1.1 (in the localhost range 127.0.0.0/8).</li>
</ul>
