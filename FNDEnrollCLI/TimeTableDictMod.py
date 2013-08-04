#!/usr/bin/env python
#-*-coding:utf-8-*-
'''


'''

import codecs, copy
#import datetime
from datetime import time # date #, timedelta
import os

import __init__
#import local_settings as ls
import timeutils


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
      #print 'time_range_list', time_range_list 
    else:
      time_range_list = []
      time_range_list.append(time_range)
      time_range_list = dict.__setitem__(self, weekdaykey, time_range_list)
      #self[weekdaykey] = time_range_list 
      #print 'time_range_list', time_range_list 
    
  #def get_time_ranges_by_weekday(self, weekday):
    #return self[weekday]
    
  def list_all_times_by_weekdaystr_and_time_labels(self):
    weekdays = self.keys()
    weekdays.sort()
    for weekday in weekdays:
      time_ranges = self.get_time_ranges_by_weekday(weekday)
      time_labels = timeutils.get_time_labels_from_time_ranges(time_ranges)
      print timeutils.dict_pt_3_letter_weekday[weekday], time_labels

  def __eq__(self, p_timetable_to_compare):
    '''
    
    When the hardcopy of p_timetable_to_compare is done into timetable_to_compare
    timetable_to_compare becomes a dict instead of a TimeTableDict
    
    The hardcopy is necessary because each equal item is removed from timetable_to_compare,
      avoiding any removals from the original object
    
    The type change mentioned above is not a problem,
      because p_timetable_to_compare is type-checked right at the beginning for being TimeTableDict
      If it's not, False will be returned right away  
     
    '''
    if type(p_timetable_to_compare) != TimeTableDict:
      return False
    timetable_to_compare = TimeTableDict.copy(p_timetable_to_compare)
    item_tuple_list_to_compare = timetable_to_compare.items()
    if len(item_tuple_list_to_compare) != len(self): #len(item_tuple_list):
      return False
    item_tuple_list = self.items()
    # if the two are equal, copy item_tuple_list_to_compare will be consumed (ie, element-removed) entirely
    for item in item_tuple_list:
      if item in item_tuple_list_to_compare:
        item_tuple_list_to_compare.remove(item)
    # if item_tuple_list_to_compare's size is not 0, the two are not equal
    if len(item_tuple_list_to_compare) > 0:
      return False
    return True

  def equal_considering_only_labels(self):
    '''
    Two TimeTableDict's are equal if their dict.items() are all the same
    However, when time ranges are converted to time labels, two TimeTableDict's may have the same labels and yet be different
    
    Yet to implement ! 
    '''
    pass
  
  def __str__(self):
    outstr = '' #'Tempos:\n=======\n'
    weekdays = self.keys()
    weekdays.sort()
    for weekday in weekdays:
      time_ranges = self[weekday] #.get_time_ranges_by_weekday(weekday)
      #outstr += '\n%s :: %s' %(timeutils.dict_pt_3_letter_weekday[weekday], str(time_ranges))
      time_labels = timeutils.get_time_labels_from_time_ranges(time_ranges)
      outstr += '%s :: %s\n' %(timeutils.dict_pt_3_letter_weekday[weekday], time_labels)
    return outstr
  
def create_table1():
  table = TimeTableDict()
  time_start = time(hour=7,minute=30)
  time_finish = time(hour=9,minute=10)
  table[0] = (time_start, time_finish)
  time_start = time(hour=18,minute=30)
  time_finish = time(hour=19,minute=20)
  table[2] = (time_start, time_finish)
  return table
      
def create_table2():
  table = TimeTableDict()
  time_start = time(hour=7,minute=30)
  time_finish = time(hour=9,minute=10)
  table[0] = (time_start, time_finish)
  time_start = time(hour=18,minute=30)
  time_finish = time(hour=19,minute=20)
  table[2] = (time_start, time_finish)
  return table
    
def test1():
  table1 = create_table1()    
  print table1    
  table2 = create_table2()
  print table2
  
  print 'Test 1 :: Comparing of equility:  table1 == table2' 
  print 'Result =', table1 == table2     
    
  time_start = time(hour=18,minute=0)
  time_finish = time(hour=19,minute=40)
  table2[5] = (time_start, time_finish)
  
  print 'Test 1 :: Comparing of equility:  table1 == table2' 
  print 'Result =', table1 == table2     


def process():
  test1()  
        
if __name__ == '__main__':
  process()
