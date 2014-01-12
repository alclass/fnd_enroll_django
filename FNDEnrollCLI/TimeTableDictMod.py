#!/usr/bin/env python
#-*-coding:utf-8-*-
'''


'''

# import codecs, copy, os
#import datetime
from datetime import time # date #, timedelta
import sys

from IniFimTupleMod import IniFimTuple
from IniFimPairsMod import IniFimPairs
import __init__
#import local_settings as ls
import timeutils
from timeutils import K


class TimeTableDict(dict):
  
  @staticmethod
  def weekday_3letter(weekday):
    return timeutils.dict_pt_3_letter_weekday[weekday]

  def __init__(self):
    # To simplify matters, constructor does not accept key:value pairs (__setitem__() does the job)
    super(TimeTableDict, self).__init__()

    
  def __setitem__(self, weekdaykey, ini_fim_tuple):
    if type(ini_fim_tuple) in [tuple, list]:
      ini_fim_tuple = IniFimTuple(ini_fim_tuple)
    if type(ini_fim_tuple) != IniFimTuple:
      raise TypeError, 'type(ini_fim_tuple)=%s != IniFimTuple in class TimeTableDict(dict)' %(str(type(ini_fim_tuple)))
    if self.has_key(weekdaykey):
      ini_fim_pairs = self[weekdaykey]
      ini_fim_pairs.append(ini_fim_tuple)
      #print 'time_range_list', time_range_list 
    else:
      ini_fim_pairs = IniFimPairs(timeutils.get_n_of_times_per_day())
      ini_fim_pairs.append(ini_fim_tuple)
      super(TimeTableDict, self).__setitem__(weekdaykey, ini_fim_pairs)
      #print 'time_range_list', time_range_list 

  def set_weekday_timetable_by_labels(self, weekday, time_label_start, time_label_finish):
    ini_fim_tuple = IniFimTuple.generate_instance_from_labels(time_label_start, time_label_finish)
    self.__setitem__(weekday, ini_fim_tuple)

  def remove_weekday_timetable_by_labels(self, weekday, time_label_start, time_label_finish):
    time_range_labels = time_label_start, time_label_finish
    ini_fim_tuple = IniFimTuple.generate_instance_from_labels(time_range_labels)
    try:
      ini_fim_pairs = self[weekday]
      ini_fim_pairs.remove_range(ini_fim_tuple)
    except IndexError:
      return

  def get_time_labels_for_weekday(self, weekday):
    time_labels_for_weekday = []
    if self.has_key(weekday):
      ini_fim_pairs = self[weekday]
      for ini_fim_tuple in ini_fim_pairs:
        time_labels_for_weekday.append(ini_fim_tuple.as_labels())
    return time_labels_for_weekday

  def get_str_hour_min_time_ranges_for_weekday(self, weekday):
    str_hour_min_time_ranges_for_weekday = []
    if self.has_key(weekday):
      ini_fim_pairs = self[weekday]
      for ini_fim_tuple in ini_fim_pairs:
        str_hour_min_time_ranges_for_weekday.append(ini_fim_tuple.as_str_hour_min_time_range())
    return str_hour_min_time_ranges_for_weekday

  
  def list_all_times_by_weekdaystr_and_time_labels(self):
    weekdays = self.keys()
    weekdays.sort()
    for weekday in weekdays:
      time_labels = self.get_time_labels_for_weekday(weekday)
      print timeutils.dict_pt_3_letter_weekday[weekday], time_labels

  def __eq__(self, p_timetable_to_compare):
    '''
    
    The strategy used here is the following:

    1) A check is done whether p_timetable_to_compare is typed TimeTableDict
       if not, say it's not equal (ie, return False)
    
    2) If sizes mismatch, say it's not equal (ie, return False)

    Ok, up til here, type and sizes are good. We'll check if items are equal, one by one.
    3) Do a hardcopy of p_timetable_to_compare so that items can be consumed
       (otherwise p_timetable_to_compare will be "hurt" outside, ie, reference is side-effected)
       consume all items that self has, it some remain, says it's not equal (ie, return False)  
     
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

  def show_timelabels_in_1_line(self):
    outstr = ''
    weekdays = self.keys()
    weekdays.sort()
    for weekday in weekdays:
      ini_fim_pairs = self[weekday]
      time_labels = ini_fim_pairs.as_labels()
      outstr += ' %s %s, ' %(timeutils.dict_pt_3_letter_weekday[weekday], str(time_labels))
    return outstr

  def __str__(self):
    outstr = '' #'Tempos:\n=======\n'
    weekdays = self.keys()
    weekdays.sort()
    for weekday in weekdays:
      ini_fim_pairs = self[weekday]
      time_labels = ini_fim_pairs.as_hours()
      outstr += '%s :: %s\n' %(timeutils.dict_pt_3_letter_weekday[weekday], str(time_labels))
    return outstr
  
def create_table1():
  table = TimeTableDict()
  #time_start = time(hour=7,minute=30)
  #time_finish = time(hour=9,minute=10)
  ini_fim_tuple = IniFimTuple.generate_instance_from_labels(K.M1, K.M2)
  table[K.MONDAY] = ini_fim_tuple
  #time_start = time(hour=18,minute=30)
  #time_finish = time(hour=19,minute=20)
  ini_fim_tuple = IniFimTuple.generate_instance_from_labels(K.N1, K.N2)
  table[K.WEDNESDAY] = ini_fim_tuple
  return table
      
def create_table2():
  table = TimeTableDict()
  #time_start = time(hour=7,minute=30)
  #time_finish = time(hour=9,minute=10)
  ini_fim_tuple = IniFimTuple.generate_instance_from_labels(K.M1, K.M2)
  table[K.MONDAY] = ini_fim_tuple
  #time_start = time(hour=18,minute=30)
  #time_finish = time(hour=19,minute=20)
  ini_fim_tuple = IniFimTuple.generate_instance_from_labels(K.N1, K.N2)
  table[K.WEDNESDAY] = ini_fim_tuple
  return table
    
def test1():
  table1 = create_table1()    
  print 'Table 1:'
  print table1    
  table2 = create_table2()
  print 'Table 2:'
  print table2
  
  print 'Test 1 :: Comparing of equility:  table1 == table2' 
  print 'Result =', table1 == table2     
    
  #time_start = time(hour=18,minute=0)
  #time_finish = time(hour=19,minute=40)
  ini_fim_tuple = IniFimTuple.generate_instance_from_labels(K.N1, K.N2)
  table2[K.FRIDAY] = ini_fim_tuple
  print 'Table 2 (changed):'
  print table2
  
  print 'Test 1 :: Comparing of equility:  table1 == table2' 
  print 'Result =', table1 == table2
  
  print
  print 'table2.show_timelabels_in_1_line():'
  print table2.show_timelabels_in_1_line()
  
       


import unittest

class TestCase(unittest.TestCase):

  def setUp(self):
    self.table1 = None
    self.table2 = None
    self.make_table1()

  def make_table1(self):
    self.table1 = TimeTableDict()
    self.table1.set_weekday_timetable_by_labels(K.MONDAY, K.M1, K.M2)
    self.table1.set_weekday_timetable_by_labels(K.MONDAY, K.N1, K.N2)
    # self.table1.remove_weekday_timetable_by_labels(K.MONDAY, K.N1, K.N2)

  def test1_equal_tables(self):
    table_copied = self.table1.copy()
    self.assertEqual(self.table1, table_copied)
    time_start_T1  = time(hour=12,minute=0)
    time_finish_T1 = time(hour=12,minute=50)
    table_copied[timeutils.K.MONDAY] = (time_start_T1, time_finish_T1)
    self.assertNotEqual(self.table1, table_copied)


def unittests():
  unittest.main()

def process():
  test1()  
        
if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
