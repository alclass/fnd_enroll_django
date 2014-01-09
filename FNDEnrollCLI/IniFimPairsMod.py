#!/usr/bin/env python
#-*-coding:utf-8-*-
'''

'''
#import codecs
import sys
from IniFimTupleMod import IniFimTuple
    
class IniFimPairs(list):
  
  def __init__(self, int_freq_size):
    '''
      Just to call superclass list __init__()
    '''
    super(IniFimPairs, self).__init__()
    self.last_index = int_freq_size - 1
    

  def append(self, pair):
    pair = self.validate_pair(pair)
    if len(pair) == 0:
      return
    # print 'adding pair', pair, 'type = ', type(pair)
    super(IniFimPairs, self).append(pair)

  def __add__(self, pairs):
    for pair in pairs:
      self.append(pair)

  def addlist(self, pairs):
    self.__add__(pairs)

  def validate_pair(self, pair):
    if type(pair) == tuple:
      pair = IniFimTuple(pair)
    if type(pair) != IniFimTuple:
      raise TypeError, 'type(pair) != IniFimTuple'
    if len(pair) == 0:
      return pair
    if len(pair) != 2:
      raise ValueError, 'len(pair) != 2 and neither empty'
    ini, fim = pair
    if ini < 0 and fim > self.last_index:
      raise IndexError, 'pair elements (%d, %d) out of range, which is (0, %d)' %(ini, fim, self.last_index)
    return pair

  def remove_range_recursive(self, removal_range, index=0):
    if index > len(self) - 1 or len(removal_range) == 0:
      return # finishes recursion
    result_list = self[index].difference(removal_range)
    # updates removal_range in case it has been "consumed" 
    removal_range_list = removal_range.difference(self[index])
    # removal_range_list can either be a 1-element or a 2-element list
    if len(removal_range_list) == 2:
      removal_range = removal_range_list[1] # pick up its right most range, so it's going index upwards
    elif len(removal_range_list) == 1:
      removal_range = removal_range_list[0]

    if len(result_list) == 1:
      inifimtuple = result_list[0]
      if len(inifimtuple) == 2:
        self[index] = inifimtuple
        index += 1 # for recursion
      else: # ie: if len(inifimtuple) == 0:
        del self[index]
        # do not add 1 to index in this case
      return self.remove_range_recursive(removal_range, index)
    # else: ie, if len(result_list) == 2:
    elif len(result_list) == 2:
      self[index] = result_list[0]
      self.insert(index+1, result_list[1])
      return # remove_range_recursive was consumed, recursion ends here

    if len(removal_range) == 0:
      return

    raise ValueError, 'len(result_list) should be either 1 or 2; it is %s' %(str(result_list))
  
  def remove_range(self, removal_range, index=0):
    if type(removal_range) == tuple:
      removal_range = IniFimTuple(removal_range)
    if type(removal_range) != IniFimTuple:
      raise TypeError, 'type(removal_range) != IniFimTuple'
    return self.remove_range_recursive(removal_range, index)
        
      
import unittest
class TestCaseIniFimPairs(unittest.TestCase):

  def setUp(self):
    pass

  def test1_types(self):
    ini_fim_pairs = IniFimPairs(17)
    pair_list = [(0, 10), (13, 16)]
    ini_fim_pairs.addlist(pair_list)
    self.assertIsInstance(ini_fim_pairs, IniFimPairs)
    for ini_fim_pair in ini_fim_pairs:
      self.assertIsInstance(ini_fim_pair, IniFimTuple)

  def test2a_removerange(self):
    '''
    '''
    ini_fim_pairs = IniFimPairs(17)
    pair_list = [(0, 10), (13, 16)]
    ini_fim_pairs.addlist(pair_list)
    ini_fim_pairs.remove_range((4, 8))
    should_now_be_pair_list = [(0, 3), (9, 10), (13, 16)]
    should_now_be_pairs =  IniFimPairs(17)
    should_now_be_pairs.addlist(should_now_be_pair_list)
    self.assertEqual(should_now_be_pair_list, ini_fim_pairs)

  def test2b_removerange(self):
    ini_fim_pairs = IniFimPairs(17)
    pair_list = [(0, 10), (13, 16)]
    ini_fim_pairs.addlist(pair_list)
    ini_fim_pairs.remove_range((4, 8))
    ini_fim_pairs.remove_range((7, 14))
    should_now_be_pair_list = [(0, 3), (15, 16)]
    should_now_be_pairs =  IniFimPairs(17)
    should_now_be_pairs.addlist(should_now_be_pair_list)
    self.assertEqual(should_now_be_pair_list, ini_fim_pairs)


def unittests():
  unittest.main()


def quick_check():
  print 'Running quick_check() to check the tuple-wrapper type for pairs added to an IniFimPairs object.'
  ini_fim_pairs = IniFimPairs(17)
  pair_list = [(0, 10), (13, 16)]
  ini_fim_pairs.addlist(pair_list)
  ini_fim_pairs.remove_range((4, 8))
  print 'After ini_fim_pairs.remove_range((4, 8)) : ini_fim_pairs =', ini_fim_pairs
  ini_fim_pairs.remove_range((7, 14))
  print 'ini_fim_pairs.remove_range((7, 14))', ini_fim_pairs
  should_now_be_pair_list = [(0, 3), (15, 16)]
  should_now_be_pairs =  IniFimPairs(17)
  should_now_be_pairs.addlist(should_now_be_pair_list)
  print 'should_now_be_pairs', should_now_be_pairs
  


def process():
  '''
  '''
  quick_check()

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
