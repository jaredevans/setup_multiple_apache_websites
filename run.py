#!/usr/bin/python

import sys, os, string, commands, shutil

def inplace_change(filename, old_string, new_string):
  s=open(filename).read()
  if old_string in s:
    s=s.replace(old_string, new_string)
    f=open(filename, 'w')
    f.write(s)
    f.flush()
    f.close()

etchosts = 'output/hosts'
#etchosts = '/etc/hosts'

html_dir_default = "output/www/"
#html_dir_default = "/var/www/"

apache_sites_available = "output/"
#apache_sites_available = "/etc/apache2/sites-available/"

apache_ssl = "output/ssl/"
#apache_ssl = "/etc/apache2/ssl/"

openssl_cmd = '/usr/bin/openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout %swww.PLACEHOLDER.key -out %swww.PLACEHOLDER.crt -subj "/C=US/ST=FL/L=Tampa/O=Local Security/OU=WebDev/CN=PLACEHOLDER" ' % (apache_ssl,apache_ssl) 


try:

#    user = os.getenv("SUDO_USER")
#    if user is None:
#      print "This program need 'sudo'"
#      sys.exit(1)

    html_dir = raw_input("Enter the top-level directory for installation of multiple sites (defaults to " + html_dir_default + "):\n")

    if not html_dir:
 	html_dir = html_dir_default

    if os.path.isdir(html_dir):
      commandString = "ls " + html_dir 
      commandOutput = commands.getoutput(commandString)
      findResults = string.split(commandOutput, "\n")

      print commandString
      print "======= has these sub-directories ======"
      for line in findResults:
        print line

      print "========================================"
    else:
      print "This home directory doesn't exist on the system...Exiting now."
      sys.exit(1) 

    domains_input = []
    print "Now enter the domains, e.g. domain1.com  , not www.domain1.com "
    entry = raw_input("one per line. Enter a blank line to quit: \n")

    while entry:
      domains_input.append(entry)
      entry = raw_input("")
    domains_input.append("domain1.com")
    domains_input.append("domain2.com")

    if not domains_input:
      print "There are no domains to process."
      sys.exit(0)

    for domain in domains_input:
      print "Action plan: set up http://%s redirect to --> http://www.%s and https://www.%s" % (domain, domain, domain)

    print "\nWebsites installed in: %s and install new site conf templates in %s ." % (html_dir,apache_sites_available)
    confirmed = raw_input('Please confirm these actions [y/N]: ').lower()
    
    if confirmed == "y":
      print "Action plans confirmed. Proceeding now...\n"
    else:
      print "User does not want to proceed. Installation terminated.\n"
#      sys.exit(0)
    
    if not os.path.exists(apache_ssl):
      os.mkdir(apache_ssl)

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
      
   
    print "\n==================\nEnabling Apache SSL module."
    os_result = os.system("sudo a2enmod ssl")
    print "==================\n"
    for domain in domains_input:
      print "Enabling www.%s" % domain
      os_result = os.system("sudo a2ensite www." + domain)

    print "\n==================\nRestarting Apache."
    os_result = os.system("service apache2 restart")
 
    print "Adding domains to your hosts file at: %s " % etchosts
    with open(etchosts, "a") as hostsfile:
      hostsfile.write("\n")
      for domain in domains_input:
        domain_line = "127.0.1.1     " + domain + "  www." + domain + "\n" 
        hostsfile.write(domain_line)

      
except:
    print "There was a problem - check the message above"

