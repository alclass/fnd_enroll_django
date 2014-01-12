#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Created on 4 août 2013

@author: friend
'''

import sys
import __init__
import local_settings as ls

class DisciplinesComplement(object):
  '''
  This class mainly reads data from text files.
  
  At the moment, the following TWO static methods do this data reading: 
    + get_facultadas_dict() : reads the id's of facultadas from their corresponding text file registered in local_settings.py
    + get_cursadas_dict()   : reads the id's of cursadas from their corresponding text file registered in local_settings.py
  '''
  
  facultadas_dict      = None
  coursed_already_dict = None
  
  @staticmethod
  def get_facultadas_dict():
    '''
    + get_facultadas_dict() : reads the id's of facultadas from their corresponding text file registered in local_settings.py
    '''
    if DisciplinesComplement.facultadas_dict == None:
      text_file_abspath = ls.get_default_ids_facultadas_abspath()
      lines = open(text_file_abspath).readlines()
      DisciplinesComplement.facultadas_dict = {}
      for line in lines:
        try:
          code = line[:6]
          DisciplinesComplement.facultadas_dict[code]=1
        except IndexError:
          continue

      # in case there are disciplinas cursadas among the facultativas, clean them out
      cursadas_dict = DisciplinesComplement.get_cursadas_dict()
      for code in cursadas_dict:
        if code in DisciplinesComplement.facultadas_dict.keys():
          del DisciplinesComplement.facultadas_dict[code]
           
    return DisciplinesComplement.facultadas_dict
    
  @staticmethod
  def get_cursadas_dict():
    '''
    + get_cursadas_dict()   : reads the id's of cursadas from their corresponding text file registered in local_settings.py
    '''
    if DisciplinesComplement.coursed_already_dict == None:
      text_file_abspath = ls.get_default_ids_cursadas_abspath()
      lines = open(text_file_abspath).readlines()
      DisciplinesComplement.coursed_already_dict = {}
      for line in lines:
        try:
          code = line[:6]
          DisciplinesComplement.coursed_already_dict[code]=1
        except IndexError:
          continue 
    return DisciplinesComplement.coursed_already_dict


class T():
  x = 1
  
  @staticmethod
  def m1():
    print T.x
    

import unittest
class TestCase1(unittest.TestCase):

  def setUp(self):
    pass

  def test1_(self):
    pass

def unittests():
  unittest.main()

def process():
  '''
  T.m1()
  sys.exit(0)
  '''
  cursadas = DisciplinesComplement.get_cursadas_dict().keys()
  print 'Cursadas:', cursadas
  print 'Total', len(cursadas)
  facultadas = DisciplinesComplement.get_facultadas_dict().keys()
  print 'Facultadas:', facultadas
  print 'Total', len(facultadas)

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
