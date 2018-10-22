from custom_stack import Stack
from semantic_cube import SemanticCube
from lark import Token
from key_actions import KeyActions
import pprint

class Quadruplets:
  def __init__(self):
    self.records=[["GOTO",None,None,None]]
    self.num_aviables=0
    self.operators = Stack() #Poper
    self.types = Stack() #Ptypes
    self.operands = Stack() #PilaO
    self.jumps = Stack() #Pjumps
    self.semantic_cube = SemanticCube()
    self.key_actions = KeyActions().table
    self.jumps.push(0)
    self.parameter_count=0
    self.current_params_table= None
    self.actual_draw_action = None

  def current_quad(self):
    return len(self.records)

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

  def start_if(self, token):
    exp_type = self.types.pop()
    if exp_type != "booleano":
      raise Exception("Type mismatch trying to evaluate si at %s:%s"%(token.line,token.column))
    result = self.operands.pop()
    self.gen_quad("GOTOF", result.value, None, None)
    self.jumps.push(len(self.records)-1)

  def end_if(self):
    end = self.jumps.pop()
    self.fill_goto(end, len(self.records))

  def else_if(self):
    self.gen_quad("GOTO", None, None, None)
    false = self.jumps.pop()
    self.jumps.push(len(self.records)-1)
    self.fill_goto(false, len(self.records))

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
    pprint.pprint(self.records)
  
  def fill_goto(self, index, value):
    self.records[index][3] = value
    pprint.pprint(self.records)

  def while_start(self):
    self.jumps.push(len(self.records))

  def while_mid(self, token):
    exp_type = self.types.pop()
    if exp_type != "booleano":
      raise Exception("Type mismatch trying to evaluate si at %s:%s"%(token.line,token.column))
    result = self.operands.pop()
    self.gen_quad("GOTOF", result.value, None, None)
    self.jumps.push(len(self.records)-1)


  def while_end(self):
    end = self.jumps.pop()
    retornar = self.jumps.pop()
    self.gen_quad("GOTO", None, None, retornar)
    self.fill_goto(end, len(self.records))

  def gen_era(self, name, params_table):
    self.gen_quad("ERA", None, None, name)
    self.parameter_count = 0
    self.current_params_table = params_table

  def gen_parameter(self):
    argument = self.operands.pop()
    argument_type = self.types.pop()
    try:
      key, value = self.current_params_table.items()[self.parameter_count]
    except IndexError:
      raise Exception("Function not declared with the same parameter size at %s:%s"%(argument.line, argument.column))
    result_type = self.semantic_cube.cube[argument_type][value["type"]]["="]
    if result_type == "ERROR":
      raise Exception("Type mismatch trying to assign (type: %s) to parameter %s (type: %s), at: %s:%s"%(argument_type, argument.value, value['type'], argument.line, argument.column))
    self.gen_quad("PARAM",argument.value,None,"param"+str(self.parameter_count))

  def more_params(self):
    self.parameter_count+=1

  def verify_params_len(self, token):
    if self.parameter_count+1 != len(self.current_params_table):
      raise Exception("Function not declared with the same parameter size at %s:%s"%(token.line, token.column))

  def draw_era_sub(self, name):
    self.gen_quad(name, None, None, None)
    self.parameter_count = 0

  def draw_params(self):
    argument = self.operands.pop()
    argument_type = self.types.pop()
    result_type = self.semantic_cube.cube[argument_type]["decimal"]["="]
    result_type_2 = self.semantic_cube.cube[argument_type]["entero"]["="]
    if result_type == "ERROR" and result_type_2 == "ERROR":
      raise Exception("Type mismatch trying to assign (type: %s) to parameter %s (type: %s), at: %s:%s"%(argument_type, argument.value, "decimal", argument.line, argument.column))
    self.gen_quad("PARAM",argument.value,None,"param"+str(self.parameter_count))

  def gen_draw_quad(self, value):
    self.gen_quad("PARAM",value,None,"param"+str(self.parameter_count))

  def fill_main(self):
    end = self.jumps.pop()
    self.fill_goto(end, len(self.records))