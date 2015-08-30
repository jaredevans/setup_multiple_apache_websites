#!/usr/bin/python

from setup_domains import setup_domains

if __name__ == "__main__":

    setup_domains("/var/www", ["test1.com", "test2.com"])
