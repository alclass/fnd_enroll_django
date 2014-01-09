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
  
  #=============================================================================
  # It's having problems with unittest.assertEqual(), so we solved this using two conditions, for the two coords: s[0]==p[0] and s[1]==p[1] 
  # def __eq__(self, p_pair):
  #   if type(p_pair) not in [tuple, list, IniFimTuple]:
  #     raise TypeError, 'type(p_pair) not in [tuple, list, IniFimTuple], type p_pair is %s' %str(type(p_pair))
  #   if len(self) == 0 and len(p_pair) == 0:
  #     return True
  #   if self[0] == p_pair[0] and self[1] == p_pair[1]:
  #     return True
  #   return False
  #=============================================================================

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
    if self[0] <= p_pair[0] and p_pair[1] <= self[1]:
      return IniFimTuple(p_pair)
    # 4th case: pair[0] is inside and pair[1] is outside
    if self[0] <= p_pair[0] <= self[1] and self[1] < p_pair[1]:
      return IniFimTuple((p_pair[0], self[1]))
    # 5th case: pair[0] is outside and pair[1] is inside
    if p_pair[0] < self[0] and self[0] <= p_pair[1] <= self[1]:
      return IniFimTuple((self[0], p_pair[1]))
    # 6th case: pair[0] is outside on the left and pair[1] is outside on the right, or at least both pair and self are equal; return self, ie, (self[0], self[1])
    if p_pair[0] <= self[0] and p_pair[1] >= self[1]:
      return self
    raise ValueError, 'None of the 6 cases in method intersect() were taken. This is a Program Logic Error. One should look into it.'

  def difference(self, p_pair):
    '''

    IMPORTANT: this method does not return a IniFimTuple, it returns a list of IniFimTuple's 

    Cases:
    # 1st case: pair is all outside by self's left-hand side, return self
    # 2nd case: pair is all outside by self's right-hand side, return self
    # 3rd case: pair contains self (ie, pair "overflows" self or at least is equal to self), return () # empty tuple
    # 4th case: pair[0] equals self[0] and pair[1] < self[1], return (pair[1]+1, self[1])
    # 5th case: pair[0] > self[0] and pair[1] equals self[1], return (self[0], pair[0]-1)
    # 6th case: pair is contained by self, 2 sets will return: { (self[0], pair[0]-1) and (pair[1]+1, self[1]) }
    '''
      
    if type(p_pair) in [tuple, list]:
      p_pair = IniFimTuple(p_pair)
    if type(p_pair) != IniFimTuple:
      raise TypeError, 'type(p_pair=%s) != IniFimTuple' %(str(p_pair))

    # 1st case where self is empty, so difference will also be empty
    if len(self) == 0:
      return [IniFimTuple(())] # empty IniFimTuple

    # 2nd case where self is empty, return self
    if len(p_pair) == 0:
      return [self]

    # 3rd case where self equals pair, return empty
    if p_pair[0] == self[0] and p_pair[1] == self[1]:
      return [IniFimTuple(())] # empty IniFimTuple

    # 4th case: pair is all outside by self's left-hand side, return self
    if p_pair[1] < self[0]:
      return [self]

    # 5th case: pair is all outside by self's right-hand side, return self
    if self[1] < p_pair[0]:
      return [self]
    
    # 6th case: pair contains self (ie, pair "overflows" self or at least is equal to self), return () # empty tuple
    if p_pair[0] <= self[0] and p_pair[1] >= self[1]:
      return [IniFimTuple(())] # empty IniFimTuple
    
    # 7th case: 1st coordinate is equal, pair[1] is inside
    if p_pair[0] == self[0] and p_pair[1] < self[1]: # notice that if pair[0]==self[0] the other coordinate cannot equal, for, if so, it's taken above
      x = p_pair[1] + 1; y = self[1]
      if x > y:
        return [IniFimTuple(())] # empty IniFimTuple
      else:
        return [IniFimTuple((x, y))]

    # 8th case: 2nd coordinate is equal, pair[0] is inside 
    if p_pair[0] > self[0] and p_pair[1] == self[1]: # notice that if pair[1]==self[1] the other coordinate cannot equal, for, if so, it's taken above
      x = self[0]; y = p_pair[0] - 1
      if x > y:
        return [IniFimTuple(())] # empty IniFimTuple
      else:
        return [IniFimTuple((x, y))]

    # 9th case: pair is inside, it's possible to return a 2-element list, a 1-element or a 1-element with an empty IniFimTuple
    if p_pair[0] > self[0] and p_pair[1] < self[1]:

      x1 = self[0]; y1 = p_pair[0] - 1
      inifimtuple1 = IniFimTuple((x1, y1))
      x2 = p_pair[1] + 1; y2 = self[1]
      inifimtuple2 = IniFimTuple((x2, y2))
      return [inifimtuple1, inifimtuple2]

    # 10th case: pair[0] < self[0] and pair[1] is within self
    if p_pair[0] < self[0] and self[0] < p_pair[1] < self[1]:
      return [IniFimTuple((p_pair[1] + 1, self[1]))]
      
    # 11th case: pair[0] is within self and pair[1] > self[1] 
    if self[0] < p_pair[0] < self[1] and self[1] < p_pair[1]:
      return [IniFimTuple((self[0], p_pair[0] - 1))]
      
    raise ValueError, 'None of the 9 cases in method difference() were taken. This is a Program Logic Error. One should look into it.'

      
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
    # 1st case where self is empty, so difference will also be empty
    '''
    inifim = IniFimTuple(())
    diff_pair = IniFimTuple((1,3))
    diff_from_method = inifim.difference(diff_pair)
    diff_should_be = [IniFimTuple(())]
    self.assertEqual(diff_from_method, diff_should_be)

  
  def test2_difference(self):
    '''
    # 2nd case where self is empty, return self
    '''
    pass
    inifim = IniFimTuple((4,8))
    diff_pair = IniFimTuple(())
    diff_from_method = inifim.difference(diff_pair)
    diff_should_be = [IniFimTuple((4, 8))]
    self.assertEqual(diff_from_method, diff_should_be)

  def test3_difference(self):
    '''
    # 3rd case where self equals pair, return empty
    '''
    inifim = IniFimTuple((4,8))
    diff_pair = IniFimTuple((4,8))
    diff_from_method = inifim.difference(diff_pair)
    diff_should_be = [IniFimTuple(())]
    self.assertEqual(diff_from_method, diff_should_be)


  def test4_difference(self):
    '''
    # 4th case: pair is all outside by self's left-hand side, return self
    '''
    inifim = IniFimTuple((40,80))
    diff_pair = IniFimTuple((4,30))
    diff_from_method = inifim.difference(diff_pair)
    diff_should_be = [IniFimTuple((40,80))]
    self.assertEqual(diff_from_method, diff_should_be)
    
  def test5_difference(self):
    '''
    # 5th case: pair is all outside by self's right-hand side, return self
    '''
    inifim = IniFimTuple((4,40))
    diff_pair = IniFimTuple((50,80))
    diff_from_method = inifim.difference(diff_pair)
    diff_should_be = [IniFimTuple((4,40))]
    self.assertEqual(diff_from_method, diff_should_be)

  def test6_difference(self):
    '''
    # 6th case: pair contains self (ie, pair "overflows" self or at least is equal to self), return () # empty tuple
    '''
    inifim = IniFimTuple((40,80))
    diff_pair = IniFimTuple((4,800))
    diff_from_method = inifim.difference(diff_pair)
    diff_should_be = [IniFimTuple(())]
    self.assertEqual(diff_from_method, diff_should_be)

  def test7_difference(self):
    '''
    # 7th case: 1st coordinate is equal, pair[1] is inside
    '''
    inifim = IniFimTuple((4,80))
    diff_pair = IniFimTuple((4,73))
    diff_from_method = inifim.difference(diff_pair)
    diff_should_be = [IniFimTuple((74,80))]
    self.assertEqual(diff_from_method, diff_should_be)

    inifim = IniFimTuple((4,80))
    diff_pair = IniFimTuple((4,79))
    diff_from_method = inifim.difference(diff_pair)
    diff_should_be = [IniFimTuple((80,80))]
    self.assertEqual(diff_from_method, diff_should_be)

  def test8_difference(self):
    '''
    # 8th case: 2nd coordinate is equal, pair[0] is inside
    '''
    inifim = IniFimTuple((4,80))
    diff_pair = IniFimTuple((40,80))
    diff_from_method = inifim.difference(diff_pair)
    diff_should_be = [IniFimTuple((4,39))]
    self.assertEqual(diff_from_method, diff_should_be)

    inifim = IniFimTuple((4,80))
    diff_pair = IniFimTuple((5,80))
    diff_from_method = inifim.difference(diff_pair)
    diff_should_be = [IniFimTuple((4,4))]
    self.assertEqual(diff_from_method, diff_should_be)

  def test9_difference(self):
    '''
    # 9th case: pair is inside, it's possible to return a 2-element list, a 1-element or a 1-element with an empty IniFimTuple
    '''
    inifim = IniFimTuple((4,80))
    diff_pair = IniFimTuple((40,70))
    diff_from_method = inifim.difference(diff_pair)
    diff_should_be = [IniFimTuple((4,39)), IniFimTuple((71,80))]
    self.assertEqual(diff_from_method, diff_should_be)

    inifim = IniFimTuple((4,80))
    diff_pair = IniFimTuple((5,79))
    diff_from_method = inifim.difference(diff_pair)
    diff_should_be = [IniFimTuple((4,4)), IniFimTuple((80,80))]
    self.assertEqual(diff_from_method, diff_should_be)


def unittests():
  unittest.main()


def test6_nonunittest():
  print '''
  inifim = IniFimTuple((4,80))
  diff_pair = IniFimTuple((50,73))
  diff_from_method = inifim.difference(diff_pair)
  diff_should_be = [IniFimTuple((4,49)), IniFimTuple((74,80))]
  '''
  inifim = IniFimTuple((4,80))
  diff_pair = IniFimTuple((50,73))
  diff_from_method = inifim.difference(diff_pair)
  diff_should_be = [IniFimTuple((4,49)), IniFimTuple((74,80))]
  print 'diff_from_method', diff_from_method
  print 'diff_should_be', diff_should_be
  
  

def process():
  '''
  '''
  test6_nonunittest()

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
