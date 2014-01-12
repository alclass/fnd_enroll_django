#!/usr/bin/env python
#-*-coding:utf-8-*-
'''


'''
#import codecs
from datetime import time # date #, timedelta
#import os
import sys

from IniFimTupleMod import IniFimTuple
import __init__
import local_settings as ls
import timeutils
from timeutils import K

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
from DisciplinesComplementMod import DisciplinesComplement

default_facultadas_id_list = None
def get_default_facultadas_id_list():
  global default_facultadas_id_list
  if default_facultadas_id_list != None:
    return default_facultadas_id_list
  lines = open(ls.get_default_ids_facultadas_abspath()).readlines()
  default_facultadas_id_list = []
  for line in lines:
    discipline_id = line.lstrip(' \t').rstrip(' \t\r\n')
    if discipline_id not in default_facultadas_id_list: 
      default_facultadas_id_list.append(discipline_id)
  return default_facultadas_id_list


class Turma(object):
  
  def __init__(self, turma_code=None):
    self.code = turma_code    
    self.discipline = None
    self.derived_name_from_discipline = None
    self.number_or_letter = None
    self.instructor = None
    self.sala       = None
    self.timetable  = TimeTableDict()  # Each key (a weekday) maps to a IniFimPairs, which is a list of IniFimTuples

  def add_timetable_element_with_ini_fim_tuple(self, weekday, ini_fim_tuple):
    try:
      self.timetable[weekday] = ini_fim_tuple
    except ValueError:
      return False
    return True

  def add_timetable_element_with_label_times(self, weekday, ini_time_label, fim_time_label):
    try:
      ini_fim_tuple = IniFimTuple.generate_instance_from_labels(ini_time_label, fim_time_label)
      self.timetable[weekday] = ini_fim_tuple 
    except ValueError:
      return False
    return True

  def add_timetable_element_with_pytimes(self, weekday, ini_pytime, fim_pytime):
    try:
      print 'In add_timetable_element_with_pytimes()', weekday, ini_pytime, fim_pytime
      ini_fim_tuple = IniFimTuple.generate_instance_from_start_and_finish_times(ini_pytime, fim_pytime)
      print 'In add_timetable_element_with_pytimes() :: ini_fim_tuple =', ini_fim_tuple 
      self.timetable[weekday] = ini_fim_tuple 
    except ValueError:
      return False
    return True

  def add_timetable_element_with_str_times(self, weekday, ini_str_time, fim_str_time):
    ini_pytime = timeutils.get_time_from_str_time(ini_str_time)
    fim_pytime = timeutils.get_time_from_str_time(fim_str_time)
    return self.add_timetable_element_with_pytimes(weekday, ini_pytime, fim_pytime)

  def does_turma_happen_at_time_labels(self, weekday, p_time_labels):
    time_labels = self.timetable.get_time_labels_for_weekday(weekday)
    if time_labels == None or time_labels == []:
      return False
    for p_time_label in p_time_labels:
      if p_time_label in time_labels:
        return True 
    return False
  
  def __unicode__(self):
    outstr = u'Turma nº %s :: %s\n' %(self.code, self.number_or_letter)
    outstr += u'Prof.: %s\n' %self.instructor
    for weekday in self.timetable:
      line = u'%s : %s\n' %(TimeTableDict.weekday_3letter(weekday), self.timetable.get_time_labels_for_weekday(weekday))
      outstr += line
    return outstr

  def __str__(self):
    return self.__unicode__()
    

import unittest
class TestCase1(unittest.TestCase):

  def setUp(self):
    pass

  def test1_(self):
    turma = Turma('1234')
    turma.add_timetable_element_with_label_times(0, K.M1, K.M2)
    

def unittests():
  unittest.main()


def process():
  turma = Turma('1234')
  turma.number_or_letter = 'N'
  turma.instructor = u'João Alves'
  turma.add_timetable_element_with_label_times(0, K.M1, K.M2)
  turma.add_timetable_element_with_label_times(2, K.M5, K.T1)
  print unicode(turma)

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()


        
if __name__ == '__main__':
  process()
