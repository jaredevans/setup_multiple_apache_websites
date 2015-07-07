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

html_dir_default = "output/"
#html_dir_default = "/var/www/"

apache_sites_available = "output/"
#apache_sites_available = "/etc/apache2/sites-available/"

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
    domains_input.append("rit.com")
    domains_input.append("gallaudet.com")

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


    for domain in domains_input:
      print "Setting up Apache conf file for %s " % domain
      domain_conf_file = apache_sites_available + "www." + domain + ".conf" 
      shutil.copy("template_apache_conf", domain_conf_file)
      inplace_change(domain_conf_file,"PLACEHOLDER",domain)

except:
    print "There was a problem - check the message above"

