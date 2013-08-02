#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Tests with Queries
'''
#import codecs
import os

#import __init__
import local_settings as ls
from TextDataScraperMod import TextDataScraper 
    
def find_by_weekday(data_obj):
  for weekday in xrange(7):
    disciplines = data_obj.find_by_weekday(weekday)
    if disciplines == []:
      continue 
    print 'weekday = ', weekday
    for discipline in disciplines:
      print discipline._id, discipline.name 
    
def process():
  txtfilename = 'disciplines_1.txt'
  txtfile_abspath = os.path.join(ls.get_app_data_dir_abspath(), txtfilename)
  data_obj = TextDataScraper(txtfile_abspath)
  data_obj.read_data()
  #data_obj.list_disciplines()
  find_by_weekday(data_obj)
  
if __name__ == '__main__':
  process()
