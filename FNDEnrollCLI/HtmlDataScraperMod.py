#!/usr/bin/env python
#-*-coding:utf-8-*-
'''

'''

import codecs
#import datetime
#from datetime import time #, timedelta
import sys

import __init__
import local_settings as ls

#from DisciplineMod import Discipline

from BeautifulSoup import BeautifulSoup
   

class TextDataScraper(object):
  '''
  OBS: this class is not yet functional.  Some work has to be put into it.
  '''
  
  def __init__(self, htmlfile_abspath=None):
    self.htmlfile_abspath = htmlfile_abspath
    if self.htmlfile_abspath == None:
      self.htmlfile_abspath = ls.get_disciplinas_grade_default_filename_abspath()
    self.disciplines = []
    
  def read_data(self):

    # or if your're using BeautifulSoup4:
    # from bs4 import BeautifulSoup

    html_infile = codecs.open(self.htmlfile_abspath,'r', encoding='utf-8') # 'windows-1252')
    #html_infile = open(self.htmlfile_abspath,'r')
    html_text = html_infile.read()
    bsoup = BeautifulSoup(html_text)
    table = bsoup('table')[0]
    rows = table.findAll('tr')
    for row in rows:
      tds = row('td')
      for td in tds:
        print td
        print td.string,

    '''
    for row in bsoup('table')[0].tbody('tr'): # 'table', {'class' : 'spad'}
      tds = row('td')
      for td in tds:
        print td.string,
      print'''
    
    
import unittest
class TestCase1(unittest.TestCase):

  def setUp(self):
    pass

  def test1_(self):
    pass

def unittests():
  unittest.main()


def process():
  scraper = TextDataScraper()
  scraper.read_data()

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
