#!/usr/bin/env python
#-*-coding:utf-8-*-
'''

'''
import codecs, sys
import xml.etree.ElementTree as ET


from DisciplineMod import Discipline
from TurmaMod import Turma
from IniFimTupleMod import IniFimTuple
import timeutils
import SqlAlchemyModels as sqlm

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import __init__
import local_settings as ls
# engine = create_engine('sqlite:////' + ls.get_default_oferecidas_sqlite_file_abspath(), echo=True)

class Reader(object):
  '''
  <discipline code="IUF216">
    <name>História do Pensamento Jurídico</name>
    <is_elective>0</is_elective>
    <turma code="2342">
      <name>Hist. Dir. Pens. Jurídico (A)</name>
      <instructor>LUIZ EDUARDO DE VASCONCELLOS FIGUEIRA</instructor>
      <timetable>
        <time_session weekday="1">
          <time_start>14:50</time_start>
          <time_finish>16:30</time_finish>
        </time_session>
      </timetable>
    </turma>  
  '''
  def __init__(self):
    self.read()

  def read(self):
    oferecidas_xml_absfile = ls.get_default_oferecidas_xml_file_abspath()
    self.xml_tree = ET.parse(oferecidas_xml_absfile)
    root = self.xml_tree.getroot()
    for discipline_tag in root.iter('discipline'):
  
      code = discipline_tag.get('code')
      discipline = Discipline.get_discipline_from_store_or_create_and_store_it(code)
      discipline_name_tag = discipline_tag.find('name')
      if discipline_name_tag == None:
        continue 
      discipline.name = discipline_name_tag.text
      discipline_is_elective_tag = discipline_tag.find('is_elective')
      discipline.is_elective = False 
      if discipline_is_elective_tag.text == '1':
        discipline.is_elective = True
      turmas_tag = discipline_tag.iter('turma')
      for turma_tag in turmas_tag:
        turma_code = turma_tag.get('code')
        turma = Turma(turma_code)
        discipline.add_turma(turma)
        #turma = discipline.get_current_turma()
        turma_name_tag = turma_tag.find('name')
        turma.number_or_letter = turma_name_tag.text  
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
          if time_start==None or time_finish==None:
            raise ValueError, 'Dates are missing. In reading %s : time_start=%s and time_finish=%s' %(oferecidas_xml_absfile, str(time_start), str(time_finish))
          turma.timetable[weekday] = IniFimTuple.generate_instance_from_start_and_finish_times(time_start, time_finish)    


  def write_disciplines_to_a_file(self):
    outfile = codecs.open('z-see2.txt', 'w', 'utf-8')
    disciplines = Discipline.get_all_stored_disciplines()
    for discipline in disciplines:
      turmas = discipline.get_turmas()
      for turma in turmas:
        weekdays_inifimpairs = turma.timetable.values()
        for inifimpairs in weekdays_inifimpairs:
          for inifimtuple in inifimpairs:
            if inifimtuple.is_label_time_within('n1'):
              line = unicode(discipline) + '\n'
              outfile.write(line)
    outfile.close()
    
  def write_disciplines_to_db(self):
    seq = 0
    Session = sessionmaker()
    engine = create_engine('sqlite:////' + ls.get_default_oferecidas_sqlite_file_abspath(), echo=True)
    Session.configure(bind=engine)
    session = Session()
    disciplines = Discipline.get_all_stored_disciplines()
    for discipline in disciplines:
      if discipline.code == None or len(discipline.code) != 6:
        continue
      if discipline.name == None or discipline.name == '':
        continue
      db_discipline = sqlm.Discipline()
      db_discipline.id = discipline.code
      db_discipline.name = discipline.name
      print u'Adding db_discipline', unicode(db_discipline) 
      session.add(db_discipline)
      turmas = discipline.get_turmas()
      for turma in turmas:
        db_turma = sqlm.Turma()
        db_turma.id = turma.code
        db_turma.instructor = turma.instructor
        db_turma.name = turma.number_or_letter
        db_turma.discipline_id = discipline.code
        # db_turma.discipline = db_discipline
        print u'Adding db_turma', unicode(db_turma) 
        session.add(db_turma)
        weekdays = turma.timetable.keys()
        for weekday in weekdays:
          db_turmatempo = sqlm.TurmaTempo()
          seq += 1
          db_turmatempo.id = seq
          db_turmatempo.weekday = weekday
          for inifimtuple in turma.timetable[weekday]:
            db_turmatempo.ini_index = inifimtuple[0]
            db_turmatempo.fim_index = inifimtuple[1]
            db_turmatempo.turma_id = turma.code
            #db_turmatempo.turma = db_turma
            print u'Adding db_turmatempo', unicode(db_turmatempo) 
            session.add(db_turmatempo)
    session.commit()
    session.close_all()

import unittest
class TestCase1(unittest.TestCase):

  def setUp(self):
    pass

  def test1_(self):
    pass


def unittests():
  unittest.main()


def process():
  r = Reader()
  r.write_disciplines_to_db()

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
        
if __name__ == '__main__':
  process()
