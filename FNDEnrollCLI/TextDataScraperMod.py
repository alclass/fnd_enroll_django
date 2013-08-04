#!/usr/bin/env python
#-*-coding:utf-8-*-
'''


'''

import codecs
#import datetime
from datetime import time #, timedelta
import os

import __init__
import local_settings as ls
import timeutils

from DisciplineMod import Discipline
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

import string
UPPERCASE_26_LETTERS = string.letters[26:]
lambda_each_uppercase = lambda x : x in UPPERCASE_26_LETTERS    
def is_line_discipline_id(line):
  if len(line) != 6:
    return False
  letters = line[:3]
  result_bool_list = map(lambda_each_uppercase, letters)
  if False in result_bool_list:
    return False
  str_numbers = line[3:]
  try:
    int(str_numbers)
    return True
  except ValueError:
    pass
  return False

def is_line_turma_ie_a_number(str_numbers):
  try:
    int(str_numbers)
    return True
  except ValueError:
    pass
  return False

def return_time_range_from_str_from_to_time_or_None(line):
  try:
    pp = line.split(' ')
    str_time_start, str_time_finish = pp[0], pp[2]
    time_start  = timeutils.get_time_from_str_time(str_time_start)
    time_finish = timeutils.get_time_from_str_time(str_time_finish)
    if time_start == None or time_finish == None:
      return None
    time_range  = (time_start, time_finish)
    return time_range
  except IndexError:
    pass  
  return None

class TextDataScraper(object):
  
  def __init__(self, txtfile_abspath=None):
    if txtfile_abspath == None:
      txtfile_abspath = ls.get_default_oferecidas_abspath() 
    self.txtfile_abspath = txtfile_abspath
    self.has_read_data_run = False

  def get_all_scraped_disciplines(self):
    '''
    It verifies first whether or not read_data() has run
    If so, return the stored instances in the Discipline store dict
    '''
    if self.has_read_data_run:
      return Discipline.get_all_stored_disciplines()
    return None
        
  def read_data(self):
    
    data_file = codecs.open(self.txtfile_abspath, 'r', encoding='utf-8')
    lines = data_file.readlines()
    next_is_instructor      = False
    next_is_discipline_name = False
    keep_ahead_weekday = None
    discipline = None
    for _, line in enumerate(lines):
      line = line.lstrip(' \t').rstrip(' \t\r\n')
      if line == '':
        continue
      if is_line_discipline_id(line):
        code = line
        discipline = Discipline.get_discipline_from_store_or_create_and_store_it(code)
        continue        
      if is_line_turma_ie_a_number(line):
        discipline.current_turma.code = line
        next_is_discipline_name = True
        continue
      if line in timeutils.dict_pt_3_letter_weekday.values():
        keep_ahead_weekday = timeutils.get_weekday_from_weekday3l(line) 
        continue
      if next_is_discipline_name:
        discipline.current_turma.name = line
        next_is_discipline_name = False
        continue
      time_range = return_time_range_from_str_from_to_time_or_None(line)
      if time_range != None and keep_ahead_weekday != None:
        has_been_added = discipline.current_turma.add_timetable_element(keep_ahead_weekday, time_range)
        if not has_been_added:
          print time_range, 'has not been added.' 
        keep_ahead_weekday = None
        next_is_instructor = True
        continue
      if next_is_instructor:
        discipline.current_turma.instructor = line
        next_is_instructor = False

    self.has_read_data_run = True
        
  def find_by_weekday(self, weekday):
    turma_found_list = []
    disciplines = self.get_all_scraped_disciplines()
    if disciplines is None:
      return []
    for discipline in disciplines:
      for turma in discipline.turmas:
        if turma.timetable.has_key(weekday):
          turma_found_list.append(turma)
    return turma_found_list 

  def find_by_timetable(self, p_ref_timetable):
    '''
    timetable, though also a dict, is a 2D data per element
    ie, it contains weekdays (each one is 0 to 6) and for each weekday an array of time ranges (each time range is a from/to time tuple)
    
    To search by timetable is to look all turmas and see which ones coincide 
    '''
    turma_found_list = []
    disciplines = self.get_all_scraped_disciplines()
    if disciplines is None:
      return []
    for discipline in disciplines:
      for turma in discipline.turmas:
        if turma.timetable == p_ref_timetable:
          turma_found_list.append(turma)
    return turma_found_list 

     
def find_by_weekday(data_obj):
  for weekday in xrange(7):
    disciplines = data_obj.find_by_weekday(weekday)
    if disciplines == []:
      continue 
    print 'weekday = ', weekday
    for discipline in disciplines:
      print discipline._id, discipline.name 
    
def process():
  data_obj = TextDataScraper()
  data_obj.read_data()
  #data_obj.list_disciplines()
  # find_by_weekday(data_obj)
  counter = 0
  for discipline in data_obj.get_all_scraped_disciplines():
    counter += 1
    print '-'*20, counter, '-'*20
    print discipline 
    print '-'*40
  
        
if __name__ == '__main__':
  process()
