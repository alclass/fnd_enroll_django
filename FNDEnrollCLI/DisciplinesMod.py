#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Created on 4 août 2013

@author: friend
'''

import xml.etree.ElementTree as ET

import codecs
import os
import timeutils
from DisciplineMod import Discipline

import __init__
import local_settings as ls

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
    

class Disciplines(object):

  def __init__(self):
    self.read_disciplines_from_xml_has_run = False
    self.xml_tree = None
  
  def get_all_disciplines(self):
    if self.read_disciplines_from_xml_has_run:
      return Discipline.get_all_stored_disciplines()
    self.read_disciplines_from_xml()
    return Discipline.get_all_stored_disciplines()
    
  def read_disciplines_from_xml(self):
    xml_file = ls.get_default_oferecidas_xml_file_abspath()
    self.xml_tree = ET.parse(xml_file)
    root = self.xml_tree.getroot()
    for discipline_tag in root.iter('discipline'):
      code = discipline_tag.get('code')
      discipline = Discipline.get_discipline_from_store_or_create_and_store_it(code)
      discipline_name_tag = discipline_tag.find('name')
      discipline.name = discipline_name_tag.text
      discipline_is_elective_tag = discipline_tag.find('is_elective')
      discipline.is_elective = False 
      if discipline_is_elective_tag.text == '1':
        discipline.is_elective = True
      turmas_tag = discipline_tag.iter('turma')
      for turma_tag in turmas_tag:
        turma_code = turma_tag.get('code')
        discipline.add_new_turma(turma_code)
        turma = discipline.get_current_turma()
        turma_name_tag = turma_tag.find('name')
        turma.name = turma_name_tag.text  
        instructor_tag = turma_tag.find('instructor')
        instructor = instructor_tag.text
        turma.instructor = instructor
        timetable_tag = turma_tag.find('timetable')
        for time_session_tag in timetable_tag.iter('time_session'):
          weekday = int(time_session_tag.get('weekday'))
          time_start_tag = time_session_tag.find('time_start')
          time_start_str = time_start_tag.text
          time_start = timeutils.get_time_from_str_time(time_start_str)
          time_finish_tag = time_session_tag.find('time_finish')
          time_finish_str = time_finish_tag.text
          time_finish = timeutils.get_time_from_str_time(time_finish_str)
          turma.timetable[weekday] = (time_start, time_finish)
      # self.disciplines.append(discipline) # no longer necessary, it's stored in the static dict in class Discipline
    
    self.read_disciplines_from_xml_has_run = True
            
  def find_by_weekday(self, weekday):
    turma_found_list = []
    disciplines = self.get_all_disciplines()
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

  def find_by_turma_code(self, turma_code):
    disciplines = self.get_all_disciplines()
    turma_found = None
    for discipline in disciplines:
      print 'disc:', discipline.code, discipline.turmas_dict.keys()
      if turma_code in discipline.turmas_dict.keys():
        turma_found = discipline.turmas_dict[turma_code]
        break
    print 'Turma found:', turma_found
    print 'Total disciplines:', len(disciplines)

  def derive_discipline_name_by_turmas(self):
    #for i, discipline in enumerate(self.disciplines):
    for discipline in self.get_all_disciplines():
      names = []
      for turma_code in discipline.turmas_dict.keys():
        turma = discipline.turmas_dict[turma_code]
        names.append(turma.name)
      discipline.name = names[0]
      #derived_name = derive_name_from_names(names)
      #new_name = clean_name_finishing_the_ending(derived_name)

  def write_text_disciplines_names(self):
    text_filename = 'disciplines_names.txt'
    text_abspath = os.path.join(ls.get_app_data_dir_abspath(), text_filename)
    text_file = codecs.open(text_abspath, 'w', 'utf-8')
    for discipline in self.get_all_disciplines():
      line = '%s  %s\n' %(discipline.code, discipline.name)
      text_file.write(line)
    text_file.close()

  def load_discipline_names_if_possible(self):
    # need to get disciplines from the static dict in class Discipline
    # _ = self.get_all_disciplines() # to guarantee the XML read has run
    text_filename = 'disciplines_names.manually-worked.txt'
    text_abspath = os.path.join(ls.get_app_data_dir_abspath(), text_filename)
    text_file = codecs.open(text_abspath, 'r', 'utf-8')
    for line in text_file.readlines():
      try:
        code = line[:6]
        name = line[8:-1] # -1 for the \n
        try:
          discipline = Discipline.instance_store_dict[code]
          discipline.name = name
        except KeyError:
          continue
      except IndexError:
        continue

  def read_text_file_and_set_discipline_names(self):
    self.load_discipline_names_if_possible()
    root = self.xml_tree.getroot()
    for discipline_tag in root.iter('discipline'):
      code = discipline_tag.get('code')
      discipline = Discipline.instance_store_dict[code]
      name_tag = discipline_tag.find('name')
      if name_tag == None:
        name_tag = ET.SubElement(discipline_tag, 'name')
        name_tag.text = discipline.name
    xml_abspath = ls.get_default_oferecidas_xml_file_abspath()
    print 'Saving', xml_abspath
    self.xml_tree.write(xml_abspath)    
    
  def write_xml_disciplines_names(self):
    root = ET.Element("disciplines_names")
    for i, discipline in enumerate(self.disciplines):
      print i+1, discipline.code, discipline.name
      discipline_tag = ET.SubElement(root, 'discipline', attrib={'code':discipline.code} )
      discipline_tag.text = discipline.name
    xml_abspath = ls.get_default_xml_disciplinas_sem_turmas_abspath()
    print 'Writing XML as', xml_abspath
    tree = ET.ElementTree(root) 
    tree.write(xml_abspath)
     
  def size(self):
    return len(self.disciplines)

def process():
  disciplines = Disciplines()
  #print 'Reading disciplines from XML'
  #disciplines.read_disciplines_from_xml()
  #print 'There are %s disciplines' %disciplines.size()
  #disciplines.derive_discipline_name_by_turmas()
  #disciplines.write_text_disciplines_names()
  #disciplines.write_xml_disciplines_names()
  disciplines.read_text_file_and_set_discipline_names()
        
if __name__ == '__main__':
  process()
