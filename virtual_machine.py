import turtle
import canvasvg
import pprint

class DaxeVM:
  def __init__(self, quads, dir_fun):
    pprint.pprint(dir_fun.dir)
    self.current_x = 0
    self.current_y = 0
    i=0
    while i < len(quads):
      record = quads[i]
      if record[0] == "+":
        print("+")
      elif record[0] == "-":
        print("-")
      elif record[0] == "*":
        print("*")
      elif record[0] == "/":
        print("/")
      elif record[0] == "==":
        print("==")
      elif record[0] == ">=":
        print(">=")
      elif record[0] == "<=":
        print("<=")
      elif record[0] == "<":
        print("<")
      elif record[0] == ">":
        print(">")
      elif record[0] == "<>":
        print("<>")
      elif record[0] == "=":
        print("=")
      elif record[0] == "GOTO":
        print("GOTO")
        # i = record[3]
      elif record[0] == "GOTOF":
        print("GOTOF")
      elif record[0] == "GOTOV":
        print("GOTOV")
      elif record[0] == "PRINT":
        print("print")
        print(record[3])
      elif record[0] == "MOVF":
        print("MOVF")
      elif record[0] == "ROT":
        print("ROT")
      elif record[0] == "PARAM":
        print("PARAM")
      elif record[0] == "GOSUB":
        print("GOSUB")
      elif record[0] == "SCUAD":
        print("SCUAD")
      elif record[0] == "ECUAD":
        print("ECUAD")
      elif record[0] == "SCIR":
        print("SCIR")
      elif record[0] == "ECIR":
        print("ECIR")
      elif record[0] == "STRI":
        print("STRI")
      elif record[0] == "ETRI":
        print("ETRI")
      elif record[0] == "STXT":
        print("STXT")
      elif record[0] == "ETXT":
        print("ETXT")
      elif record[0] == "PARAM":
        print("PARAM")
      elif record[0] == "ENDPROC":
        print("ENDPROC")
      elif record[0] == "ERA":
        print("ERA")
      elif record[0] == "RETURN":
        print("RETURN")
      else:
        raise Exception("Unrecognized action %s"%(record[0]))
      i+=1
