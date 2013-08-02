#!/usr/bin/env python
#-*-coding:utf-8-*-
'''


'''

import codecs
#import datetime
from datetime import time # date #, timedelta
import os

import __init__
import local_settings as ls
import timeutils

'''
L1 IUE514
L2  
L3 5866
L4  DIR. EMPRESA RELAÇÕES DE TRABALHO   
L5 Qui
L6  
L7 16:40 às 18:20
L8  IVAN SIMOES GARCIA
'''

class TimeTableDict(dict):
  
  def __init__(self, *args):
    dict.__init__(self, args)
    
  def __setitem__(self, weekdaykey, time_range):
    if not timeutils.is_time_range_a_tuple_of_times(time_range):
      return
    if dict.has_key(self, weekdaykey):
    #if self.has_key(weekdaykey):
      time_range_list = dict.__getitem__(self, weekdaykey)
      time_range_list.append(time_range)
      print 'time_range_list', time_range_list 
    else:
      time_range_list = []
      time_range_list.append(time_range)
      time_range_list = dict.__setitem__(self, weekdaykey, time_range_list)
      #self[weekdaykey] = time_range_list 
      print 'time_range_list', time_range_list 
    
  #def get_time_ranges_by_weekday(self, weekday):
    #return self[weekday]
    
  def list_all_times_by_weekdaystr_and_time_labels(self):
    weekdays = self.keys()
    weekdays.sort()
    for weekday in weekdays:
      time_ranges = self.get_time_ranges_by_weekday(weekday)
      time_labels = timeutils.get_time_labels_from_time_ranges(time_ranges)
      print timeutils.dict_pt_3_letter_weekday[weekday], time_labels

  def __str__(self):
    outstr = 'Tempos:\n=======\n'
    weekdays = self.keys()
    weekdays.sort()
    for weekday in weekdays:
      time_ranges = self[weekday] #.get_time_ranges_by_weekday(weekday)
      outstr += '\n%s :: %s' %(timeutils.dict_pt_3_letter_weekday[weekday], str(time_ranges))
      time_labels = timeutils.get_time_labels_from_time_ranges(time_ranges)
      outstr += '\n%s :: %s' %(timeutils.dict_pt_3_letter_weekday[weekday], time_labels)
    return outstr
  
def test1():
  table = TimeTableDict()
  time_start = time(hour=7,minute=30)
  time_finish = time(hour=9,minute=10)
  table[0] = (time_start, time_finish)
  time_start = time(hour=18,minute=30)
  time_finish = time(hour=19,minute=20)
  table[2] = (time_start, time_finish)
  print table    
    
    
def process():
  test1()  
        
if __name__ == '__main__':
  process()
