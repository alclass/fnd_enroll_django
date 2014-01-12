#!/usr/bin/env python
#-*-coding:utf-8-*-
'''

'''
import sys


import DisciplineMod
import TurmaMod
from IniFimTupleMod import IniFimTuple
import timeutils

import __init__
import local_settings as ls

from sqlalchemy import create_engine
engine = create_engine('sqlite:////' + ls.get_default_oferecidas_sqlite_file_abspath(), echo=True)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref 

from sqlalchemy import Column, Integer, String, Boolean
class Discipline(Base):
  __tablename__ = 'disciplines'

  id = Column(String(6), primary_key=True)
  name = Column(String)
  is_coursed    = Column(Boolean)
  is_elective   = Column(Boolean)
  is_prereq_ok  = Column(Boolean)
  

  def __repr__(self):
    return "<DisciplineDB(id='%s', name='%s')>" % (self.id, self.name)

class Turma(Base):
  __tablename__ = 'turmas'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  instructor =  Column(String)
  sala = Column(Integer)
  discipline_id = Column(String(6), ForeignKey('disciplines.id'))
  discipline    = relationship('Discipline', backref=backref('turmas', order_by=id))

  def __repr__(self):
    return "<Turma(id='%s', name='%s', disc.='%s')>" % (self.id, self.name, self.discipline_id)
  
class TurmaTempo(Base):
  __tablename__ = 'turmatempos'
  
  id = Column(Integer, primary_key=True) 
  weekday = Column(Integer)
  ini_index = Column(Integer)
  fim_index = Column(Integer)
  turma_id = Column(Integer, ForeignKey('turmas.id'))
  turma    = relationship('Turma', backref=backref('turmatempos', order_by=id))

  def __repr__(self):
    return "<TurmaTempo(weekday=%d, ini=%d, fim=%d)>" % (self.weekday, self.ini_index, self.fim_index)


import unittest
class TestCase1(unittest.TestCase):

  def setUp(self):
    pass

  def test1_(self):
    pass


def unittests():
  unittest.main()


def process():
  print 'Base.metadata.create_all(engine)'
  Base.metadata.create_all(engine)
  pass

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
        
if __name__ == '__main__':
  process()
