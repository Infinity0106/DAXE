from lark import Lark

l = Lark('''
g_iniciar_programa: g_nombre_programa g_variables?

g_nombre_programa: T_PROGRAM T_COMILLA T_ID T_COMILLA T_PUNTO_COMA

g_variables: T_VAR T_VAR_ID T_PUNTO_PUNTO T_VAR_TYPE [T_LEFT_BRAKET T_NUM_INT T_RIGHT_BRAKET] g_variables_1 T_PUNTO_COMA
g_variables_1: [(T_COMMA T_VAR_ID T_PUNTO_PUNTO T_VAR_TYPE [T_LEFT_BRAKET T_NUM_INT T_RIGHT_BRAKET])*]








// TOKENS
T_PROGRAM: "programa"i
T_COMILLA: /\"/
T_ID: /[A-Za-z]+/
T_PUNTO_COMA: ";"
T_VAR: "var"i
T_VAR_ID: /&[A-Za-z]+/
T_PUNTO_PUNTO: ":"
T_VAR_TYPE: /entero|decimal/
T_LEFT_BRAKET: "["
T_RIGHT_BRAKET: "]"
T_NUM_INT: INT
T_COMMA: ","




T_FUN_ID: /\~LETTER+/
T_NUM_DEG: /(36[0]|3[0-5][0-9]|[12][0-9][0-9]|[1-9]?[0-9])/
T_NUM_FLOAT: FLOAT


%import common.WS
%import common.INT
%import common.FLOAT
%import common.LETTER

%ignore WS
''', start='g_iniciar_programa', parser='lalr')

print( l.parse('''
programa "prueba";
var &i : entero, &j : decimal;

dibujar(){
  var &h : decimal;

  adelante 60;
  rotar &i;
  cuadro 5;
  circulo 10;
  triangulo &j, 10;

  mientras(&i < 10){
    &i = &i + 1;
  }

  ~uno(&i, &j);
}
''') )

# programa "prueba";
# var &i : entero, &j : decimal;

# funcion : entero ~uno(&juan : entero, &pancho : decimal){
#   var &k : entero;
#   si(&juan < &pancho){
#     imprimir &i;
#   } sino {
#     imprimir &j;
#   }
#   regresar &k;
# }

# dibujar(){
#   var &h : decimal;

#   adelante 60;
#   rotar &i;
#   cuadro 5;
#   circulo 10;
#   triangulo &j, 10;

#   mientras(&i < 10){
#     &i = &i + 1;
#   }

#   ~uno(&i, &j);
# }