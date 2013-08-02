#!/usr/bin/env python
#-*-coding:utf-8-*-
'''


'''
#import codecs
from datetime import time # date #, timedelta
#import os

import __init__
#import local_settings as ls
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

from TimeTableDictMod import TimeTableDict 

class Discipline(object):
  
  attrib_strs = ['code', 'group', 'name', 'timetable', 'instructor']

  def __init__(self):
    self.init_attribs()
    self.disciplines = []
    self.timetable = TimeTableDict()
    self.contiguous_time_start_and_finish_tuple_list = []

  def init_attribs(self):
    '''
    self.code   = None 
    self.group = None 
    self.name  = None 
    self.weekday3l  = None 
    self.times      = None
    self.instructor = None
    '''
    for attrib_str in self.attrib_strs:
      exec('self.%s = None' %attrib_str) 
    self.attribs_dict = None
    _ = self.return_attribs_dict()

  def set_id(self, code):
    self._id  = code
    self.code = code
    
  def add_timetable_element(self, weekday, time_range):
    if not timeutils.is_time_range_a_tuple_of_times(time_range):
      return False
    self.timetable[weekday] = time_range
    return True
    

  def add_contiguous_time_start_and_finish_tuple(self, time_start_and_finish_tuple):
    self.contiguous_time_start_and_finish_tuple_list.append(time_start_and_finish_tuple)
    
  def return_attribs_dict(self):
    if self.attribs_dict == None:
      self.init_attribs_dict()
    return self.attribs_dict 
  
  def init_attribs_dict(self): 
    self.attribs_dict = {}
    for attrib_str in self.attrib_strs:
      if eval('self.%s' %attrib_str) == None:
        continue 
      exec_str = 'self.attribs_dict["%(key)s"]="%(value)s"' %{'key':attrib_str, 'value':eval('self.%s' %attrib_str)}
      print exec_str
      exec(exec_str) 
    return self.attribs_dict
  
  def is_within_comparative_time_start_and_finish(self, time_start_and_finish_tuple):
    pass
      
  def __unicode__(self):
    outstr = u'Disciplina:\n=============\n' 
    for attrib_str in self.attrib_strs:
      if eval('self.%s' %attrib_str) == None:
        continue 
      outstr += '%(key)s = %(value)s\n' %{'key':attrib_str, 'value':eval('self.%s' %attrib_str)}
    outstr += str(self.timetable)
    return outstr

  def __str__(self):
    return self.__unicode__()
    

def test1():
  d = Discipline()
  d.set_id('IUS518')  
  d.name = 'Direito da Integração'
  time_start  = time(hour=7,minute=30)
  time_finish = time(hour=9,minute=10)
  time_range  = time_start, time_finish
  result = d.add_timetable_element(0, time_range)
  print 'Added', time_range, result
  time_start  = time(hour=10,minute=30)
  time_finish = time(hour=11,minute=20)
  time_range  = time_start, time_finish
  result = d.add_timetable_element(2, time_range)
  print 'Added', time_range, result
  print d

  
def process():
  test1()  
        
if __name__ == '__main__':
  process()
