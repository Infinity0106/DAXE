from custom_stack import Stack
from semantic_cube import SemanticCube
from lark import Token
from key_actions import KeyActions

class Quadruplets:
  def __init__(self):
    self.records=[]
    self.num_aviables=0
    self.operators = Stack() #Poper
    self.types = Stack()
    self.operands = Stack() #PilaO
    self.semantic_cube = SemanticCube()
    self.key_actions = KeyActions().table

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
      result_type = self.semantic_cube.cube[left_type][right_type][operator]
      if result_type == "ERROR":
        raise Exception("Type mismatch trying to assign (type: %s) to %s (type: %s), at: %s:%s"%(right_type, left_operand, left_type, left_operand.line, left_operand.column))
      else:
        self.num_aviables+=1
        result_name = Token("T_TMP_ID", 'tmp'+str(len(self.records)))
        self.gen_quad(operator, left_operand.value, right_operand.value, result_name.value)
        if operator != "=":
          self.operands.push(result_name)
          self.types.push(result_type)

  def gen_custom_quad(self, type):
    result_name = self.operands.pop()
    self.gen_quad(type, None, None, result_name.value)

  def gen_quad(self, op, lop, rop, res):
    if op == "=":
      self.records.append([op,rop,None,lop])
      # self.records.append([self.key_actions[op],rop,None,lop])
    else:
      self.records.append([op,lop,rop,res])
      # self.records.append([self.key_actions[op],lop,rop,res])
    print(self.records)
