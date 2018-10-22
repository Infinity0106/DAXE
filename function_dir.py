from collections import OrderedDict

class FunctionsDir:
  def __init__(self):
    self.dir = {}
    self.current_func = None
    self.program_key = None
    self.current_type = None

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
  
  def create_params_of_function(self):
    for key in self.dir[self.current_func]["vars"]:
      self.dir[self.current_func]["params"][key] = self.dir[self.current_func]["vars"][key]

  def define_func_start_point(self, index):
    self.dir[self.current_func]["start"]=index

  def delete_current_var_table(self):
    del self.dir[self.current_func]["vars"]

  def add_variable(self, var_name):
    if var_name in self.dir[self.current_func]["vars"] or var_name in self.dir[self.program_key]["vars"]:
      raise Exception("Multiple variable declaration(%s) in function %s"%(var_name, self.current_func))
    self.dir[self.current_func]["vars"][var_name]={
      "type": self.current_type
    }

  def get_current_vars_table(self):
    tmp = self.dir[self.current_func]["vars"].copy()
    tmp.update(self.dir[self.program_key]["vars"])
    return tmp

  def validate_existence(self, key):
    if key.value not in self.dir:
      raise Exception("Function %s not defined at %s:%s"%(key.value, key.line, key.column))

  def get_params_of(self, value):
    return self.dir[value]['params']