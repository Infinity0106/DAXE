import pprint
import re

class DaxeMEM:
  def __init__(self):
    self.directions = {
      1:{},# Global Int
      2:{},# Global Decimal
      3:{},# Global Temporal Int
      4:{},# Global Temporal Decimal
      5:{},# Constant Int
      6:{},# Constant Decimal
      7:{},# Constant String
      8:{},# Local Int
      9:{},# Local Decimal
      10:{},# Temporal Int
      11:{},# Temporal Decimal
      12:{}# Temporal Bool
    }

  def add(self, value, dir_v):
    if isinstance(dir_v, str):
      dir_str = re.findall('\d+|$', dir_v)[0]
      dir_int = int(dir_str)
      dir_v = self.get(dir_int)
    key1 = dir_v/1000
    key2 = dir_v%1000
    self.directions[key1][key2] = value

  def add_dir_to_dir(self, dir_from, dir_to):
    try:
      keyfrom1 = dir_from/1000
      keyfrom2 = dir_from%1000
      keyto1 = dir_to/1000
      keyto2 = dir_to%1000
      self.directions[keyto1][keyto2] = self.directions[keyfrom1][keyfrom2];
    except KeyError:
      raise Exception("Uninitialized variable")

  def get(self, dir_v):
    try:
      if isinstance(dir_v, str):
        dir_str = re.findall('\d+|$', dir_v)[0]
        dir_int = int(dir_str)
        dir_v = self.get(dir_int)
      key1 = dir_v/1000
      key2 = dir_v%1000
      # pprint.pprint(self.directions)
      # print(self.directions[key1][key2])
      return self.directions[key1][key2]
    except KeyError:
      raise Exception("Uninitialized variable")

  def search(self, value, dir):
    # pprint.pprint(self.directions)
    for key, value_to in self.directions[dir].items():
      if value == value_to:
        return dir*1000+int(key)
    return None