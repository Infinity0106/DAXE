import pprint

class Stack:
  def __init__(self):
    self.stack = []
    self.len = 0
    # self.has_instance=False

  def __str__(self):
    """
      imprimir el stack de manera apropiada,
      crear el propio print usilizado para
      debugear
    """
    txt="["
    for value in self.stack:
      # if hasattr(value, 'stack'):
      #   # txt += "["
      #   txt += value.__str__()
      #   # txt += "]"
      # else:
        txt += str(value)
        txt+=", "
    txt+="]"
    return txt

  def push(self, item):
    """
      agrega un valor al arreglo al final
      append (agrega al final)
    """
    # if hasattr(self.top(), 'stack'):
    #   self.has_instance=True
    #   self.top().push(item)
    # else:
    self.stack.append(item)

  def pop(self):
    """
      saca el ultimo valor de 
      la pila de instancia
    """
    return self.stack.pop()

  def top(self):
    """
      regresa el valor tope
      de la pila, en caso de estar
      vacia regresa un empty string
    """
    if(len(self.stack) == 0):
      return ''
    value = self.stack.pop()
    self.stack.append(value)
    return value

  def size(self):
    """
      regresa el tamano de la stack
      se utiliza para el stack overflow
    """
    return len(self.stack)

  def pop_arg(self):
    """
      loop por el stack hasta que detecte el fondo falso
      cada loop generar un pop (desechar informacion)
    """
    tmp = Stack()
    for i in reversed(self.stack):
      if i != "(":
        tmp.push(self.pop())
      else:
        self.pop();
        break
    return tmp;

  def top_arg(self):
    """
      loop en el stack para generar un stack temporal
      sin sacarlos en el general
    """
    tmp = Stack()
    for i in reversed(self.stack):
      if i != "(":
        tmp.push(i)
      else:
        break
    return tmp;
