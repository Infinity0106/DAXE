from custom_stack import Stack
from semantic_cube import SemanticCube

class Quadruplets:
  def __init__(self):
    self.records=[]
    self.num_aviables=0
    self.operators = Stack() #Poper
    self.types = Stack()
    self.operands = Stack() #PilaO
    self.semantic_cube = SemanticCube()

  def add_id(self, name, type):
    self.types.push(type)
    self.operands.push(name)

  def add_operator(self, item):
    self.operators.push(item)

  def pop_operator(self):
    self.operators.pop()

  def algorithm_with(self, labels):
    operator = self.operators.top()
    if operator in labels:
      right_operand = self.operands.pop()
      right_type = self.types.pop()
      left_operand = self.operands.pop()
      left_type = self.types.pop()
      operator = self.operators.pop()
      print(left_type)
      print(right_type)
      print(operator)
      result_type = self.semantic_cube.cube[left_type][right_type][operator]
      if result_type == "ERROR":
        raise Exception("Type mismatch")
      else:
        self.num_aviables+=1
        result_name = 'tmp'+str(len(self.records))
        self.gen_quad(operator, left_operand, right_operand, result_name)
        self.operands.push(result_name)
        self.types.push(result_type)
    print(self.records)
    print(self.operands.stack)
    print(self.types.stack)
    print(self.operators.stack)

  def gen_quad(self, op, lop, rop, res):
    self.records.append([op,lop,rop,res])
