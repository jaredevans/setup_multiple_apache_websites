#!/usr/bin/python

import sys 
import os 
import string 
import commands 
import shutil

# Replace a string inside a file
def inplace_change(filename, old_string, new_string):
  s=open(filename).read()
  if old_string in s:
    s=s.replace(old_string, new_string)
    f=open(filename, 'w')
    f.write(s)
    f.flush()
    f.close()

# Location of system hosts file. First is for debugging, second for actual location
etchosts = 'output/hosts'
etchosts = '/etc/hosts'

# Location of home directories for websites. First is for debugging, second for actual location
html_dir_default = "output/www/"
html_dir_default = "/var/www/"

# Location of Apache config directory. First is for debugging, second for actual location
apache_sites_available = "output/"
apache_sites_available = "/etc/apache2/sites-available/"

# Location of Apache ssl directory. First is for debugging, second for actual location
apache_ssl = "output/ssl/"
apache_ssl = "/etc/apache2/ssl/"

# The openssl command to auto-generate a SSL certificate
openssl_cmd = '/usr/bin/openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout %swww.PLACEHOLDER.key -out %swww.PLACEHOLDER.crt -subj "/C=US/ST=FL/L=Tampa/O=Local Security/OU=WebDev/CN=PLACEHOLDER" ' % (apache_ssl,apache_ssl) 


try:

    # This script needs to run with sudo privs
    user = os.getenv("SUDO_USER")
    if user is None:
      print "This program need 'sudo'"
      sys.exit(1)

    # Ask where to put the directories for the websites. defaults to /var/www
    html_dir = raw_input("Enter the top-level directory for installation of multiple sites (defaults to " + html_dir_default + "):\n")

    if not html_dir:
 	html_dir = html_dir_default

    # Show what is already at the web home directory to assist user in making good decisions on how to proceed
    if os.path.isdir(html_dir):
      commandString = "ls " + html_dir 
      commandOutput = commands.getoutput(commandString)
      findResults = string.split(commandOutput, "\n")

      print commandString
      print "======= has these files or sub-directories ======"
      for line in findResults:
        print line

      print "========================================"
    else:
      print "This home directory doesn't exist on the system...Exiting now."
      sys.exit(1) 

    # Ask for all the domains to be created as a website.
    domains_input = []
    print "Now enter the domains without the 'www.', e.g. domain1.com , not www.domain1.com "
    entry = raw_input("one per line. Enter a blank line to quit: \n")

    while entry:
      domains_input.append(entry)
      entry = raw_input("")

    if not domains_input:
      print "There are no domains to process."
      sys.exit(0)

    # Show the user the Action Plans of what will happen and get a confirmation that all is good to proceed.
    for domain in domains_input:
      print "Action plan: set up http://%s redirect to --> http://www.%s and https://www.%s" % (domain, domain, domain)

    # Get confirmation from the user before proceeding
    print "\nWebsites installed in: %s and install new site conf templates in %s ." % (html_dir,apache_sites_available)
    confirmed = raw_input('Please confirm these actions [y/N]: ').lower()
    
    if confirmed == "y":
      print "Action plans confirmed. Proceeding now...\n"
    else:
      print "User does not want to proceed. Installation terminated.\n"
      sys.exit(0)
    
    # Create the Apache SSL directory to store the websites' SSL certificates in.
    if not os.path.exists(apache_ssl):
      os.mkdir(apache_ssl)
    
    # These steps will be taken for each domain/website:
    # 1) Create the Apache conf file 
    # 2) Create the SSL private/public keys
    # 4) Create the website home directory and the barebones index.html

    for domain in domains_input:
      print "\n\n======================\nInstalling Apache conf file for %s " % domain
      domain_conf_file = apache_sites_available + "www." + domain + ".conf" 
      shutil.copy("template_apache_conf", domain_conf_file)
      inplace_change(domain_conf_file,"PLACEHOLDER",domain)
      print "Creating and installing private/public key for %s " % domain
      domain_openssl_cmd = openssl_cmd
      domain_openssl_cmd = domain_openssl_cmd.replace("PLACEHOLDER",domain)
      os_result = os.system(domain_openssl_cmd)
      if os_result == 0:
         print "\nSUCCESS creating the public/private keys for %s .\n" % domain
      domain_html_dir = html_dir + "www." + domain + "/"
      print "Creating directory %s , if it doesn't exist" % domain_html_dir
      if not os.path.exists(domain_html_dir):
         os.mkdir(domain_html_dir)
      domain_index_file = domain_html_dir + "index.html" 
      print "Creating file %s" % domain_index_file
      shutil.copy("template_index_html", domain_index_file)
      inplace_change(domain_index_file,"PLACEHOLDER",domain)
      
    #Enable the Apache SSL module
    print "\n==================\nEnabling Apache SSL module."
    os_result = os.system("sudo a2enmod ssl")
    print "==================\n"

    # For each website, enable it
    for domain in domains_input:
      print "Enabling www.%s" % domain
      os_result = os.system("sudo a2ensite www." + domain)

    # Restart Apache service to bring into effect all the new changes
    print "\n==================\nRestarting Apache."
    os_result = os.system("service apache2 restart")
 
    # Add the domains to system's hosts file so that can access them locally
    # But, first check the hosts file to make sure the domain isn't already there.
    print "Adding domains to your hosts file at: %s " % etchosts
    with open(etchosts, "a") as hostsfile:
      hostsfile.write("\n")
      for domain in domains_input:
        domain_line = "127.0.1.1     " + domain + "  www." + domain + "\n" 
        if domain in open(etchosts).read():
	  print "%s was found in the hosts file, skipping..." % domain
        else:
	  hostsfile.write(domain_line)
      
except:
    print "There was a problem - check the message above"

