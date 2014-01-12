#!/usr/bin/env python
#-*-coding:utf-8-*-
'''


'''
#import codecs
from datetime import time # date #, timedelta
#import os
import sys

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
from DisciplinesComplementMod import DisciplinesComplement
from TurmaMod import Turma
from timeutils import K

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



class Discipline(object):
  
  instance_store_dict = {}

  @staticmethod
  def get_discipline_from_store_or_create_and_store_it(code):
    if Discipline.instance_store_dict.has_key(code):
      discipline = Discipline.instance_store_dict[code]
      return discipline
    discipline = Discipline(code)
    Discipline.instance_store_dict[code] = discipline
    return discipline

  @staticmethod
  def get_discipline_from_store_or_None(code):
    if Discipline.instance_store_dict.has_key(code):
      discipline = Discipline.instance_store_dict[code]
      return discipline
    return None
  
  @staticmethod
  def get_all_stored_disciplines():
    return Discipline.instance_store_dict.values()

  @staticmethod
  def get_cursadas():
    coursed_already_dict = DisciplinesComplement.get_cursadas_dict()
    if coursed_already_dict == None:
      return []
    disciplines = []
    for code in coursed_already_dict.keys():
      discipline = Discipline.get_discipline_from_store_or_None(code)
      if discipline != None:
        disciplines.append(discipline)
    return disciplines
  
  @staticmethod
  def get_facultadas():
    facultadas_dict = DisciplinesComplement.get_facultadas_dict()
    if facultadas_dict == None:
      return []

    disciplines = []
    for code in facultadas_dict.keys():
      discipline = Discipline.get_discipline_from_store_or_None(code)
      if discipline != None:
        disciplines.append(discipline)
    return disciplines

  def __init__(self, code):
    '''
    '''
    self.code = code
    self.turmas_dict = {}
    self.current_turma = None #Turma() # this is a -1 turma, ie, a sort-of null turma
    self.name = None

  def add_turma(self, turma):
    '''
    3 things happen here:
    1) The turma object (reference) receives self (the discipline itself), a registration act;
    2) The turma object (reference) becomes the "current_turma"
    3) The turma object (reference) is stocked in the turmas_dict
    '''
    turma.discipline = self
    self.current_turma = turma
    self.turmas_dict[turma.code] = self.current_turma
    
  def get_current_turma(self):
    return self.current_turma

  def get_turmas(self):
    return self.turmas_dict.values()

  def is_it_facultada(self):
    facultadas_dict = DisciplinesComplement.get_facultadas_dict()
    if facultadas_dict == None:
      return False
    if self.code in facultadas_dict.keys():
      return True
    return False
  
  def is_it_cursada(self):
    coursed_already_dict = DisciplinesComplement.get_cursadas_dict()
    if coursed_already_dict == None:
      return False
    if self.code in coursed_already_dict.keys():
      return True
    return False
    
  def __unicode__(self):
    outstr = u'Disciplina: %s\n' %self.code 
    outstr += u'Turma(s):\n'
    for turma in self.get_turmas():
      outstr += unicode(turma)
    return outstr

  def __str__(self):
    return self.__unicode__()
    

def test1():
  code = 'IUS518'
  discipline = Discipline(code)
  discipline.name = 'Direito da Integração'
  turma = Turma(turma_code_number='1234')
  turma.instructor = 'João Alves'
  discipline.add_turma(turma)
  
  bool_result = discipline.current_turma.add_timetable_element(K.MONDAY, K.M1, K.M2)
  pytime_range = K.get_pytime_range_from_time_labels(K.M1, K.M2)
  print 'Added', pytime_range, bool_result
  bool_result = discipline.current_turma.add_timetable_element(K.MONDAY, K.M1, K.M2)
  pytime_range = K.get_pytime_range_from_time_labels(K.M4, K.M5)
  print 'Added', pytime_range, bool_result
  print unicode(discipline)


import unittest
class TestCase1(unittest.TestCase):

  def setUp(self):
    pass

  def test1_(self):
    discipline_code = 'IUS518'
    discipline = Discipline(discipline_code)
    discipline_name = 'Direito da Integração'
    discipline.name = discipline_name 
    turma_code = '1234'
    turma = Turma(turma_code)
    turma.instructor = 'João Alves'
    discipline.add_turma(turma)
    self.assertEqual(discipline.code, discipline_code)
    self.assertEqual(discipline.name, discipline_name)
    self.assertEqual(discipline.get_current_turma(), turma)
    self.assertEqual(discipline.get_current_turma().code, turma_code)
    

def unittests():
  unittest.main()


def process():
  id_list = get_default_facultadas_id_list()
  print id_list
  print 'Total', len(id_list)
  test1()

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
