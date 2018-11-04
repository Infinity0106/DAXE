from custom_stack import Stack
import re
import turtle
import canvasvg
import pprint
import math

class DaxeVM:
  def __init__(self, quads, dir_fun, mem):
    # pprint.pprint(dir_fun.dir)
    # pprint.pprint(mem.directions)
    pprint.pprint(quads)
    self.current_x = 0
    self.current_y = 0
    self.left_op=0
    self.right_op=0
    self.params=Stack()
    self.flow=Stack()
    self.current_fun=Stack()
    i=0
    turtle.Screen().colormode(255)
    turtle.speed(0)
    while i < len(quads):
      record = quads[i]

      size = self.params.size()
      if size > 1000:
        raise Exception("Stack overflow")

      if record[0] == "+": #DONE
        self.left_op = mem.get(record[1])
        self.right_op = mem.get(record[2])
        mem.add(self.left_op+self.right_op, record[3])
      
      elif record[0] == "-": #DONE
        self.left_op = mem.get(record[1])
        self.right_op = mem.get(record[2])
        mem.add(self.left_op-self.right_op, record[3])
      
      elif record[0] == "*": #DONE
        self.left_op = mem.get(record[1])
        self.right_op = mem.get(record[2])
        mem.add(self.left_op*self.right_op, record[3])
      
      elif record[0] == "/": #DONE
        self.left_op = mem.get(record[1])
        self.right_op = mem.get(record[2])
        mem.add(float(self.left_op)/self.right_op, record[3])
      
      elif record[0] == "==": #DONE
        self.left_op = mem.get(record[1])
        self.right_op = mem.get(record[2])
        mem.add(self.left_op==self.right_op, record[3])
      
      elif record[0] == ">=": #DONE
        self.left_op = mem.get(record[1])
        self.right_op = mem.get(record[2])
        mem.add(self.left_op>=self.right_op, record[3])
      
      elif record[0] == "<=": #DONE
        self.left_op = mem.get(record[1])
        self.right_op = mem.get(record[2])
        mem.add(self.left_op<=self.right_op, record[3])
      
      elif record[0] == "<": #DONE
        self.left_op = mem.get(record[1])
        self.right_op = mem.get(record[2])
        mem.add(self.left_op<self.right_op, record[3])
      
      elif record[0] == ">": #DONE
        self.left_op = mem.get(record[1])
        self.right_op = mem.get(record[2])
        mem.add(self.left_op>self.right_op, record[3])
      
      elif record[0] == "<>": #DONE
        self.left_op = mem.get(record[1])
        self.right_op = mem.get(record[2])
        mem.add(self.left_op!=self.right_op, record[3])
      
      elif record[0] == "=": #DONE
        self.left_op = mem.get(record[1])
        mem.add(self.left_op, record[3])
      
      elif record[0] == "GOTO": #DONE
        i = record[3] - 1

      elif record[0] == "GOTOF":
        if not mem.get(record[1]):
          i = record[3]-1
      
      elif record[0] == "GOTOV":
        if mem.get(record[1]):
          i = record[3]-1
      
      elif record[0] == "PRINT": #DONE
        val = mem.get(record[3])
        print(val)
      
      elif record[0] == "MOVF":
        self.left_op = mem.get(record[3])
        turtle.fd(self.left_op)
      
      elif record[0] == "ROT":
        self.left_op = mem.get(record[3])
        turtle.left(self.left_op)
      
      elif record[0] == "PARAM":
        val = mem.get(record[1])
        self.params.push(val)

      elif record[0] == "GOSUB":
        self.flow.push(i)
        self.current_fun.push(record[3])
        if len(self.flow.stack)>1000:
          raise Exception("Stack overflow calling function %s"%(record[3]))
        i = dir_fun.dir[record[3]]['start']-1
        params_stack = self.params.top_arg()
        for key, value in dir_fun.dir[record[3]]['params'].items():
          mem.add(params_stack.top(), value['dirV']);

      elif record[0] == "SCUAD":
        self.params.push("(")
      
      elif record[0] == "ECUAD":
        params = self.params.pop_arg().stack
        turtle.pu()
        turtle.setx(params[4])
        turtle.sety(params[3])
        turtle.seth(0)
        turtle.pd()
        turtle.fillcolor(self.regtotup(params[1]))
        turtle.fill(True)
        turtle.pensize(params[0])
        turtle.fd(params[3])
        turtle.left(90)
        turtle.fd(params[3])
        turtle.left(90)
        turtle.fd(params[3])
        turtle.left(90)
        turtle.fd(params[3])
        turtle.left(90)
        turtle.fill(False)
      
      elif record[0] == "SCIR":
        self.params.push("(")
      
      elif record[0] == "ECIR":
        params = self.params.pop_arg().stack
        turtle.pu()
        turtle.setx(params[4])
        turtle.sety(params[3])
        turtle.seth(0)
        turtle.pd()
        turtle.fillcolor(self.regtotup(params[1]))
        turtle.fill(True)
        turtle.pensize(params[0])
        turtle.circle(params[2])
        turtle.fill(False)
      
      elif record[0] == "STRI":
        self.params.push("(")
      
      elif record[0] == "ETRI":
        params = self.params.pop_arg().stack
        turtle.pu()
        turtle.setx(params[5])
        turtle.sety(params[4])
        turtle.seth(0)
        turtle.pd()
        turtle.fillcolor(self.regtotup(params[1]))
        turtle.fill(True)
        turtle.pensize(params[0])
        l = ( params[2]**2 + (params[3]/2.0)**2)**0.5
        alfa = math.atan2(params[2], params[3]/2.0) # To compute alfa
        alfa = math.degrees(alfa)
        alfa = 180.0 - alfa
        turtle.forward(params[3])
        turtle.left(alfa)
        turtle.forward(l)
        turtle.left(2*(180-alfa))
        turtle.forward(l)
        turtle.fill(False)
      
      elif record[0] == "STXT":
        self.params.push("(")
      
      elif record[0] == "ETXT":
        params = self.params.pop_arg().stack
        print(params)
        turtle.pu()
        turtle.setx(params[4])
        turtle.sety(params[3])
        turtle.seth(0)
        turtle.pd()
        turtle.color(self.regtotup(params[1]))
        turtle.write(params[2],font=("Arial", params[0], "normal"))
      
      elif record[0] == "PARAM":
        val = mem.get(record[1])
        self.params.push(val)
    
      elif record[0] == "ENDPROC":
        i = self.flow.pop()
        self.current_fun.pop();
        self.params.pop_arg();
        call_stack = self.current_fun.top()
        if call_stack != '':
          params = self.params.top_arg();
          for key, value in dir_fun.dir[call_stack]['params'].items():
            mem.add(params.top(), value['dirV']);
      
      elif record[0] == "ERA":
        self.params.push("(")
      
      elif record[0] == "RETURN":
        # tmp_i = self.flow.top() + 1
        # record2 = quads[tmp_i];
        fun_name = self.current_fun.top()
        mem.add_dir_to_dir(record[3], dir_fun.dir[fun_name]['return'])

        # if record2[0] == 'PARAM':
        #   mem.add(value, record2[1])
        # elif record2[0] == '=':
        #   mem.add(value, record2[1])
        # elif record2[0] == 'PRINT':
        #   mem.add(value, record2[3])
        # elif record2[0] == 'GOSUB':
        #   mem.add(value, record2[3])
        # elif record2[0] == 'RETURN':
        #   mem.add(value, record2[3])

      else:
        raise Exception("Unrecognized action %s"%(record[0]))
      i+=1

    canvasvg.saveall("image.svg", turtle.getcanvas())
    turtle.done()

  def regtotup(self, str):
    arr = [int(s) for s in re.findall(r'\b\d+\b', str)]
    return (arr[0],arr[1],arr[2])