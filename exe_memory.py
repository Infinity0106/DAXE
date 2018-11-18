import pprint
import re

class DaxeMEM:
  def __init__(self):
    self.directions = {
      1:{},# Global Int
      2:{},# Global Decimal
      3:{},# Global Temporal Int
      4:{},# Global Temporal Decimal
      5:{},# Constant Int
      6:{},# Constant Decimal
      7:{},# Constant String
      8:{},# Local Int
      9:{},# Local Decimal
      10:{},# Temporal Int
      11:{},# Temporal Decimal
      12:{}# Temporal Bool
    }

  def add(self, value, dir_v):
    """
      en caso de ser un string convierte el numero a direccion para poder
      traer la direccion donde esta guardado el valor, 

      despues convierte la direccion virtual a numero accesible en memoria
      y le asigna el valor pasado como parametro
      value: el valor a asignar 4.3
      dir_v: direccion en donde asignarla (1000)
    """
    if isinstance(dir_v, str):
      dir_str = re.findall('\d+|$', dir_v)[0]
      dir_int = int(dir_str)
      dir_v = self.get(dir_int)
    key1 = dir_v/1000
    key2 = dir_v%1000
    self.directions[key1][key2] = value

  def add_dir_to_dir(self, dir_from, dir_to):
    """
      asigna el valor interno de la dir_from a la direccion to,
      sive para pasar valores de arreglos.

      dir_from: direccion virtual (1000)
      dir_to: direccion virtual(1000)
    """
    try:
      keyfrom1 = dir_from/1000
      keyfrom2 = dir_from%1000
      keyto1 = dir_to/1000
      keyto2 = dir_to%1000
      self.directions[keyto1][keyto2] = self.directions[keyfrom1][keyfrom2];
    except KeyError:
      raise Exception("Variable no inicializada")

  def get(self, dir_v):
    """
      checas si es un string para ver si es una direccion de arreglo
      en caso de serlo obtiene el valor de sa direccion
      y substituye la direccion_virtual obtenida,

      combierte la direccion virtual en manera accesibe para la memoria
      y regresa su valor, en caso de que la direccio no existe arroja
      variable no inicializada
    """
    try:
      if isinstance(dir_v, str):
        dir_str = re.findall('\d+|$', dir_v)[0]
        dir_int = int(dir_str)
        dir_v = self.get(dir_int)
      key1 = dir_v/1000
      key2 = dir_v%1000
      # pprint.pprint(self.directions)
      # print(self.directions[key1][key2])
      return self.directions[key1][key2]
    except KeyError:
      raise Exception("Variable no inicializada")

  def search(self, value, dir):
    """
      busca en las constante para ver si ya ha sido declarado el valor
      y no tener constantes repetidas, regresa la direccion en formato
      5010 (5 key, 10 valor)

      valor: constante,
      dir: direccion en numero (1,2,3)
    """
    # pprint.pprint(self.directions)
    for key, value_to in self.directions[dir].items():
      if value == value_to:
        return dir*1000+int(key)
    return None