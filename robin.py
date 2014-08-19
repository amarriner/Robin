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

   if s[:2].upper() == 'A ':
      s = s[2:]

   parenthetical = re.compile(r'\(.*?\)')
   s = re.sub(parenthetical, '', s)

   punctuation = re.compile(r'[^A-Za-z0-9 -]')
   s = re.sub(punctuation, '', s)

   return string.strip(s).lower()


def main():
   """Initial entry point"""

   request = requests.get(IDIOM_BASE)
   soup = BeautifulSoup(request.content)

   # There are two UL tags that contain links to pages with idioms on them
   # Pick one at random and then a link at random within that UL to find the URL to scrape for an idom
   link = random.choice(random.choice(soup.find_all('ul', limit=2)).find_all('a'))
   print link.get('href')

   request = requests.get(link.get('href'))
   soup = BeautifulSoup(request.content)

   idiom = random.choice(soup.find_all('b')).contents[0]
   print idiom
   print format_idiom(idiom)


if __name__ == '__main__':
   sys.exit(main())
