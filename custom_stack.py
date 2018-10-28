import pprint

class Stack:
  def __init__(self):
    self.stack = []
    self.len = 0

  def __str__(self):
    txt = "["
    for value in self.stack:
      if hasattr(value, 'stack'):
        txt += "["
        txt += value.__str__()
        txt += "]"
      else:
        txt += str(value)
        txt+=", "
    txt+=']'
    return txt

  def push(self, item):
    if isinstance(item, Stack):
      self.len-=1
    if hasattr(self.top(), 'stack'):
      self.top().push(item)
    else:
      self.stack.append(item)
    self.len+=1

  def pop(self, parent=False):
    print('@@@')
    print(self.top())
    print('@@@')
    if parent and hasattr(self.top(), 'stack'):
      self.len -= len(self.top().stack)
      return self.top().pop()
    else:
      self.len-=1
      return self.stack.pop()

  def top(self):
    if(len(self.stack) == 0):
      return ''
    value = self.stack.pop()
    self.stack.append(value)
    return value

  def size(self):
    return self.len