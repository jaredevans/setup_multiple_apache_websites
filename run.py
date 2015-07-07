#!/usr/bin/python

import stat, sys, os, string, commands

try:

#    user = os.getenv("SUDO_USER")
#    if user is None:
#      print "This program need 'sudo'"
#      sys.exit(1)

    html_dir = raw_input("Enter the top-level directory for installation of multiple sites (defaults to /var/www):\n")

    if not html_dir:
 	html_dir = '/var/www'

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

    if not domains_input:
      print "There are no domains to process."
      sys.exit(0)

    for domain in domains_input:
      print "Action plan: set up http://%s redirect to --> http://www.%s and https://www.%s" % (domain, domain, domain)

    print "\nWebsites installed in: %s and install new site conf templates in /etc/apache2/sites-available ." % (html_dir)
    confirmed = raw_input('Please confirm these actions [y/N]: ').lower()
    
    if confirmed == "y":
      print "Action plans confirmed. Proceeding now...\n"
    else:
      print "User does not want to proceed. Installation terminated.\n"
      sys.exit(0)

except:
    print "There was a problem - check the message above"

