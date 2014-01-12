#!/usr/bin/env python
#-*-coding:utf-8-*-
'''

'''
#import codecs
import sys
from IniFimTupleMod import IniFimTuple
    
class IniFimPairs(list):
  '''
  This class models a list of IniFimTuple's.
  The idea behind this is to model a time table with discrete start and finish times.
  Because these 2 times are discrete, they are operated via integers.
  
  Example:
  Let pair (M1, M2) be the start and finish times of a class lecture.
  Internally, this pair is (0, 1).  For another instance, (M3, M5) would be (2, 4)
  
  Though this class inherits from list, at construction, 
    it needs the total number of times in the table, not an initial list.
  
  For example:
  If time_table (named labels_contiguity) is: 
    ['M1','M2','M3','M4','M5','T1','T2','T3','T4','T5','T6','T7','N1','N2','N3','N4','N5']
  The total number of times in the table is len(time_table), which is, counting above, 17, (or 5+7+5)
  
  
  Appending pairs happens keeping them in ascending order.
  Some operations are available which may not be of use depending on the application one wants.
  For example: method contiguealize_it() may or may not be useful. It unifies times if they are unifiable.
    Example: (M1, M2) may be unified with (M3, M4) resulting in pair (M1, M4)  

  Method remove_range() extracts times from the time table.
  '''
  
  def __init__(self, int_freq_size):
    '''
      Just to call superclass list __init__()
    '''
    super(IniFimPairs, self).__init__()
    self.last_index = int_freq_size - 1
    

  def append(self, p_pair):
    p_pair = self.validate_pair(p_pair)
    if len(p_pair) == 0:
      return
    # print 'adding pair', p_pair, 'type = ', type(p_pair)
    for index, current_pair in enumerate(self):
      if p_pair[0] < current_pair[0]:
        super(IniFimPairs, self).insert(index, p_pair)
        return
    super(IniFimPairs, self).append(p_pair)

  def __add__(self, pairs):
    for pair in pairs:
      self.append(pair)

  def addlist(self, pairs):
    self.__add__(pairs)

  def get_equivalent_tuple_list(self):
    outlist = []
    for pair in self:
      t = tuple(pair)
      outlist.append(t)
    return outlist

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

  def order_pairs_ascendingly(self):
    '''
    This method should never be used, because method append() takes care of inserting a pair in order
    ( This method has not yet been tested !!! )
    '''
    xs = []
    for pair in self:
      x, _ = pair
      xs.append(x, pair.copy())
    super(IniFimPairs, self).__init__() # deleting all pairs
    xs.sort(lambda x : x[0])
    pairs_in_order = zip(*xs)[1]
    super(IniFimPairs, self).__init__(pairs_in_order) # deleting all pairs

  def report_intersections(self):
    intersection_doubles = []
    for index, current_pair in enumerate(self[:-1]):
      next_pair = self[index+1]
      if current_pair[1] >= next_pair[0]:
        print 'current_pair[1] >= next_pair[0], ie, %s intersects %s' %(str(current_pair), str(next_pair))
        intersection_doubles.append((current_pair, next_pair))
    return intersection_doubles

  def as_labels(self):
    times_as_labels = []
    for ini_fim_tuple in self:
      times_as_labels.append(ini_fim_tuple.as_labels())
    return times_as_labels

  def as_hours(self):
    times_as_hours = []
    for ini_fim_tuple in self:
      times_as_hours.append(ini_fim_tuple.as_hours())
    return times_as_hours

  def contiguealize_it(self, index=0):
    '''
    This method presupposes order of pairs in ascendent, if not, an exception will be raised
    '''
    
    if index >= len(self) - 1:
      return

    current_pair = self[index]
    next_pair    = self[index+1]

    if current_pair[0] > next_pair[0]:
      raise ValueError, 'Inconsistent current_pair[0]=%d > next_pair[0]=%d' %(current_pair[0], next_pair[0])

    if current_pair[1] + 1 < next_pair[0]:
      return self.contiguealize_it(index+1)
    
    if current_pair[1] >= next_pair[1]:
      del self[index+1]
      return self.contiguealize_it(index)
      
    new_y = next_pair[1]
    new_current_pair = IniFimTuple((current_pair[0], new_y))
    self[index] = new_current_pair
    del self[index+1]
    return self.contiguealize_it(index)

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

  def test2_insert_order(self):
    ini_fim_pairs = IniFimPairs(100)
    pair_list = [(13, 16), (0, 10)]
    pair_list_in_order = [(0, 10),(13, 16)]
    ini_fim_pairs.addlist(pair_list)
    self.assertEqual(ini_fim_pairs.get_equivalent_tuple_list(), pair_list_in_order)

  def test3_contiguealize(self):
    ini_fim_pairs = IniFimPairs(100)
    pair_list = [(11, 16), (8, 10), (0,3)]
    pair_list_in_order = [(0, 3),(8, 16)]
    ini_fim_pairs.addlist(pair_list)
    ini_fim_pairs.contiguealize_it()
    self.assertEqual(ini_fim_pairs.get_equivalent_tuple_list(), pair_list_in_order)

  def test4_report_intersections(self):
    ini_fim_pairs = IniFimPairs(100)
    pair_list = [(10, 16), (8, 10), (0,8)]
    ini_fim_pairs.addlist(pair_list)
    intersection_doubles = []
    ift1 = IniFimTuple((0,8))
    ift2 = IniFimTuple((8,10))
    intersection_doubles.append((ift1, ift2))
    ift1 = IniFimTuple((8,10))
    ift2 = IniFimTuple((10,16))
    intersection_doubles.append((ift1, ift2))
    self.assertEqual(ini_fim_pairs.report_intersections(), intersection_doubles)

  def test5a_removerange(self):
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

  def test5b_removerange(self):
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
