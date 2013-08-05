#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Tests with Queries
'''
#import codecs
import os

#import __init__
#import local_settings as ls
# from TextDataScraperMod import TextDataScraper
from DisciplinesMod import Disciplines 
from DisciplineMod import Discipline 

import sys

lambda_UPPER = lambda x : x.upper()
class Query(object):
  def __init__(self):
    self.disciplines = Disciplines()
    self.disciplines.read_disciplines_from_xml()
    
  def list_by_timetable(self):
    weekday = None
    index = 2
    if 'weekday' in sys.argv:
      index = sys.argv.index('weekday')
      index = index + 1
      weekday = int(sys.argv[index])
      index = index + 1
    print 'weekday', weekday
    time_labels = sys.argv[index:]
    time_labels = map(lambda_UPPER, time_labels)
    print 'time_labels', time_labels
    #self.disciplines.search_by_time_labels(time_labels, weekday)
    #discipline = Discipline.get_discipline_from_store_or_None('IUF525')
    for discipline in self.disciplines.get_all_disciplines():
      if not discipline.is_it_allowed_to_course():
        continue
      if discipline.is_it_coursed_already():
        continue
      for turma in discipline.get_turmas():
        #print 'turma', turma.name, turma.timetable.show_timetable_in_1_line(), turma.timetable.show_timelabels_in_1_line()
        if turma.does_turma_happen_at_time_labels(weekday, time_labels):
          eletiva_msg = ''
          if discipline.is_elective:
            eletiva_msg = '(elet.)'
          print discipline.code, turma.name, eletiva_msg, turma.timetable.show_timetable_in_1_line(), turma.instructor
  
    
def dispatch_for_commands():
  if 'times' in sys.argv:
    query = Query()
    query.list_by_timetable()
   
def print_help_and_exit():
  print '''
  Usage:
  query.py times [weekday <weekdaynumber>] <label_1> <label_2> ... <label_n>
  '''
  sys.exit(0)
      
def process():
  if 'help' in sys.argv:
    print_help_and_exit()
  #sys.argv += ['times', 'weekday', '3', 'm5', 't1']
  dispatch_for_commands()
  
if __name__ == '__main__':
  process()
