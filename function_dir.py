from collections import OrderedDict

class FunctionsDir:
  def __init__(self):
    self.dir = {}
    self.current_func = None
    self.program_key = None
    self.current_type = None
    self.current_var = None
    self.loc_int = 8000
    self.loc_decimal = 9000
    self.glo_int = 1000
    self.glo_decimal = 2000

  def create_program(self, name, type):
    """
      inicializa el direcotiro de funciones
      con la primera funcion global que
      es el main e inicialzar las variables
      de current type y program key que se
      va a utilizar para linkear las variables
      de otras funciones

      name: nombre del programa
      type: "void"
    """
    self.dir[name]={
      "type": type
    }
    self.current_func = name
    self.program_key = name
    self.current_type = type
  
  def create_var_table(self):
    """
      crea un direcotiro de variables si no se ha
      inicializado en la funcion local actual,
    """
    if "vars" not in self.dir[self.current_func]:
      self.dir[self.current_func]["vars"]={};

  def set_current_type(self, type):
    """
      cambiar el tipo acutal, para variables
      y funciones delcaradas

      type: "entero", "decimal, "void"
    """
    self.current_type = type

  def add_function(self, name):
    """
      detecta si la funcion ya ha sido declarada, en ese caso
      regresa error en caso contrario crea un directorio
      para las funciones sin propiedades.
      
      name: "nombre de la funcion"
    """
    if name in self.dir:
      raise Exception("Declaraci\xc3\xb3n m\xc3\xbaltiple de funciones con el mismo nombre %s"%(name))
    self.dir[name]={}
    self.current_func=name

  def create_function_vars(self):
    """
      Agrega la funcion actual declarada
      con sus varibales y parametros vacios, 
      en caso de que no sea tipo void
      genera una propiedad return para 
      generar una direccion virtual
    """
    self.dir[self.current_func]={
      "type": self.current_type,
      "vars": OrderedDict(),
      "params": OrderedDict()
    }
    if self.current_type != "void":
      self.dir[self.current_func]["return"]=self.get_aviable_dir(self.current_type, True)
  
  def create_params_of_function(self):
    """
      obtiene todas las variables creadas
      hasta este momento, y las va agregando 
      a los parametros de la funcion
    """
    for key in self.dir[self.current_func]["vars"]:
      self.dir[self.current_func]["params"][key] = self.dir[self.current_func]["vars"][key]

  def define_func_start_point(self, index):
    """
      define el primer cuadruplo creado en la funcion,
      para saber a donde brincar cuando se invoque
    """
    self.dir[self.current_func]["start"]=index

  def delete_current_var_table(self, size):
    """
      se agrega el tamano de temporales
      que se van a utilizar para separa
      la memoria de ejecucion cuadno se invoque
    """
    # del self.dir[self.current_func]["vars"]
    self.dir[self.current_func]['tmp_size'] = size

  def add_variable(self, var_name):
    """
      busca en las variables locales y globales si
      estan declaradas si ya lo estan regresa un error
      y crea una propiedad de varaible actual y guarda 
      su tipo y direccion virtual dependiendo los contadores
      en donde esten.
      var_name: "string"
    """
    if var_name in self.dir[self.current_func]["vars"] or ("vars" in self.dir[self.program_key] and var_name in self.dir[self.program_key]["vars"]):
      raise Exception("Declaraci\xc3\xb3n m\xc3\xbaltiple de variable(%s) en la funci\xc3\xb3n(%s)"%(var_name, self.current_func))
    self.current_var = var_name
    self.dir[self.current_func]["vars"][var_name]={
      "type": self.current_type,
      "dirV": self.get_aviable_dir(self.current_type, self.current_func == self.program_key)
    }

  def get_current_vars_table(self):
    """
      evalua si las variables exiten en la tempora
      y si existen variables globales delcaras,
      lo combinan todo para poder regresar las variables
      a las que tiene acceso el programa en este momento.
    """
    if "vars" in self.dir[self.current_func]:
      tmp = self.dir[self.current_func]["vars"].copy()
      if "vars" in self.dir[self.program_key]:
        tmp.update(self.dir[self.program_key]["vars"])
    elif "vars" in self.dir[self.program_key]:
      tmp = self.dir[self.program_key]["vars"]
    else:
      tmp = {}
    return tmp

  def validate_existence(self, key):
    """
      validar que existe la funcion
      en la tabla de funciones
    """
    if key.value not in self.dir:
      raise Exception("Funci\xc3\xb3n %s indefinida en %s:%s"%(key.value, key.line, key.column))

  def get_params_of(self, value):
    """
      regresa los parametros de la funcion
      pedida
    """
    return self.dir[value]['params']

  def get_current_fun_table(self):
    """
      regresa la funcion que esta
      activa.
    """
    return self.dir[self.current_func]
  
  def get_fun_table_by_id(self, id):
    """
      regresa la funcion con su informacion completa
      en base a tu id.
    """
    return self.dir[id]

  def get_type_of(self, var_id):
    """
      regresa el tipo de la variable,
      para poder compara las operaciones con
      cubo semantico.
    """
    tmp = self.dir[self.current_func]["vars"].copy()
    if "vars" in self.dir[self.program_key]:
      tmp.update(self.dir[self.program_key]["vars"])
    return tmp[var_id]["type"]

  def get_dirV_of(self, var_id):
    """
      convierte id de varaible a su
      direccion virtual de dicha variable
    """
    tmp = self.dir[self.current_func]["vars"].copy()
    if "vars" in self.dir[self.program_key]:
      tmp.update(self.dir[self.program_key]["vars"])
    return tmp[var_id]["dirV"]
  
  def get_aviable_dir(self, type, is_global):
    """
      convertir strings a direcciones
      disponibles ya sean globales
      o locales, enteras o decimales
    """
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
    """
      reinicar los valores de
      las variables locales para poder
      uitlizarlas en otras llamadas
    """
    self.loc_int = 8000
    self.loc_decimal = 9000

  def current_var_is_array(self):
    """
      declara que la variable es arreglo
      e inicializar su tamano en 0
    """
    self.dir[self.current_func]["vars"][self.current_var]["dim"]=0
  
  def assign_dim(self, size):
    """
      crear la dimension (espacion en memoria)
      que se va a utiliza para el arreglo
    """
    self.dir[self.current_func]["vars"][self.current_var]["dim"]=size
  
  def next_aviable_dir(self):
    """
      regresa la siguiente vairable que se puede
      utilziar que son lcoales enteras o decimales, y globales
      entera y decimales, que son las que se pueden
      utlizar en las funciones.
    """
    dir = self.dir[self.current_func]["vars"][self.current_var]["dirV"]
    size = self.dir[self.current_func]["vars"][self.current_var]["dim"] - 1

    if dir >= 8000 and dir <= 8999:
      self.loc_int += size
    elif dir >= 9000 and dir <= 9999:
      self.loc_decimal += size
    elif dir >= 1000 and dir <= 1999:
      self.glo_int += size
    elif dir >= 2000 and dir <= 2999:
      self.glo_decimal += size

