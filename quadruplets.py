from custom_stack import Stack
from semantic_cube import SemanticCube
from lark import Token
from key_actions import KeyActions
from exe_memory import DaxeMEM
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
    self.cte_string = 7000
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
    self.memory = DaxeMEM()
    self.curren_arr = None

  def link_fun_dir(self, fun):
    """
      pasar la instancia del directorio de funciones
      a los quadruplos para poder usar sus funciones

      fun: instancia FunDir
    """
    self.fun_dir = fun

  def current_quad(self):
    """
     Regresa el indice de los records
     se obtiene por medio del tamano del
     arreglo
    """
    return len(self.records)

  def add_id(self, name, type):
    """
      Agregar un id y tu tipo para 
      que los dos stacks esten en sincronia

      name: Token,
      type: "decima", "entero", "booleano"
    """
    self.types.push(type)
    self.operands.push(name)

  def add_operator(self, item):
    """
      Agregar a la pila de operadoes cual es 
      el ultimo detectado

      item: "=","<=",">=",+,-,*,/,... etc.
    """
    self.operators.push(item)

  def pop_operator(self):
    """
      sacar un operador de la pila de operandos,
      se creo para la interaccion con la clase
      de visitantes
    """
    self.operators.pop()

  def algorithm_with(self, labels):
    """
      Algorithm_with: toma como parametros un arreglo de operadores
      ejemplo ["="] o ["/", "*"]

      entra si el tope del operador esta en la lista,
      despues se comparan los tipos para ver que no generen error
      generan la variable temporal con la direccion correcta
    """
    operator = self.operators.top()
    if operator in labels:
      right_operand = self.operands.pop()
      right_type = self.types.pop()
      left_operand = self.operands.pop()
      left_type = self.types.pop()
      operator = self.operators.pop()
      result_type = self.semantic_cube.cube[left_type][right_type][operator]
      if result_type == "ERROR":
        print(left_operand, left_type, right_operand, right_type)
        raise Exception("Tipos no coinciden en la %s (tipos: %s) a %s (tipos: %s), en: %s:%s"%(operator, right_type, left_operand, left_type, left_operand.line, left_operand.column))
      else:
        self.num_aviables+=1
        result_name = Token("T_TMP_ID", 'tmp_'+str(result_type)+'_'+str(self.num_aviables), line=left_operand.line, column= left_operand.column)
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
    """
      saca el tipo del temproa, en caso de no
      ser booleano, regresa error,
      despues el resultado lo valida para generar
      el gotof, y agrega a la pila de saltos
    """
    exp_type = self.types.pop()
    if exp_type != "booleano":
      raise Exception("Tipos no coinciden tratando de evaluar si en %s:%s"%(token.line,token.column))
    result = self.operands.pop()
    value = self.token_to_dir(result)
    self.gen_quad("GOTOF", value, None, None)
    # result = self.operands.pop()
    # self.gen_quad("GOTOF", result.value, None, None)
    self.jumps.push(len(self.records)-1)

  def end_if(self):
    """
      se saca el saldo inicial
      para poder rellenarlo con el cuadruplo despues
      del bracket que cierra
    """
    end = self.jumps.pop()
    self.fill_goto(end, len(self.records))

  def else_if(self):
    """
      genera el goto pero rellena el gotof
      anterior y genera los jumps para
      el goto del else
    """
    self.gen_quad("GOTO", None, None, None)
    false = self.jumps.pop()
    self.jumps.push(len(self.records)-1)
    self.fill_goto(false, len(self.records))

  def gen_custom_quad(self, type):
    """
      genera quad custom, 
      ya sea type que es la key,
      se utiliza para el print, 
      movf y rot, que solo tienen un resultado
    """
    result_name = self.operands.pop()
    result_type = self.types.pop()
    result = self.token_to_dir(result_name)
    self.gen_quad(type, None, None, result)

  def gen_quad(self, op, lop, rop, res):
    """
      genera un cuadriplo a los records
      op: key de operacion
      lop: left operando, string o numero o none
      rop: right operando, string o numero o none
      res: resultado de la operacion string o numero o none
    """
    if op == "=":
      self.records.append([op,rop,None,lop])
      # self.records.append([self.key_actions[op],rop,None,lop])
    else:
      self.records.append([op,lop,rop,res])
      # self.records.append([self.key_actions[op],lop,rop,res])
  
  def fill_goto(self, index, value):
    """
      obtiene el cuadruplo que se quiere
      rellenar con el index
      y se rellena con el value, que es es la nueva direccion
    """
    self.records[index][3] = value

  def while_start(self):
    """
      guarda el jump antes de la expresion
      para poder rellenar el ultimo goto
    """
    self.jumps.push(len(self.records))

  def while_mid(self, token):
    """
      genera el gotof despues de
      evaluar la expresion
    """
    exp_type = self.types.pop()
    if exp_type != "booleano":
      raise Exception("Tipos no coinciden tratando de evaluar si en %s:%s"%(token.line,token.column))
    result = self.operands.pop()
    value = self.token_to_dir(result)
    self.gen_quad("GOTOF", value, None, None)
    # self.gen_quad("GOTOF", result.value, None, None)
    self.jumps.push(len(self.records)-1)

  def while_end(self):
    """
      saca el jump generado
      para poder rellenar el
      goto generado.
    """
    end = self.jumps.pop()
    retornar = self.jumps.pop()
    self.gen_quad("GOTO", None, None, retornar)
    self.fill_goto(end, len(self.records))

  def gen_era(self, name, params_table):
    """
      inicializa el era para demostrar
      iniciar de la fucnion
    """
    self.gen_quad("ERA", None, None, name)
    self.parameter_count.push(0)
    self.current_params_table = params_table

  def gen_parameter(self):
    """
      generar el argumento
      en el cuadruplo de param
      y genera la key
    """
    argument = self.operands.pop()
    argument_type = self.types.pop()
    try:
      current_num = self.parameter_count.top()
      key, value = self.current_params_table.items()[current_num]
    except IndexError:
      raise Exception("Funci\xc3\xb3n no declarada con el mismo tama\xc3\xb1o de par\xc3\xa1metros en %s:%s"%(argument.line, argument.column))
    result_type = self.semantic_cube.cube[value["type"]][argument_type]["="]
    if result_type == "ERROR":
      raise Exception("Tipos no coinciden en la asignaci\xc3\xb3n (tipo: %s) al par\xc3\xa1metro %s (tipo: %s), en: %s:%s"%(argument_type, key, value['type'], argument.line, argument.column))
    value = self.token_to_dir(argument)
    self.gen_quad("PARAM",value,None,"param"+str(current_num))

  def more_params(self):
    """
      suma el index de los apramestor +1
      para que la key no se quede traslapada
    """
    actual = self.parameter_count.pop()
    actual+=1
    self.parameter_count.push(actual)

  def verify_params_len(self, token):
    """
      verificar que los parametros
      proporcionados sean del mismo
      tamano que los parametros declarados
      en la funcion
    """
    actual = self.parameter_count.top()
    if not (actual == 0 and len(self.current_params_table) == 0) and actual+1 != len(self.current_params_table):
      raise Exception("Funci\xc3\xb3n no declarada con el mismo tama\xc3\xb1o de par\xc3\xa1metros en %s:%s"%(token.line, token.column))
    self.parameter_count.pop()

  def draw_era_sub(self, name):
    """
      generar el era de los dibujos
    """
    self.gen_quad(name, None, None, None)
    self.parameter_count.push(0)

  def draw_params(self):
    """
      genera los parametros para 
      dibujar estos pueden ser
      validados con el tipo esperado
    """
    argument = self.operands.pop()
    argument_type = self.types.pop()
    result_type = self.semantic_cube.cube[argument_type]["decimal"]["="]
    result_type_2 = self.semantic_cube.cube[argument_type]["entero"]["="]
    if result_type == "ERROR" and result_type_2 == "ERROR":
      raise Exception("Tipos no coinciden en la asignaci\xc3\xb3n (tipo: %s) al par\xc3\xa1metro %s (tipo: %s), en: %s:%s"%(argument_type, argument.value, "decimal", argument.line, argument.column))
    actual = self.parameter_count.top()
    value = self.token_to_dir(argument)
    self.gen_quad("PARAM",value,None,"param"+str(actual))
    # value = self.token_to_dir(argument)
    # self.gen_quad("PARAM",value,None,"param"+str(self.parameter_count))

  def gen_draw_quad(self, value):
    """
      genera parametros para funciones de dibujar
    """
    actual = self.parameter_count.top()
    dir = self.token_to_dir(value)
    self.gen_quad("PARAM",dir,None,"param"+str(actual))
    # self.gen_quad("PARAM",value,None,"param"+str(actual))

  def fill_main(self):
    """
      rellena el primer goto del programa
      por que ya encontro la funcion main
    """
    end = self.jumps.pop()
    self.fill_goto(end, len(self.records))

  def gen_return_assign(self, name, dir, type):
    """
      genera el return, al final se genera una asignacion
      para poder obtener el valor de return
      y guardarlo en un temporal
    """
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
    self.num_aviables+=1
    result_name = Token("T_TMP_ID", 'tmp_'+str(type)+'_'+str(self.num_aviables))
    result = self.token_to_dir(result_name)
    self.gen_quad("=", result, dir, None)
    # self.gen_quad("=", result_name.value, dir, None)
    self.operands.push(result_name)
    self.types.push(type)

  def reset_tmp_counter(self):
    """
      reinicia los valor de contadores
      para los temporales y poder ahorrar memoria
    """
    self.num_aviables = 0;
    self.tmp_bool = 12000
    self.tmp_decimal = 11000
    self.tmp_int = 10000

  def token_to_dir(self, token, look_in = None):
    """
      token_to_dir: toke una variable tipo token
      tiene propiedad de tipo y valor, look_in es un directorio de variables
      si se porporciona busca ahi si no lo busca en la funcion actual

      switch de tipo de tocken para saber que contador aumentar y que tipo
      de variable es si es flotante, booleano, entero, contante, string
    """
    value = None
    if token.type == "T_NUM_INT":
      tmp = self.memory.search(int(token.value), 5)
      if tmp == None:
        value = self.cte_int
        self.cte_int+=1
        self.memory.add(int(token.value), value)
      else:
        value=tmp

    elif token.type == "T_NUM_FLOAT":
      tmp = self.memory.search(float(token.value), 6)
      if tmp == None:
        value = self.cte_decimal
        self.cte_decimal+=1
        self.memory.add(float(token.value), value)
      else:
        value = tmp

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
      value = self.cte_string
      self.cte_string+=1
      self.memory.add(token.value, value)

    elif token.type == 'T_COLOR':
      value = self.cte_string
      self.cte_string+=1
      self.memory.add(token.value, value)
    
    elif token.type == 'T_TMP_DIR':
      value = token.value

    return value

  def start_verify_array(self):
    """
      Obtener el tope de los operandos y de los tipos(id del arreglo)
      sin sacarlos, determinar si esta declarado como un arreglo
      y agregar fondo falso a los operadores para las expresiones
    """
    id = self.operands.top()
    type = self.types.top()
    var_table = self.fun_dir.get_current_vars_table()
    if not "dim" in var_table[id]:
      raise Exception("Variable (%s) no es un arreglo en %s:%s"%(id.value, id.line, id.column))
    self.curren_arr = var_table[id];
    self.add_operator("(")

  def verify_array(self):
    """
      obtener el tope de los operandos para determinar el valor
      y crear cuadruplo este en el rango de la dimension
    """
    tmp = self.operands.top()
    left = self.token_to_dir(tmp)
    self.gen_quad("VERIFY", left, 0, self.curren_arr["dim"])

  def generate_array_access(self):
    """
      Sacar los id del array y su expresion interna para accesso

      si el index no es entero marca error
      generan la suma de la direccion base mas el tamano del temporal
      para tener la direccion y generar su temporal (T)
      y agregarlo a los operadores
    """
    aux = self.operands.pop()
    aux_type = self.types.pop()
    array_id = self.operands.pop()
    array_type = self.types.pop()

    if aux_type != "entero":
      raise Exception("El \xc3\xadndice del arreglo (%s) no es un entero en %s:%s"%(aux.value, aux.line, aux.column))

    base = self.curren_arr["dirV"]

    self.num_aviables+=1
    result_name = Token("T_TMP_ID", 'tmp_'+str(array_type)+'_'+str(self.num_aviables), line=aux.line, column= aux.column)
    base_name = Token("T_NUM_INT", str(base), line=aux.line, column= aux.column)

    left = self.token_to_dir(aux)
    result = self.token_to_dir(result_name)
    dir_base = self.token_to_dir(base_name)
    self.gen_quad("+", left, dir_base, result)

    tmp_token = Token("T_TMP_DIR", '('+str(result)+')', line=aux.line, column= aux.column)
    self.operands.push(tmp_token)
    self.types.push(array_type)
    self.operators.pop()