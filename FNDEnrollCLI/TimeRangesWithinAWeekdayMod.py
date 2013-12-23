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
  
  Example:
  Suppose we have this time range list:
    [(M1,M2), (M3,M4), (T1,T3)] 
  
  The example list above can be contiguealized, so to say, so that it reduces to:
    [(M1,M4), (T1,T3)] 

  Notice that the two ranges (M1,M2), (M3,M4) fused into only one range, ie, (M1,M4)
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

  def test1_equal_tables(self):
    pass

