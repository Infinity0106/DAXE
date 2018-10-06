import Queue as queue

class Quadruplets:
  def __init__(self):
    self.records=[]
    self.operators = queue.LifoQueue()
    self.operands = queue.LifoQueue()

