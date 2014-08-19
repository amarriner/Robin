#!/usr/bin/env python

"""Script to build Holy ______ Batman! tweets"""

from bs4 import BeautifulSoup

import keys
import random
import re
import requests
import string
import sys
import twitter


# Scraping www.idiomconnection.com for idioms
IDIOM_BASE = 'http://www.idiomconnection.com'


def format_idiom(idiom):
   """Returns idiom lowercase without parentheticals, punctuation and removing preceeding 'A ...' """

   # Sometimes the idiom is one thing OR another, pick one
   if len(idiom.lower().split(' <i>or</i> ')):
      idiom = random.choice(idiom.lower().split(' <i>or</i> '))

   # Some idioms have two words separated by a slash, we should pick one of those words to use
   s = ''
   for w in idiom.split(' '):
      if len(w.split('/')) > 1:
         w = random.choice(w.split('/'))

      if len(s):
         s += ' '

      s += w

   # Replace (someone's) or one's with your
   s = s.replace('one\'s', 'your')
   s = s.replace('(someone`s)', 'your')

   # Strip leading 'A ' if it exists
   if s[:2].upper() == 'A ':
      s = s[2:]

   # Remove anything inside parentheses
   parenthetical = re.compile(r'\(.*?\)')
   s = re.sub(parenthetical, '', s)

   # Sometimes the previous regex will leave two spaces in a row and since I suck too much with regexes to do
   # this all in one step, I'll strip them out here
   s = s.replace('  ', ' ')

   # Remove most punctuation
   punctuation = re.compile(r'[^A-Za-z0-9 -\']')
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

   # Get the randomly picked page with a list of idioims
   request = requests.get(link.get('href'))
   soup = BeautifulSoup(request.content)

   # Take one idiom from that page, and format it
   idiom = format_idiom(random.choice(soup.find_all('b')).contents[0])
   tweet = 'Holy ' + idiom + ', Batman!'
   print tweet


   # Connect to Twitter
   api = twitter.Api(keys.consumer_key, keys.consumer_secret, keys.access_token, keys.access_token_secret)

   # Tweet
   status = api.PostUpdate(tweet)


if __name__ == '__main__':
   sys.exit(main())
