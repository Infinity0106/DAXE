import pprint

class Stack:
  def __init__(self):
    self.stack = []
    self.len = 0
    # self.has_instance=False

  def __str__(self):
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
    # if hasattr(self.top(), 'stack'):
    #   self.has_instance=True
    #   self.top().push(item)
    # else:
      self.stack.append(item)

  def pop(self):
    return self.stack.pop()

  def top(self):
    if(len(self.stack) == 0):
      return ''
    value = self.stack.pop()
    self.stack.append(value)
    return value

  def size(self):
    return len(self.stack)

  def pop_arg(self):
    #TODO: make it work
    tmp = Stack()
    for i in reversed(self.stack):
      if i != "(":
        tmp.push(self.pop())
      else:
        self.pop();
        break
    return tmp;

  def top_arg(self):
    #TODO: make it work
    tmp = Stack()
    for i in reversed(self.stack):
      if i != "(":
        tmp.push(self.top())
      else:
        break
    return tmp;
