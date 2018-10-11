class Stack:
  def __init__(self):
    self.stack = []

  def push(self, item):
    self.stack.append(item)

  def pop(self):
    return self.stack.pop()

  def top(self):
    if(len(self.stack) == 0):
      return ''
    value = self.stack.pop()
    self.stack.append(value)
    return value

