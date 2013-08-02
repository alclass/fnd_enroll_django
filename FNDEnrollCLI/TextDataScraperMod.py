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


class TextDataScraper(object):
  
  def __init__(self, txtfile_abspath):
    self.txtfile_abspath = txtfile_abspath
    self.disciplines = []
    
  def read_data(self):
    
    data_file = codecs.open(self.txtfile_abspath, 'r', encoding='utf-8')
    lines = data_file.readlines()
    for i, line in enumerate(lines):
      line = line.strip(' \t\r\n')
      if line == '':
        continue
      line_n = i + 1
      if line_n % 8 == 1:
        # discipline id / code
        discipline = Discipline()
        discipline.set_id(line.lstrip(' \t')) 
      elif line_n % 8 == 3:
        # discipline group
        discipline.group = line.lstrip(' \t') 
      elif line_n % 8 == 4:
        # discipline name
        discipline.name = line.lstrip(' \t') 
      elif line_n % 8 == 5:
        # discipline 3-letter weekday
        weekday3l = line.lstrip(' \t')
        keep_ahead_weekday = timeutils.get_weekday_from_weekday3l(weekday3l) 
      elif line_n % 8 == 7:
        # discipline times
        phrase = line.lstrip(' \t')
        pp = phrase.split(' ')
        str_time_start, str_time_finish = pp[0], pp[2]
        time_start = timeutils.get_time_from_str_time(str_time_start)
        time_finish = timeutils.get_time_from_str_time(str_time_finish)
        time_range = (time_start, time_finish)
        discipline.add_timetable_element(keep_ahead_weekday, time_range)
      elif line_n % 8 == 0:
        # discipline instructor
        discipline.instructor = line.lstrip(' \t')
        self.disciplines.append(discipline)
        
  def list_disciplines(self):
    for i, discipline in enumerate(self.disciplines):
      print i+1, discipline

  def find_by_weekday(self, weekday):
    found_list = []
    for discipline in self.disciplines:
      if discipline.timetable.has_key(weekday):
        found_list.append(discipline)
    return found_list 

  def find_by_times(self, contiguous_time_labels):
    time_start_and_finish_tuples = ls.convert_time_labels_to_time_start_and_finish_tuples(contiguous_time_labels)
    found_list = []
    for discipline in self.disciplines:
      for time_start_and_finish_tuple in time_start_and_finish_tuples:
        if discipline.is_within_comparative_time_start_and_finish(time_start_and_finish_tuple):
          found_list.append(discipline)
    return found_list 

     
def find_by_weekday(data_obj):
  for weekday in xrange(7):
    disciplines = data_obj.find_by_weekday(weekday)
    if disciplines == []:
      continue 
    print 'weekday = ', weekday
    for discipline in disciplines:
      print discipline._id, discipline.name 
    
def process():
  txtfilename = 'disciplines_1.txt'
  txtfile_abspath = os.path.join(ls.get_app_data_dir_abspath(), txtfilename)
  data_obj = TextDataScraper(txtfile_abspath)
  data_obj.read_data()
  #data_obj.list_disciplines()
  find_by_weekday(data_obj)
  
        
if __name__ == '__main__':
  process()
