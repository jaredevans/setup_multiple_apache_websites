import stat, sys, os, string, commands

try:
    html_dir = raw_input("Enter the top-level directory for installation of multiple sites:\n")
    commandString = "ls " + html_dir 
    commandOutput = commands.getoutput(commandString)
    findResults = string.split(commandOutput, "\n")

    print "Lines:"
    print commandOutput
    print "================================"
    for line in findResults:
	print line
except:
    print "There was a problem - check the message above"

