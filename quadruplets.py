from custom_stack import Stack
from semantic_cube import SemanticCube
from lark import Token
from key_actions import KeyActions
import pprint

class Quadruplets:
  def __init__(self):
    self.records=[["GOTO",None,None,None]]
    self.num_aviables=0
    self.tmp_int = 10000
    self.tmp_decimal = 11000
    self.tmp_bool = 12000
    self.cte_int = 5000
    self.cte_decimal = 6000
    self.glo_tmp_int = 3000
    self.glo_tmp_decimal = 4000
    self.operators = Stack() #Poper
    self.types = Stack() #Ptypes
    self.operands = Stack() #PilaO
    self.jumps = Stack() #Pjumps
    self.semantic_cube = SemanticCube()
    self.key_actions = KeyActions().table
    self.jumps.push(0)
    self.parameter_count=Stack()
    self.current_params_table= None
    self.actual_draw_action = None
    self.fun_dir = None
    self.dir_tmp ={}

  def link_fun_dir(self, fun):
    self.fun_dir = fun

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
        result_name = Token("T_TMP_ID", 'tmp_'+str(result_type)+'_'+str(self.num_aviables))
        # print(result_name.value)
        left = self.token_to_dir(left_operand)
        right = self.token_to_dir(right_operand)
        result = self.token_to_dir(result_name)
        self.gen_quad(operator, left, right, result)
        # self.gen_quad(operator, left_operand.value, right_operand.value, result_name.value)
        if operator != "=":
          self.operands.push(result_name)
          self.types.push(result_type)

  def start_if(self, token):
    exp_type = self.types.pop()
    if exp_type != "booleano":
      raise Exception("Type mismatch trying to evaluate si at %s:%s"%(token.line,token.column))
    result = self.operands.pop()
    value = self.token_to_dir(result)
    self.gen_quad("GOTOF", value, None, None)
    # result = self.operands.pop()
    # self.gen_quad("GOTOF", result.value, None, None)
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
    result = self.token_to_dir(result_name)
    self.gen_quad(type, None, None, result)

  def gen_quad(self, op, lop, rop, res):
    if op == "=":
      self.records.append([op,rop,None,lop])
      # self.records.append([self.key_actions[op],rop,None,lop])
    else:
      self.records.append([op,lop,rop,res])
      # self.records.append([self.key_actions[op],lop,rop,res])
    # pprint.pprint(self.records[-1])
    # pprint.pprint(self.operands.stack)
    # pprint.pprint(self.operators.stack)
  
  def fill_goto(self, index, value):
    self.records[index][3] = value
    # pprint.pprint(self.records)

  def while_start(self):
    self.jumps.push(len(self.records))

  def while_mid(self, token):
    exp_type = self.types.pop()
    if exp_type != "booleano":
      raise Exception("Type mismatch trying to evaluate si at %s:%s"%(token.line,token.column))
    result = self.operands.pop()
    value = self.token_to_dir(result)
    self.gen_quad("GOTOF", value, None, None)
    # self.gen_quad("GOTOF", result.value, None, None)
    self.jumps.push(len(self.records)-1)

  def while_end(self):
    end = self.jumps.pop()
    retornar = self.jumps.pop()
    self.gen_quad("GOTO", None, None, retornar)
    self.fill_goto(end, len(self.records))

  def gen_era(self, name, params_table):
    self.gen_quad("ERA", None, None, name)
    self.parameter_count.push(0)
    self.current_params_table = params_table

  def gen_parameter(self):
    argument = self.operands.pop()
    argument_type = self.types.pop()
    try:
      current_num = self.parameter_count.top()
      key, value = self.current_params_table.items()[current_num]
    except IndexError:
      raise Exception("Function not declared with the same parameter size at %s:%s"%(argument.line, argument.column))
    result_type = self.semantic_cube.cube[argument_type][value["type"]]["="]
    if result_type == "ERROR":
      raise Exception("Type mismatch trying to assign (type: %s) to parameter %s (type: %s), at: %s:%s"%(argument_type, argument.value, value['type'], argument.line, argument.column))
    value = self.token_to_dir(argument)
    self.gen_quad("PARAM",value,None,"param"+str(current_num))

  def more_params(self):
    actual = self.parameter_count.pop()
    actual+=1
    self.parameter_count.push(actual)

  def verify_params_len(self, token):
    actual = self.parameter_count.top()
    if actual+1 != len(self.current_params_table):
      raise Exception("Function not declared with the same parameter size at %s:%s"%(token.line, token.column))
    self.parameter_count.pop()

  def draw_era_sub(self, name):
    self.gen_quad(name, None, None, None)
    self.parameter_count.push(0)

  def draw_params(self):
    argument = self.operands.pop()
    argument_type = self.types.pop()
    result_type = self.semantic_cube.cube[argument_type]["decimal"]["="]
    result_type_2 = self.semantic_cube.cube[argument_type]["entero"]["="]
    if result_type == "ERROR" and result_type_2 == "ERROR":
      raise Exception("Type mismatch trying to assign (type: %s) to parameter %s (type: %s), at: %s:%s"%(argument_type, argument.value, "decimal", argument.line, argument.column))
    actual = self.parameter_count.top()
    value = self.token_to_dir(argument)
    self.gen_quad("PARAM",value,None,"param"+str(actual))
    # value = self.token_to_dir(argument)
    # self.gen_quad("PARAM",value,None,"param"+str(self.parameter_count))

  def gen_draw_quad(self, value):
    actual = self.parameter_count.top()
    dir = self.token_to_dir(value)
    self.gen_quad("PARAM",dir,None,"param"+str(actual))
    # self.gen_quad("PARAM",value,None,"param"+str(actual))

  def fill_main(self):
    end = self.jumps.pop()
    self.fill_goto(end, len(self.records))

  def gen_return_assign(self, name):
    # pprint.pprint(self.operands.stack)
    # pprint.pprint(self.operators.stack)
    # self.num_aviables+=1
    #     result_name = Token("T_TMP_ID", 'tmp_'+str(result_type)+'_'+str(self.num_aviables))
    #     # print(result_name.value)
    #     left = self.token_to_dir(left_operand)
    #     right = self.token_to_dir(right_operand)
    #     result = self.token_to_dir(result_name)
    #     self.gen_quad(operator, left, right, result)
    #     # self.gen_quad(operator, left_operand.value, right_operand.value, result_name.value)
    #     if operator != "=":
    #       self.operands.push(result_name)
    #       self.types.push(result_type)
    print("todo")
  
  def reset_tmp_counter(self):
    self.num_aviables = 0;
    self.tmp_bool = 12000
    self.tmp_decimal = 11000
    self.tmp_int = 10000

  def token_to_dir(self, token, look_in = None):
    value = None
    if token.type == "T_NUM_INT":
      value = self.cte_int
      self.cte_int+=1

    elif token.type == "T_NUM_FLOAT":
      value = self.cte_decimal
      self.cte_decimal+=1

    elif token.type == "T_TMP_ID":
      if token.value in self.dir_tmp:
        value = self.dir_tmp[token.value]
      else:
        if "entero" in token.value:
          self.dir_tmp[token.value] = self.tmp_int
          value = self.tmp_int
          self.tmp_int+=1

        if "decimal" in token.value:
          self.dir_tmp[token.value] = self.tmp_decimal
          value = self.tmp_decimal
          self.tmp_decimal+=1

        if "booleano" in token.value:
          self.dir_tmp[token.value] = self.tmp_bool
          value = self.tmp_bool
          self.tmp_bool+=1

    elif token.type == "T_VAR_ID":
      if look_in != None:
        value = look_in[token.value]['dirV']
      else:
        value = self.fun_dir.get_dirV_of(token.value)

    elif token.type == 'T_FUN_ID':
      fun_table = self.fun_dir.get_fun_table_by_id(token.value)
      if fun_table["type"] == 'entero':
        value = self.glo_tmp_int
        self.glo_tmp_int+=1

      elif fun_table["type"] == 'decimal':
        value = self.glo_tmp_decimal
        self.glo_tmp_decimal+=1

    elif token.type == 'T_ID':
      value = token.value

    elif token.type == 'T_COLOR':
      value = token.value

    return value