#!/usr/bin/env python
#-*-coding:utf-8-*-
'''

TextDataScraperMod.py

This class was designed/implemented because the UFRJ's HTML data source was, unfortunately, ill-formed.

How the data source TEXT is formed:
In a browser, Selecting All, copying and pasting the text has been a Plan-B solution (at least for the time being).

The text result of this Copy&Paste should look like the following:

L1 IUE514
L2  
L3 5866
L4  DIR. EMPRESA RELAÇÕES DE TRABALHO   
L5 Qui
L6  
L7 16:40 às 18:20
L8  IVAN SIMOES GARCIA

Class TextDataScraper scrapes these 8 lines (L1 to L8 above) and saves all "turmas" in an XML file.
This XML file is read later on and modeled by class Discipline.
A list of Disciplines is used to help search and query disciplines and times (see query.py). 
'''

import codecs
import sys
import xml.etree.ElementTree as ET

import __init__
import local_settings as ls
import timeutils
#from timeutils import K

from DisciplineMod import Discipline
from DisciplinesMod import Disciplines
from TurmaMod import Turma
#from IniFimTupleMod import IniFimTuple

import string
UPPERCASE_26_LETTERS = string.letters[26:]
lambda_each_uppercase = lambda x : x in UPPERCASE_26_LETTERS    
def is_line_discipline_id(line):
  '''
  The first 3 chars are always UPPERCASE letters
  The last 3 may follow the two combinations:
    2.1) either it's a 3-number string
    2.2) or it has an UPPERCASE letter followed by 2 numbers
    
  Examples:
  IUF351 = FILOSOFIA DO DIREITO I
  IUWK11 = MONOGRAFIA JURÍDICA I 
  '''
  if len(line) != 6:
    return False
  letters = line[:3]
  result_bool_list = map(lambda_each_uppercase, letters)
  if False in result_bool_list:
    return False
  str_numbers = line[4:]
  try:
    int(str_numbers)
    return True
  except ValueError:
    pass
  str_letter_or_number = line[3]
  if str_letter_or_number in UPPERCASE_26_LETTERS:
    return True
  try:
    int(str_letter_or_number)
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
    
    IS_ELECTIVE = False
    
    data_file = codecs.open(self.txtfile_abspath, 'r', encoding='utf-8')
    lines = data_file.readlines()
    next_is_instructor      = False
    next_is_discipline_name = False
    keep_ahead_weekday = None
    discipline = None
 
    self.turmas_code = []

    for _, line in enumerate(lines):
      line = line.lstrip(' \t').rstrip(' \t\r\n')
      if line == '':
        continue
      if is_line_discipline_id(line):
        code = line
        if code == 'IUE514':
          IS_ELECTIVE = True
        discipline = Discipline.get_discipline_from_store_or_create_and_store_it(code)
        discipline.is_elective = IS_ELECTIVE 
        continue        
      if is_line_turma_ie_a_number(line):
        turma_code = int(line)
        turma = Turma(turma_code)
        discipline.add_turma(turma)
        #discipline.current_turma.code = turma_code_number 
        self.turmas_code.append(turma_code)
        next_is_discipline_name = True
        continue
      if line in timeutils.dict_pt_3_letter_weekday.values():
        keep_ahead_weekday = timeutils.get_weekday_from_weekday3l(line) 
        continue
      if next_is_discipline_name:
        turma_version_of_discipline_name = line
        discipline.get_current_turma().name = turma_version_of_discipline_name
        next_is_discipline_name = False
        continue
      time_range = return_time_range_from_str_from_to_time_or_None(line)
      print u'**** time_range %s' %discipline, '+++time_range', time_range, '++++line', line
      if time_range != None and keep_ahead_weekday != None:
        time_start, time_finish = time_range
        has_been_added = discipline.get_current_turma().add_timetable_element_with_pytimes(keep_ahead_weekday, time_start, time_finish)
        if not has_been_added:
          print time_range, 'has not been added.' 
        keep_ahead_weekday = None
        next_is_instructor = True
        continue
      if next_is_instructor:
        instructor_name = line
        discipline.get_current_turma().instructor = instructor_name
        next_is_instructor = False

    self.has_read_data_run = True

  def fill_in_discipline_names_if_possible(self):
    disciplines = Disciplines()
    disciplines.load_discipline_names_if_possible()

  def transform_into_xml(self):
    '''
    '''
    self.fill_in_discipline_names_if_possible()
    disciplines = self.get_all_scraped_disciplines()
    root = ET.Element("disciplines")
    for discipline in disciplines:
      discipline_tag = ET.SubElement(root, 'discipline', attrib={'code':discipline.code} )
      try: 
        discipline_name = discipline.name
        name_tag = ET.SubElement(discipline_tag, 'name')
        name_tag.text = discipline_name
        is_elective = 0
        if discipline.is_elective:
          is_elective = 1
        is_elective_tag = ET.SubElement(discipline_tag, 'is_elective')
        is_elective_tag.text = str(is_elective)
      except AttributeError:
        pass 
      turma_codes = discipline.turmas_dict.keys()
      turma_codes.sort()
      for turma_code in turma_codes:
        turma = discipline.turmas_dict[turma_code]
        turma_tag = ET.SubElement(discipline_tag, 'turma', attrib={'code':str(turma.code)} )
        turma_name_tag = ET.SubElement(turma_tag, 'name')
        turma_name_tag.text = turma.name
        instructor_tag = ET.SubElement(turma_tag, 'instructor')
        instructor_tag.text = turma.instructor
        weekdays = turma.timetable.keys()
        if len(weekdays) > 0:
          timetable_tag =  ET.SubElement(turma_tag, 'timetable')
          weekdays.sort()
          for weekday in weekdays:
            ini_fim_pairs = turma.timetable[weekday]
            for ini_fim_tuple in ini_fim_pairs:
              ini_str_time, fim_str_time = ini_fim_tuple.as_str_hour_min_time_range()
              time_session_tag = ET.SubElement(timetable_tag, 'time_session', attrib={'weekday':str(weekday)} )
              time_start_tag = ET.SubElement(time_session_tag, 'time_start')
              time_start_tag.text = ini_str_time 
              time_finish_tag = ET.SubElement(time_session_tag, 'time_finish')
              time_finish_tag.text = fim_str_time
            
    # wrap it in an ElementTree instance, and save as XML
    tree = ET.ElementTree(root)
    #app_data_dir_abspath = ls.get_app_data_dir_abspath()
    #xml_filename = 'disciplines.xml'
    xml_abspath = ls.get_default_oferecidas_xml_file_abspath() # os.path.join(app_data_dir_abspath, xml_filename)
    print 'Writing XML as', xml_abspath 
    tree.write(xml_abspath)
     

     
def find_by_weekday(data_obj):
  for weekday in xrange(7):
    disciplines = data_obj.find_by_weekday(weekday)
    if disciplines == []:
      continue 
    print 'weekday = ', weekday
    for discipline in disciplines:
      print discipline._id, discipline.name 
    

import unittest

class TestCase(unittest.TestCase):
  
  def test_1(self):
    pass



def unittests():
  unittest.main()


def process():
  data_obj = TextDataScraper()
  data_obj.read_data()
  #data_obj.list_disciplines()
  # find_by_weekday(data_obj)

  data_obj.transform_into_xml()
  counter = 0
  for discipline in data_obj.get_all_scraped_disciplines():
    counter += 1
    print counter, discipline.code 
  '''
  data_obj.find_by_turma_code(1520)
  data_obj.turmas_code.sort()
  print data_obj.turmas_code
  '''

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()
  process()
