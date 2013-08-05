#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Created on 4 août 2013

@author: friend
'''

import os, sys
import __init__
import local_settings as ls

class DisciplinesComplement(object):
  
  facultadas_dict      = None
  coursed_already_dict = None
  
  @staticmethod
  def get_facultadas_dict():
    if DisciplinesComplement.facultadas_dict == None:
      text_filename = 'ids_de_facultadas.txt'
      text_file_abspath = os.path.join(ls.get_app_data_dir_abspath(), text_filename)
      lines = open(text_file_abspath).readlines()
      DisciplinesComplement.facultadas_dict = {}
      for line in lines:
        try:
          code = line[:6]
          DisciplinesComplement.facultadas_dict[code]=1
        except IndexError:
          continue 
    return DisciplinesComplement.facultadas_dict
    
  @staticmethod
  def get_coursed_already_dict():
    if DisciplinesComplement.coursed_already_dict == None:
      text_filename = 'ids_de_cursadas.txt'
      text_file_abspath = os.path.join(ls.get_app_data_dir_abspath(), text_filename)
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
    

def process():
  '''
  T.m1()
  sys.exit(0)
  '''
  coursed = DisciplinesComplement.get_coursed_already_dict().keys()
  print 'Cursadas:', coursed
  coursed = DisciplinesComplement.get_facultadas_dict().keys()
  print 'Facultadas:', coursed
        
if __name__ == '__main__':
  process()
