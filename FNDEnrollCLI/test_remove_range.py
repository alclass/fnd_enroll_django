#!/usr/bin/env python
#-*-coding:utf-8-*-
'''

'''
#import codecs
import os, sys

class IniFimTuple(tuple):
  
  def __init__(self, tuple_pair):
    if tuple_pair == None:
      raise ValueError, 'IniFimTuple(tuple) cannot be initialized with None.'
    if tuple_pair == ():
      super(IniFimTuple, self).__init__(())
      return
    index_ini, index_fim = self.validate_tuple_pair(tuple_pair)
    super(IniFimTuple, self).__init__((index_ini, index_fim))
    
  def validate_tuple_pair(self, tuple_pair):
    if len(tuple_pair) != 2:
      raise ValueError, 'IniFimTuple(tuple) should have exactly 2 values.  It is %s.' %(str(tuple_pair))
    try:
      index_ini, index_fim = int(tuple_pair[0]), int(tuple_pair[1])
    except ValueError:
      raise ValueError, 'Failed to int pair : index_ini, index_fim = int(index_ini), int(index_fim)' 
    if index_ini > index_fim:
      raise IndexError, 'index_ini (%d) > index_fim (%d)' %(index_ini, index_fim) 
    return index_ini, index_fim

  def intersect(self, p_pair):
    '''
    Cases:
    # 1st case: pair is all outside by self's left-hand side, return () # empty tuple
    # 2nd case: pair is all outside by self's right-hand side, return () # empty tuple
    # 3rd case: pair is all inside, return pair itself
    # 4th case: pair[0] is inside and pair[1] is outside, return (pair[0], self[1])
    # 5th case: pair[0] is outside and pair[1] is inside, return (self[0], pair[1])
    # 6th case: pair[0] is outside on the left and pair[1] is outside on the right, return self, ie, (self[0], self[1])
    '''
    # 1st case: pair is all outside by self's left-hand side
    if p_pair[1] < self[0]:
      return IniFimTuple(()) # empty tuple
    # 2st case: pair is all outside by self's right-hand side
    if self[1] < p_pair[0]:
      return IniFimTuple(()) # empty tuple
    # 3st case: pair is all inside
    if self[0] <= p_pair[0] <= self[1]:
      if self[0] <= p_pair[1] <= self[1]:
        return IniFimTuple(p_pair)
      # 4th case: pair[0] is inside and pair[1] is outside
      interset = IniFimTuple((p_pair[0], self[1]))
      return interset
    # 5th case: pair[0] is outside and pair[1] is inside
    if self[0] <= p_pair[1] <= self[1]:
      interset = IniFimTuple((self[0], p_pair[1]))
      return interset
    if p_pair[0] <= self[0] and p_pair[1] >= self[1]:
      return self
    raise ValueError, 'None of the 6 cases in method intersect() were taken. This is a Program Logic Error. One should look into it.'

  def difference(self, p_pair):
    '''
    Cases:
    # 1st case: pair is all outside by self's left-hand side, return self
    # 2nd case: pair is all outside by self's right-hand side, return self
    # 3rd case: pair contains self (ie, pair "overflows" self or at least is equal to self), return () # empty tuple
    # 4th case: pair[0] equals self[0] and pair[1] < self[1], return (pair[1]+1, self[1])
    # 5th case: pair[0] > self[0] and pair[1] equals self[1], return (self[0], pair[0]-1)
    # 6th case: pair is contained by self, 2 sets will return: { (self[0], pair[0]-1) and (pair[1]+1, self[1]) }
    '''
      
    if type(p_pair) == tuple:
      p_pair = IniFimTuple(p_pair)
    if type(p_pair) != IniFimTuple:
      raise TypeError, 'type(p_pair=%s) != IniFimTuple' %(str(p_pair))

    if len(self) == 0:
      return [IniFimTuple(())]

    # 1st case: pair is all outside by self's left-hand side, return self
    if len(p_pair) == 0 or p_pair[1] < self[0]:
      return [self] # empty tuple

    # 2nd case: pair is all outside by self's right-hand side, return self
    if self[1] < p_pair[0]:
      return [self] # empty tuple
    
    # 3rd case: pair contains self (ie, pair "overflows" self or at least is equal to self), return () # empty tuple
    if p_pair[0] <= self[0] and p_pair[1] >= self[1]:
      return [IniFimTuple(())]
    
    # 4th case: pair[0] equals self[0] and pair[1] < self[1], return (pair[1]+1, self[1])
    if p_pair[0] == self[0] and p_pair[1] < self[1]:
      return [IniFimTuple((p_pair[1]+1, self[1]))]
    
    # 5th case: pair[0] > self[0] and pair[1] equals self[1], return (self[0], pair[0]-1)
    if p_pair[0] > self[0] and p_pair[1] == self[1]:
      return [IniFimTuple((self[0], p_pair[0]-1))]

    # 6th case: pair is contained by self, 2 sets will return: { (self[0], pair[0]-1) and (pair[1]+1, self[1]) }
    if p_pair[0] > self[0] and p_pair[1] < self[1]:
      return [IniFimTuple((self[0], p_pair[0]-1)), IniFimTuple((p_pair[1]+1, self[1]))]
    
    raise ValueError, 'None of the 6 cases in method difference() were taken. This is a Program Logic Error. One should look into it.'

    
    
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

  def remove_range_inner_recursive(self, removal_range, index=0):
    if index > len(self) - 1 or len(removal_range) == 0:
      return # finishes recursion
    pair = self[index]
    result_list = pair.difference(removal_range)
    # updates removal_range in case it has been "consumed" 
    removal_range_list = removal_range.difference(pair)
    # removal_range_list can either be a 1-element or a 2-element list, if it's a 1-element, renew removal_range, otherwise, let it recurse as it is
    if len(removal_range_list) == 1:
      removal_range = removal_range_list[0]
      # if it's length 2, do not change removal_range, let it recurse as it is, 
      # because this algorithm does not spawn for more than 1 IniFimTuple as the removal_range
      # (it still works logically okay, it's just a little bigger than it should be, no problem)

    if len(result_list) == 1:
      inifimtuple = result_list[0]
      if len(inifimtuple) == 2:
        self[index] = inifimtuple
        index += 1 # for recursion
      else: # ie: if len(inifimtuple) == 0:
        del self[index]
        # do not add 1 to index in this case
      return self.remove_range_inner_recursive(removal_range, index)
    # else: ie, if len(result_list) == 2:
    self[index] = result_list[0]
    self.insert(index+1, result_list[1])
    return self.remove_range_inner_recursive(removal_range, index)
  
  def remove_range(self, removal_range, index=0):
    if type(removal_range) == tuple:
      removal_range = IniFimTuple(removal_range)
    if type(removal_range) != IniFimTuple:
      raise TypeError, 'type(removal_range) != IniFimTuple'
    return self.remove_range_inner_recursive(removal_range, index)
        
      
