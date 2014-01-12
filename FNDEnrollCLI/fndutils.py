#!/usr/bin/env python
#-*-coding:utf-8-*-
'''

'''
import sys

import __init__
import local_settings as ls

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

def clean_name_finishing_the_ending(name):
  new_name = name
  if new_name.find('Tarde') > -1:
    new_name = new_name.replace('Tarde','')
  if new_name.find('Manhã') > -1:
    new_name = new_name.replace('Manhã','')
  if new_name.find('Noite') > -1:
    new_name = new_name.replace('Manhã','')
  new_name = new_name.rstrip('- ')
  return new_name

def reset_derived_name_if_equal_beginning_str(derived_name, name):
  index = len(derived_name)
  for i in xrange(len(derived_name)):
    if i > len(name) - 1:
      index = i
      break 
    if derived_name[i] != name[i]:
      index = i
      break
  new_derived_name = derived_name[:index]
  return new_derived_name 

def derive_name_from_names(names):
  if names == None or len(names) == 0:
    return None
  derived_name = names[0]
  for name in names[1:]:
    derived_name = reset_derived_name_if_equal_beginning_str(derived_name, name)
  return derived_name 
    


import unittest
class TestCase1(unittest.TestCase):

  def setUp(self):
    pass

  def test1_(self):
    pass


def unittests():
  unittest.main()


def process():
  print get_default_facultadas_id_list()

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
        
if __name__ == '__main__':
  process()
