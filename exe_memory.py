import pprint

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
    key1 = dir_v/1000
    key2 = dir_v%1000
    self.directions[key1][key2] = value

  def add_dir_to_dir(self, dir_from, dir_to):
    keyfrom1 = dir_from/1000
    keyfrom2 = dir_from%1000
    keyto1 = dir_to/1000
    keyto2 = dir_to%1000
    self.directions[keyto1][keyto2] = self.directions[keyfrom1][keyfrom2];

  def get(self, dir_v):
    key1 = dir_v/1000
    key2 = dir_v%1000
    # print(dir_v)
    # print(key1)
    # print(key2)
    # pprint.pprint(self.directions)
    # print(self.directions[key1][key2])
    return self.directions[key1][key2]

  def search(self, value, dir):
    # pprint.pprint(self.directions)
    for key, value_to in self.directions[dir].items():
      if value == value_to:
        return dir*1000+int(key)
    return None