import unittest
class TestCaseIniFimTuple(unittest.TestCase):

  def setUp(self):
    pass

  def test1_intersect(self):
    '''
    1st case: pair is all outside by self's left-hand side, return () # empty tuple
    '''
    inifim = IniFimTuple((4,8))
    intersect_pair = IniFimTuple((1,3))
    intersection_from_method = inifim.intersect(intersect_pair)
    intersect_should_be = IniFimTuple(())
    self.assertEqual(intersection_from_method, intersect_should_be)

  
  def test2_intersect(self):
    '''
    # 2nd case: pair is all outside by self's right-hand side, return () # empty tuple
    '''
    pass
    inifim = IniFimTuple((4,8))
    intersect_pair = IniFimTuple((11,33))
    intersection_from_method = inifim.intersect(intersect_pair)
    intersect_should_be = IniFimTuple(())
    self.assertEqual(intersection_from_method, intersect_should_be)

  def test3_intersect(self):
    '''
    # 3rd case: pair is all inside, return pair itself
    '''
    inifim = IniFimTuple((40,80))
    intersect_pair = IniFimTuple((45,55))
    intersection_from_method = inifim.intersect(intersect_pair)
    intersect_should_be = IniFimTuple((45,55))
    self.assertEqual(intersection_from_method, intersect_should_be)


  def test4_intersect(self):
    '''
    # 4th case: pair[0] is inside and pair[1] is outside, return (pair[0], self[1])
    '''
    inifim = IniFimTuple((4, 8))
    intersect_pair = IniFimTuple((6,55))
    intersection_from_method = inifim.intersect(intersect_pair)
    intersect_should_be = IniFimTuple((6, 8))
    self.assertEqual(intersection_from_method, intersect_should_be)
    
  def test5_intersect(self):
    '''
    # 5th case: pair[0] is outside and pair[1] is inside, return (self[0], pair[1])
    '''
    inifim = IniFimTuple((4, 8))
    intersect_pair = IniFimTuple((2,7))
    intersection_from_method = inifim.intersect(intersect_pair)
    intersect_should_be = IniFimTuple((4, 7))
    self.assertEqual(intersection_from_method, intersect_should_be)

  def test6_intersect(self):
    '''
    # 6th case: pair[0] is outside on the left and pair[1] is outside on the right, return self, ie, (self[0], self[1])
    '''
    inifim = IniFimTuple((10,20))
    intersect_pair = IniFimTuple((5,25))
    intersection_from_method = inifim.intersect(intersect_pair)
    intersect_should_be = IniFimTuple((10,20))
    self.assertEqual(intersection_from_method, intersect_should_be)
    
  def test1_difference(self):
    '''
    # 1st case: pair is all outside by self's left-hand side, return self
    '''
    inifim = IniFimTuple((4,8))
    diff_pair = IniFimTuple((1,3))
    diff_from_method = inifim.difference(diff_pair)
    diff_should_be = [IniFimTuple((4, 8))]
    self.assertEqual(diff_from_method, diff_should_be)

  
  def test2_difference(self):
    '''
    # 2nd case: pair is all outside by self's right-hand side, return self
    '''
    pass
    inifim = IniFimTuple((4,8))
    diff_pair = IniFimTuple((11,33))
    diff_from_method = inifim.difference(diff_pair)
    diff_should_be = [IniFimTuple((4, 8))]
    self.assertEqual(diff_from_method, diff_should_be)

  def test3_difference(self):
    '''
    # 3rd case: pair contains self (ie, pair "overflows" self or at least is equal to self), return () # empty tuple
    '''
    inifim = IniFimTuple((4,8))
    diff_pair = IniFimTuple((1,30))
    diff_from_method = inifim.difference(diff_pair)
    diff_should_be = [IniFimTuple(())]
    self.assertEqual(diff_from_method, diff_should_be)


  def test4_difference(self):
    '''
    # 4th case: pair[0] equals self[0] and pair[1] < self[1], return (pair[1]+1, self[1])
    '''
    inifim = IniFimTuple((4,80))
    diff_pair = IniFimTuple((4,30))
    diff_from_method = inifim.difference(diff_pair)
    diff_should_be = [IniFimTuple((31,80))]
    self.assertEqual(diff_from_method, diff_should_be)
    
  def test5_difference(self):
    '''
    # 5th case: pair[0] > self[0] and pair[1] equals self[1], return (self[0], pair[0]-1)
    '''
    inifim = IniFimTuple((4,80))
    diff_pair = IniFimTuple((50,80))
    diff_from_method = inifim.difference(diff_pair)
    diff_should_be = [IniFimTuple((4,49))]
    self.assertEqual(diff_from_method, diff_should_be)

  def test6_difference(self):
    '''
    # 6th case: pair is contained by self, 2 sets will return: { (self[0], pair[0]-1) and (pair[1]+1, self[1]) }
    '''
    inifim = IniFimTuple((4,80))
    diff_pair = IniFimTuple((50,73))
    diff_from_method = inifim.difference(diff_pair)
    diff_should_be = [IniFimTuple((4,49)), IniFimTuple((74,80))]
    self.assertEqual(diff_from_method, diff_should_be)


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

  def test1_removerange(self):
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


def unittests():
  unittest.main()


def quick_check():
  print 'Running quick_check() to check the tuple-wrapper type for pairs added to an IniFimPairs object.'
  ini_fim_pairs = IniFimPairs(17)
  pair_list = [(0, 10), (13, 16)]
  ini_fim_pairs.addlist(pair_list)
  


def process():
  '''
  '''
  quick_check()

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
