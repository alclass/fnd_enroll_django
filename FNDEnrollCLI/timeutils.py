#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
timeutils.py

'''


from datetime import time
import datetime

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

dict_pt_3_letter_weekday = {0:'Seg',1:'Ter',2:'Qua',3:'Qui',4:'Sex', 5:'Sab',6:'Dom'}
labels_contiguity = ['M1','M2','M3','M4','M5','T1','T2','T3','T4','T5','T6','T7','N1','N2','N3','N4','N5']
def put_time_labels_in_order(p_time_labels):
  '''
  Because N is before T alphabetically, the sorting process is done 2-stepfully
  ie, first we sort from M1 to T7, then, secondly, we sort from N1 to N5
  Thirdly and last, we concatenate the two 
  '''
  labels_manha_and_tarde = labels_contiguity[:12] # 12 is 5 + 7, ie, M1 to M5 plus T1 to T7
  p_labels_manha_and_tarde = []
  p_labels_noite = []  
  for time_label in p_time_labels:
    if time_label in labels_manha_and_tarde:
      p_labels_manha_and_tarde.append(time_label)
    else:
      p_labels_noite.append(time_label)
  p_labels_manha_and_tarde.sort()
  p_labels_noite.sort()
  return p_labels_manha_and_tarde + p_labels_noite 

LABEL_SMALLER = -1
LABEL_EQUAL   =  0
LABEL_GREATER =  1
def compare_2_time_labels_less_equal_greater(label1, label2):
  if label1 not in labels_contiguity:
    return None 
  if label2 not in labels_contiguity:
    return None 
  index1 = labels_contiguity.index(label1)
  index2 = labels_contiguity.index(label2)
  if index1 < index2:
    return LABEL_SMALLER
  if index1 == index2:
    return LABEL_EQUAL
  return LABEL_GREATER
  
def minus_one(time_label):
  if time_label not in labels_contiguity:
    return None
  index = labels_contiguity.index(time_label)
  if index == 0:
    return None
  return labels_contiguity[index-1]
    
def plus_one(time_label):
  if time_label not in labels_contiguity:
    return None
  index = labels_contiguity.index(time_label)
  if index == len(labels_contiguity) - 1:
    return None
  return labels_contiguity[index+1]

   
  
  

class K:
  MONDAY    = 0
  TUESDAY   = 1
  WEDNESDAY = 2
  THURSDAY  = 3
  FRIDAY    = 4
  SATURDAY  = 5
  SUNDAY    = 6
  M1 = 'M1'; M2 = 'M2'; M3 = 'M3'; M4 = 'M4'; M5 = 'M5'
  T1 = 'T1'; T2 = 'T2'; T3 = 'T3'; T4 = 'T4'; T5 = 'T5'; T6 = 'T6'; T7 = 'T7'
  N1 = 'N1'; N2 = 'N2'; N3 = 'N3'; N4 = 'N4'; N5 = 'N5'

  @staticmethod
  def validate_label_or_raise(time_label):
    if time_label not in labels_contiguity:
      raise ValueError, 'time_label (=%s) not in labels_contiguity (=%s)' %(time_label, str(labels_contiguity))

  @staticmethod
  def get_time_range_from_time_labels(label_start, label_finish):
    K.validate_label_or_raise(label_start)
    K.validate_label_or_raise(label_finish)
    p_time_labels = label_start, label_finish
    p_time_labels = put_time_labels_in_order(p_time_labels)
    time_range_start = map_labels_to_time_start_and_finish[p_time_labels[0]]
    time_range_finish = map_labels_to_time_start_and_finish[p_time_labels[1]]
    return time_range_start, time_range_finish 


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

def get_str_hour_minute_from_pytime(pytime):
  if type(pytime) != datetime.time:
    return None
  return '%02d:%02d' %(pytime.hour, pytime.minute)

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
    #print 'time_range', time_range 
    if not is_time_range_a_tuple_of_times(time_range):
      #print 'FALSE', time_range
      #print type(time_range)
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
  time_labels = put_time_labels_in_order(time_labels)
  return time_labels

def print_map_labels_to_time_start_and_finish():
  for label in map_labels_to_time_start_and_finish.keys():
    print label, map_labels_to_time_start_and_finish[label]

def convert_contiguous_time_labels_to_a_time_start_and_finish_tuple(contiguous_time_labels):
  resulting_time_start  = None
  resulting_time_finish = None 
  for time_label in contiguous_time_labels:
    try:
      time_start, time_finish = map_labels_to_time_start_and_finish[time_label]
      if resulting_time_start == None or time_start < resulting_time_start:
        resulting_time_start = time_start
      if resulting_time_finish == None or time_finish > resulting_time_finish:
        resulting_time_finish = time_finish
    except KeyError:
      continue
  return (resulting_time_start, resulting_time_finish) 

def convert_time_labels_to_time_ranges(time_labels):
  time_ranges = []
  for time_label in time_labels:
    try:
      time_start, time_finish = map_labels_to_time_start_and_finish[time_label]
      time_range = time_start, time_finish
      time_ranges.append(time_range)
    except KeyError:
      continue
  return time_ranges

def convert_time_ranges_to_time_labels(time_ranges):
  time_labels = []
  all_time_ranges = map_labels_to_time_start_and_finish.items()
  all_labels, all_time_ranges = zip(*all_time_ranges)
  all_time_starts, all_time_finishes = zip(*all_time_ranges)
  all_time_starts = list(all_time_starts)
  #all_time_starts.sort()
  all_time_finishes = list(all_time_finishes)
  #all_time_finishes.sort()
  #print all_time_starts
  #print all_time_finishes
  for time_range in time_ranges:
    time_start  = time_range[0]
    time_finish = time_range[1]
    try:
      index = all_time_starts.index(time_start)
      label_start = all_labels[index]
      time_labels.append(label_start)
      #print 'label_start', label_start 
      #print 'time_finish', time_finish
      index = all_time_finishes.index(time_finish)
      label_finish = all_labels[index]
      time_labels.append(label_finish)
      #print 'label_finish', label_finish 
      #index_finish = labels_contiguity.index(label_finish)
      #index_start  = labels_contiguity.index(label_start)
      #time_labels = labels_contiguity[index_start : index_finish + 1]
      #return time_labels
    except ValueError:
      pass
  time_labels = list(set(time_labels))
  time_labels = put_time_labels_in_order(time_labels)
  return time_labels
      

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
  
def test2():
  time_ranges = []
  time_range = map_labels_to_time_start_and_finish['T1']
  print 'T1 time_range', time_range
  time_ranges.append(time_range)
  time_range = map_labels_to_time_start_and_finish['T2']
  print 'T2 time_range', time_range
  time_ranges.append(time_range)
  print convert_time_ranges_to_time_labels(time_ranges)
  
  
def process():
  #test1()
  test2()
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
  