# -*- coding: utf-8 -*-
# local_settings.py
'''
timeutils.py

'''


from datetime import time
import datetime

dict_pt_3_letter_weekday = {0:'Seg',1:'Ter',2:'Qua',3:'Qui',4:'Sex', 5:'Sab',6:'Dom'}
map_labels_to_time_start_and_finish_strs = {
  'M1':(u'7:30', u'8:20'),
  'M2':(u'8:20', u'9:10'),
  'M3':(u'9:20', u'10:10'),
  'M4':(u'10:10', u'11:00'),
  'M5':(u'11:10', u'12:00'),
  'T1':(u'12:00', u'12:50'),
  'T2':(u'13:00', u'13:50'),
  'T3':(u'13:50', u'14:40'),
  'T4':(u'14:50', u'15:40'),
  'T5':(u'15:40', u'16:30'),
  'T6':(u'16:40', u'17:30'),
  'T7':(u'17:30', u'18:20'),
  'N1':(u'18:30', u'19:20'),
  'N2':(u'19:20', u'20:10'),
  'N3':(u'20:10', u'21:00'),
  'N4':(u'21:00', u'21:50'),
  'N5':(u'21:50', u'22:40'),
}  

map_labels_to_time_start_and_finish = {}
def form_map_labels_to_time_start_and_finish():
  for label in map_labels_to_time_start_and_finish_strs.keys():
    # tuple_start_and_finish_strs
    time_start_str = map_labels_to_time_start_and_finish_strs[label][0]
    str_hour_start, str_minute_start = time_start_str.split(':')
    time_finish_str = map_labels_to_time_start_and_finish_strs[label][1]
    str_hour_finish, str_minute_finish = time_finish_str.split(':')
    time_range = time(hour=int(str_hour_start), minute=int(str_minute_start)), time(hour=int(str_hour_finish), minute=int(str_minute_finish))  
    map_labels_to_time_start_and_finish[label] = time_range
form_map_labels_to_time_start_and_finish()

def is_time_range_a_tuple_of_times(time_range):
  if type(time_range) != tuple:
    return False
  try:    
    time_start = time_range[0]
    if type(time_start) != datetime.time:
      return False
    time_finish = time_range[1]
    if type(time_finish) != datetime.time:
      return False
    return True
  except IndexError:
    pass
  except TypeError: # time_range[0] may raise TypeError: 'datetime.time' object has no attribute '__getitem__'
    pass
  return False


f_index_find = lambda x, v: v == x[1]  
def get_weekday_from_weekday3l_impl2(weekday3l):
  items = dict_pt_3_letter_weekday.items()
  result = map(f_index_find(weekday3l), items)
  index = result.index(True)
  return items[index][0]

def get_weekday_from_weekday3l(weekday3l):
  items = dict_pt_3_letter_weekday.items()
  for item in items:
    if weekday3l == item[1]:
      return item[0]
  return None

def get_time_from_str_time(str_time):
  dtime = None
  try:
    pp = str_time.split(':')
    hour = int(pp[0])
    minute = int(pp[1])
    if len(pp) > 2:
      second = int(pp[2])
      dtime = time(hour=hour, minute=minute, second=second)
      return dtime
    dtime = time(hour=hour, minute=minute)
    return dtime
  except IndexError:
    pass
  except ValueError:
    pass
  return dtime

def get_time_labels_from_time_ranges(time_ranges):
  time_labels = []
  for time_range in time_ranges:
    print 'time_range', time_range 
    if not is_time_range_a_tuple_of_times(time_range):
      print 'FALSE', time_range
      print type(time_range)
      continue
    p_time_start = time_range[0] 
    p_time_finish = time_range[1] 
    for label in map_labels_to_time_start_and_finish.keys():
      time_start, time_finish = map_labels_to_time_start_and_finish[label]
      if p_time_start <= time_start < p_time_finish:
        if label not in time_labels: 
          time_labels.append(label)
      if p_time_start < time_finish <= p_time_finish:
        if label not in time_labels: 
          time_labels.append(label)
  return time_labels

def print_map_labels_to_time_start_and_finish():
  for label in map_labels_to_time_start_and_finish.keys():
    print label, map_labels_to_time_start_and_finish[label]

def test1():
  print map_labels_to_time_start_and_finish
  time_start = time(hour=7, minute=30)
  time_finish = time(hour=9, minute=30)
  time_range = (time_start, time_finish) 
  time_ranges = [time_range] 
  print get_time_labels_from_time_ranges(time_ranges)
  time_start = time(hour=18, minute=30)
  time_finish = time(hour=21, minute=0)
  time_range = (time_start, time_finish) 
  time_ranges.append(time_range) 
  print get_time_labels_from_time_ranges(time_ranges)
  
def process():
  test1()
  #print_map_labels_to_time_start_and_finish()  
        


import unittest

class TestCase(unittest.TestCase):
  
  def test_time_true_or_false(self):
    time_start = time(hour=7, minute=30)
    time_finish = time(hour=9, minute=10)
    time_range = (time_start, time_finish) 
    self.assertTrue(is_time_range_a_tuple_of_times(time_range))

  def test_type_time(self):
    time_start = time(hour=7, minute=30)
    self.assertEqual(type(time_start), time)
    time_finish = time(hour=9, minute=10)
    self.assertEqual(type(time_finish), time)


if __name__ == '__main__':
  process()
  # unittest.main()  