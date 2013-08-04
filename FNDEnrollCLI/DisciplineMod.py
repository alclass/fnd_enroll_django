#!/usr/bin/env python
#-*-coding:utf-8-*-
'''


'''
#import codecs
from datetime import time # date #, timedelta
#import os

import __init__
import local_settings as ls
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

default_facultadas_id_list = None
def get_default_facultadas_id_list():
  global default_facultadas_id_list
  if default_facultadas_id_list != None:
    return default_facultadas_id_list
  lines = open(ls.get_default_ids_facultadas_abspath()).readlines()
  default_facultadas_id_list = []
  for line in lines:
    discipline_id = line.lstrip(' \t').rstrip(' \t\r\n')
    default_facultadas_id_list.append(discipline_id)
  return default_facultadas_id_list


class Turma(object):
  
  def __init__(self):
    self.code = None    
    self.name = None
    self.instructor = None
    self.timetable = TimeTableDict()

  def add_timetable_element(self, weekday, time_range):
    if not timeutils.is_time_range_a_tuple_of_times(time_range):
      return False
    self.timetable[weekday] = time_range
    return True
  
  def __unicode__(self):
    outstr = u'Turma nº %s :: %s\n' %(self.code, self.name)
    outstr += u'Prof.: %s\n' %self.instructor
    outstr += str(self.timetable)
    return outstr

  def __str__(self):
    return self.__unicode__()
    

  def add_timetable_element_from_str_time_range(self, weekday, str_time_range):
    if weekday not in xrange(0, 7):
      return False
    try:
      pp = str_time_range.split(' ')
      str_time_start, str_time_finish = pp[0], pp[2]
      time_start  = timeutils.get_time_from_str_time(str_time_start)
      time_finish = timeutils.get_time_from_str_time(str_time_finish)
      if time_start == None or time_finish == None:
        return False
      time_range  = (time_start, time_finish)
      return self.add_timetable_element(weekday, time_range)
    except IndexError:
      pass
    return False


class Discipline(object):
  
  instance_store_dict = {}

  @staticmethod
  def get_discipline_from_store_or_create_and_store_it(code):
    if Discipline.instance_store_dict.has_key(code):
      discipline = Discipline.instance_store_dict[code]
      discipline.add_empty_current_turma()
      return discipline
    discipline = Discipline(code)
    Discipline.instance_store_dict[code] = discipline
    return discipline

  @staticmethod
  def get_all_stored_disciplines():
    return Discipline.instance_store_dict.values()

  def __init__(self, code):
    '''
    '''
    self.code = code
    self.turmas = []
    self.add_empty_current_turma()

  def add_empty_current_turma(self):
    self.current_turma = Turma()
    self.turmas.append(self.current_turma)
    
  def __unicode__(self):
    outstr = u'Disciplina: %s\n' %self.code 
    outstr += u'Turma(s):\n'
    for turma in self.turmas:
      outstr += str(turma)
    return outstr

  def __str__(self):
    return self.__unicode__()
    

def test1():
  code = 'IUS518'
  d = Discipline(code)
  d.current_turma.code = '1234'
  d.current_turma.name = 'Direito da Integração'
  d.current_turma.instructor = 'João Alves'
  #
  time_start  = time(hour=7,minute=30)
  time_finish = time(hour=9,minute=10)
  time_range  = time_start, time_finish
  result = d.current_turma.add_timetable_element(0, time_range)
  print 'Added', time_range, result
  time_start  = time(hour=10,minute=30)
  time_finish = time(hour=11,minute=20)
  time_range  = time_start, time_finish
  result = d.current_turma.add_timetable_element(2, time_range)
  print 'Added', time_range, result
  print d


def process2():
  timetable = None
  if '-w' in sys.argv:
    weekday = get_weekday()
    if '-t' in sys.argv:
      times = get_times()
    timetable = TimeTableDict()
    timetable[weekday] = times
  if timetable:
    scraper = TextDataScraper()
    scraper.find_by_
  
def process():
  id_list = get_default_facultadas_id_list()
  print id_list
  print 'Total', len(id_list)
  test1()
        
if __name__ == '__main__':
  process()
