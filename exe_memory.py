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

  def get(self, dir_v):
    key1 = dir_v/1000
    key2 = dir_v%1000
    # print(dir_v)
    # print(key1)
    # print(key2)
    # print(self.directions[key1][key2])
    return self.directions[key1][key2]

