from collections import OrderedDict

class FunctionsDir:
  def __init__(self):
    self.dir = {}
    self.current_func = None
    self.program_key = None
    self.current_type = None
    self.loc_int = 8000
    self.loc_decimal = 9000
    self.glo_int = 1000
    self.glo_decimal = 2000

  def create_program(self, name, type):
    self.dir[name]={
      "type": type
    }
    self.current_func = name
    self.program_key = name
    self.current_type = type
  
  def create_var_table(self):
    if "vars" not in self.dir[self.current_func]:
      self.dir[self.current_func]["vars"]={};

  def set_current_type(self, type):
    self.current_type = type

  def add_function(self, name):
    if name in self.dir:
      raise Exception("Multiple function declaration with the same name %s"%(name))
    self.dir[name]={}
    self.current_func=name

  def create_function_vars(self):
    self.dir[self.current_func]={
      "type": self.current_type,
      "vars": OrderedDict(),
      "params": OrderedDict()
    }
    if self.current_type != "void":
      self.dir[self.current_func]["return"]=self.get_aviable_dir(self.current_type, True)
  
  def create_params_of_function(self):
    for key in self.dir[self.current_func]["vars"]:
      self.dir[self.current_func]["params"][key] = self.dir[self.current_func]["vars"][key]

  def define_func_start_point(self, index):
    self.dir[self.current_func]["start"]=index

  def delete_current_var_table(self, size):
    # del self.dir[self.current_func]["vars"]
    self.dir[self.current_func]['tmp_size'] = size

  def add_variable(self, var_name):
    if var_name in self.dir[self.current_func]["vars"] or var_name in self.dir[self.program_key]["vars"]:
      raise Exception("Multiple variable declaration(%s) in function %s"%(var_name, self.current_func))
    self.dir[self.current_func]["vars"][var_name]={
      "type": self.current_type,
      "dirV": self.get_aviable_dir(self.current_type, self.current_func == self.program_key)
    }

  def get_current_vars_table(self):
    if "vars" in self.dir[self.current_func]:
      tmp = self.dir[self.current_func]["vars"].copy()
      tmp.update(self.dir[self.program_key]["vars"])
    else:
      tmp = self.dir[self.program_key]["vars"]
    return tmp

  def validate_existence(self, key):
    if key.value not in self.dir:
      raise Exception("Function %s not defined at %s:%s"%(key.value, key.line, key.column))

  def get_params_of(self, value):
    return self.dir[value]['params']

  def get_current_fun_table(self):
    return self.dir[self.current_func]
  
  def get_fun_table_by_id(self, id):
    return self.dir[id]

  def get_type_of(self, var_id):
    tmp = self.dir[self.current_func]["vars"].copy()
    tmp.update(self.dir[self.program_key]["vars"])
    return tmp[var_id]["type"]

  def get_dirV_of(self, var_id):
    tmp = self.dir[self.current_func]["vars"].copy()
    tmp.update(self.dir[self.program_key]["vars"])
    return tmp[var_id]["dirV"]
  
  def get_aviable_dir(self, type, is_global):
    value = None
    if is_global:
      if type == "entero":
        value = self.glo_int
        self.glo_int+=1

      elif type == "decimal":
        value = self.glo_decimal
        self.glo_decimal+=1

    else:
      if type == "entero":
        value = self.loc_int
        self.loc_int+=1

      elif type == "decimal":
        value = self.loc_decimal
        self.loc_decimal+=1

    return value

  def reset_local_counter(self):
    self.loc_int = 8000
    self.loc_decimal = 9000