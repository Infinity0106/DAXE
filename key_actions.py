class KeyActions:
  def __init__(self):
    self.table={
      "+":0,
      "-":1,
      "*":2,
      "/":3,
      "==":4,
      ">=":5,
      "<=":6,
      "<":7,
      ">":8,
      "<>":9,
      "=":10,
      "GOTO":11, #salto incondicional
      "GOTOF":12, #Goto en falso
      "GOTOV":13, #Goto en verdadero
      "PRINT":14, #imprimir en pantall
      "MOVF":15, #dibujar acciones adelante
      "ROT":16, #dibujar acciones rotar,
      "PARAM":17,
      "GOSUB":18,
      "SCUAD":19,
      "ECUAD":20,
      "SCIR":21,
      "ECIR":22,
      "STRI":23,
      "ETRI":24,
      "STXT":25,
      "ETXT":26,
      "ENDPROC":27,
      "ERA":28,
      "RETURN":29
    }