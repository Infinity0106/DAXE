import Queue as queue

class Quadruplets:
  def __init__(self):
    self.records=[]
    self.operators = queue.LifoQueue()
    self.types = queue.LifoQueue()
    self.operands = queue.LifoQueue()
  
  def add_variable(self, var):
    print(var)
