#!/usr/bin/env python
#-*-coding:utf-8-*-
'''


'''

from datetime import time # date #, timedelta
import os, sys

import __init__
#import local_settings as ls
import timeutils
from timeutils import K
from IniFimPairsMod import IniFimPairs


class TimeRangesWithinAWeekday(list):
  '''
  This class (TimeRangesWithinAWeekday) extends from list
  Its main purpose is to post-process the list of time ranges so that if ranges overlap, they become unified
  The class also breaks ranges apart if some inner part of it is removed
  
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

  Notice that the one range (M1,T1) subtracted of (M3,M4) got broken into two ranges, ie, (M1,M2) and (M5,T1)
  
  In a nutshell:
    [(M1,M2), (M3,M4), (T1,T3)] =reduces_to=> [(M1,M4), (T1,T3)]
    [(M1,T1)] - [(M3,T4)] =reduces_to=> [(M1,M2), (M5,T1)]
  

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
    
  def contiguealize_it(self, index=0):
    if index >= len(self) - 1:
      return
    front_time_range   = self[index]
    next_time_range    = self[index+1]
    front_ending_at    = front_time_range[1]
    next_beginning_at  = next_time_range[0]
    less_equal_greater = timeutils.compare_2_time_labels_less_equal_greater(front_ending_at, next_beginning_at)
    if less_equal_greater == timeutils.LABEL_SMALLER:
      return self.contiguealize_it(index+1)
    # Swap
    front_beginning_at  = front_time_range[0]
    next_ending_at      = next_time_range[1]
    self[index+1] = (front_beginning_at, next_ending_at)
    del self[index]
    return self.contiguealize_it(index+1)
      
    pass

  def remove_range(self, time_range_to_remove, index=0):
    
    ini_fim_pairs = IniFimPairs(len(timeutils.labels_contiguity))
    for time_range_labels in self:
      ini_fim_int_indices = timeutils.convert_time_range_labels_to_indices(time_range_labels)
      ini_fim_pairs.append(ini_fim_int_indices)
    time_range_to_remove_indices = timeutils.convert_time_range_labels_to_indices(time_range_to_remove)
    ini_fim_pairs.remove_range(time_range_to_remove_indices)
    
    super(TimeRangesWithinAWeekday, self).__init__()
    for ini_fim_tuple in ini_fim_pairs:
      time_range_by_labels = timeutils.convert_indices_to_time_range_labels(ini_fim_tuple)
      self.append(time_range_by_labels)

  def remove(self, time_range):
    '''
    This method is overridden here from parent "list"
    '''
    super(TimeRangesWithinAWeekday, self).remove(time_range)
    return self.contiguealize_it()


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
    weekday_time_ranges.append((K.M1, K.M2))    
    weekday_time_ranges.append((K.M3, K.M4))
    weekday_time_ranges_already_given_contiguous = TimeRangesWithinAWeekday((K.M1, K.M4))
    self.assertEqual(weekday_time_ranges, weekday_time_ranges_already_given_contiguous)

  def test1_verify_removal_and_breaking_of_contiguealization(self):
    weekday_time_ranges = TimeRangesWithinAWeekday()
    weekday_time_ranges.append((K.M1, K.T1))    
    weekday_time_ranges.remove_range((K.M3, K.M4))
    weekday_time_ranges_already_given_uncontiguous = TimeRangesWithinAWeekday()
    weekday_time_ranges_already_given_uncontiguous.append((K.M1, K.M2))
    weekday_time_ranges_already_given_uncontiguous.append((K.M5, K.T1))
    self.assertEqual(weekday_time_ranges, weekday_time_ranges_already_given_uncontiguous)


def unittests():
  unittest.main()

def process():
  '''
  '''
  pass

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
