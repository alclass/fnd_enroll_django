#!/usr/bin/env python
#-*-coding:utf-8-*-
'''


'''

from datetime import time # date #, timedelta
import os

import __init__
#import local_settings as ls
import timeutils
from timeutils import K

class TimeRangesWithinAWeekday(list):
  '''
  This class (TimeRangesWithinAWeekday) extends from list
  Its main purpose is to post-process the list of time ranges so that if ranges overlap, they become unified
  The class also breaks ranges apart if some part of it is removed
  
  The 2 examples below illustrate the 2 cases, ie:
    1) the summation with possible contiguealization
    2) the extraction with possible uncontiguealization
  
  (The 2) Examples:

  1) Contiguealization

  Suppose we have this time range list:
    [(M1,M2), (M3,M4), (T1,T3)] 
  
  The example list above can be contiguealized, so to say, so that it reduces to:
    [(M1,M4), (T1,T3)] 

  Notice that the two ranges (M1,M2), (M3,M4) fused into only one range, ie, (M1,M4)

  2) Uncontiguealization

  Suppose we have this time range list:
    [(M1,T1)] 
  
  Suppose further that we remove time range (M3,T4) from it
  Because of this removal, the list gets uncontiguealized, ie, the resulting list becomes: 
    [(M1,M2), (M5,T1)] 

  Notice that the one range (M1,T1) subtracted of (M3,M4) get broken into two ranges, ie, (M1,M2) and (M5,T1)

  '''
  
  def __init__(self, *args):
    '''
      Just to call superclass list __init__()
    '''
    super(TimeRangesWithinAWeekday, self).__init__(args)
  
  def append(self, time_range):
    '''
      1st) Call superclass list append()
      2nd) Contiguealize the list if that is the case (the resulting list may or may not be contiguous)
    '''
    super(TimeRangesWithinAWeekday, self).append(time_range)
    self.contiguealize_it()

  def __add__(self, time_range_list):
    '''
      1st) Call superclass list __add__()  (which is equivalent of the "+" operation in-between lists)
      2nd) Contiguealize the list if that is the case (the resulting list may or may not be contiguous)
    '''
    super(TimeRangesWithinAWeekday, self).__add__(time_range_list)
    self.contiguealize_it()
    
  def contiguealize_it(self):
    pass

  def remove_range(self, time_range):
    pass

  def remove(self, time_range):
    '''
    This method is overridden here from parent "list"
    '''
    return self.remove_range(time_range)


def process():
  pass  
        
if __name__ == '__main__':
  process()

import unittest

class TestCase(unittest.TestCase):

  def setUp(self):
    self.table1 = None
    self.table2 = None
    self.make_table1()

  def make_table1(self):
    pass

  def test1_verify_contiguealization(self):
    weekday_time_ranges = TimeRangesWithinAWeekday()
    weekday_time_ranges.append(K.M1, K.M2)    
    weekday_time_ranges.append(K.M3, K.M4)
    weekday_time_ranges_already_given_contiguous = TimeRangesWithinAWeekday((K.M3, K.M4))
    self.assertEqual(weekday_time_ranges, weekday_time_ranges_already_given_contiguous)

  def test1_verify_removal_and_breaking_of_contiguealization(self):
    weekday_time_ranges = TimeRangesWithinAWeekday()
    weekday_time_ranges.append((K.M1, K.T1))    
    weekday_time_ranges.remove_range((K.M3, K.M4))
    weekday_time_ranges_already_given_uncontiguous = TimeRangesWithinAWeekday()
    weekday_time_ranges_already_given_uncontiguous.append((K.M1, K.M2))
    weekday_time_ranges_already_given_uncontiguous.append((K.M5, K.T1))
    self.assertEqual(weekday_time_ranges, weekday_time_ranges_already_given_uncontiguous)
