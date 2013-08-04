#!/usr/bin/env python
#-*-coding:utf-8-*-
'''

'''

import codecs
#import datetime
from datetime import time #, timedelta
import os

import __init__
import local_settings as ls
import timeutils

from DisciplineMod import Discipline

from BeautifulSoup import BeautifulSoup
   

class TextDataScraper(object):
  
  def __init__(self, htmlfile_abspath=None):
    self.htmlfile_abspath = htmlfile_abspath
    if self.htmlfile_abspath == None:
      self.htmlfile_abspath = ls.get_disciplinas_grade_default_filename_abspath()
    self.disciplines = []
    
  def read_data(self):

    # or if your're using BeautifulSoup4:
    # from bs4 import BeautifulSoup

    html_infile = codecs.open(self.htmlfile_abspath,'r', encoding='windows-1252')
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
    
    
def process():
  scraper = TextDataScraper()
  scraper.read_data()
        
if __name__ == '__main__':
  process()
