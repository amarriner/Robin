#!/usr/bin/env python

"""Script to build Holy ______ Batman! tweets"""

from bs4 import BeautifulSoup

import random
import re
import requests
import string
import sys


# Scraping www.idiomconnection.com for idioms
IDIOM_BASE = 'http://www.idiomconnection.com'


def format_idiom(s):
   """Returns idiom lowercase without parentheticals, punctuation and removing preceeding 'A ...' """

   # Strip leading 'A ' if it exists
   if s[:2].upper() == 'A ':
      s = s[2:]

   # Remove anything inside parentheses
   parenthetical = re.compile(r'\(.*?\)')
   s = re.sub(parenthetical, '', s)

   # Remove most punctuation
   punctuation = re.compile(r'[^A-Za-z0-9 -]')
   s = re.sub(punctuation, '', s)


   return string.strip(s).lower()


def main():
   """Initial entry point"""

   # Retrieve main idiom page
   request = requests.get(IDIOM_BASE)
   soup = BeautifulSoup(request.content)

   # There are two UL tags that contain links to pages with idioms on them
   # Pick one at random and then a link at random within that UL to find the URL to scrape for an idom
   link = random.choice(random.choice(soup.find_all('ul', limit=2)).find_all('a'))
   print link.get('href')

   # Get the randomly picked page with a list of idioims
   request = requests.get(link.get('href'))
   soup = BeautifulSoup(request.content)

   # Take one idiom from that page, and format it
   idiom = format_idiom(random.choice(soup.find_all('b')).contents[0])

   print 'Holy ' + idiom + ' Batman!'


if __name__ == '__main__':
   sys.exit(main())
