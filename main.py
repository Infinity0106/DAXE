from lark import Lark
from transformer import DaxeTransformer

daxe_parser = Lark('''
g_iniciar_programa: g_nombre_programa g_variables? g_funciones* g_main

g_nombre_programa: a_t_programa T_COMILLA a_t_id_programa T_COMILLA T_PUNTO_COMA

g_variables: a_t_var a_t_var_id_y_tipo [T_LEFT_BRAKET T_NUM_INT T_RIGHT_BRAKET] g_variables_1 T_PUNTO_COMA
g_variables_1: [(T_COMMA a_t_var_id_y_tipo [T_LEFT_BRAKET T_NUM_INT T_RIGHT_BRAKET])*]

g_funciones: a_t_fun T_PUNTO_PUNTO g_funciones_1 a_t_fun_id a_t_fun_l_par [g_funciones_2] T_RIGHT_PAR g_funciones_3
g_funciones_1: a_t_var_type
             | a_t_var_void
g_funciones_2: a_t_var_id_y_tipo [(T_COMMA a_t_var_id_y_tipo)*]
g_funciones_3: T_LEFT_CRULY_BRAKET g_variables? g_estatutos g_funciones_4 g_t_end_function
g_funciones_4: [T_RETURN g_var_cte T_PUNTO_COMA]

g_main: T_DIBUJAR T_LEFT_PAR T_RIGHT_PAR T_LEFT_CRULY_BRAKET [g_variables] (g_estatutos)* a_t_end_program

g_dibujar_acciones: g_dibujar_acciones_1 g_expresion T_PUNTO_COMA
g_dibujar_acciones_1: T_ADELANTE
                    | T_ROTAR

g_estatutos: g_condicional
           | g_ciclo
           | g_dibujar_acciones
           | g_dibujar_objetos
           | g_asignacion
           | g_escritura
           | T_FUN_ID T_LEFT_PAR [g_expresion [(T_COMMA g_expresion)*]] T_RIGHT_PAR T_PUNTO_COMA

g_dibujar_objetos: T_CUADRADO g_expresion T_COMMA g_expresion T_COMMA g_expresion T_COMMA T_COLOR T_COMMA T_NUM_INT T_PUNTO_COMA
                 | T_CIRCULO g_expresion T_COMMA g_expresion T_COMMA g_expresion T_COMMA T_COLOR T_COMMA T_NUM_INT T_PUNTO_COMA
                 | T_TRIANGULO g_expresion T_COMMA g_expresion T_COMMA g_expresion T_COMMA g_expresion T_COMMA T_COLOR T_COMMA T_NUM_INT T_PUNTO_COMA
                 | T_TEXTO g_expresion T_COMMA g_expresion T_COMMA T_COMILLA T_ID T_COMILLA T_COMMA T_COLOR T_COMMA T_NUM_INT T_PUNTO_COMA

g_escritura: T_IMPRIMIR g_expresion T_PUNTO_COMA

g_expresion: g_exp [g_relacional g_exp]

g_relacional: T_MAYOR_QUE
            | T_MENOR_QUE
            | T_MAYOR_IGUAL_QUE
            | T_MENOR_IGUAL_QUE
            | T_IGUAL_IGUAL_QUE
            | T_DIFERENTE_QUE

g_ciclo: T_MIENTRAS T_LEFT_PAR g_expresion T_RIGHT_PAR T_LEFT_CRULY_BRAKET [(g_estatutos)*] T_RIGHT_CRULY_BRAKET

g_asignacion: T_VAR_ID [T_LEFT_BRAKET g_expresion T_RIGHT_BRAKET] T_IGUAL g_expresion T_PUNTO_COMA

g_exp: g_termino [(g_exp_1 g_termino)*]
g_exp_1: T_PLUS
			 | T_MINUS
       
g_termino: g_factor [(g_termino_1 g_factor)*]
g_termino_1: T_MULTIPLICATION
					 | T_DIVITION
           
g_factor: T_LEFT_PAR g_expresion T_RIGHT_PAR
				| g_factor_1? g_var_cte
g_factor_1: T_PLUS
					| T_MINUS
           
g_var_cte: T_ID
				 | T_VAR_ID
         | T_NUM_FLOAT
         | T_NUM_INT
         | T_FUN_ID T_LEFT_PAR [g_expresion [(T_COMMA g_expresion)*]] T_RIGHT_PAR
         | T_VAR_ID T_LEFT_BRAKET g_expresion T_RIGHT_BRAKET
         
g_condicional: T_IF T_LEFT_PAR g_expresion T_RIGHT_PAR g_condicional_1 [T_ELSE g_condicional_1]
g_condicional_1: T_LEFT_CRULY_BRAKET [(g_estatutos)*] T_RIGHT_CRULY_BRAKET

// ACTIONS
a_t_programa: T_PROGRAM
a_t_id_programa: T_ID
a_t_var: T_VAR
a_t_var_id_y_tipo: T_VAR_ID T_PUNTO_PUNTO a_t_var_type
a_t_end_program: T_RIGHT_CRULY_BRAKET
a_t_var_type: T_VAR_TYPE
a_t_var_void: T_VOID
a_t_fun: T_FUN
a_t_fun_id: T_FUN_ID
a_t_fun_l_par: T_LEFT_PAR
g_t_end_function: T_RIGHT_CRULY_BRAKET


// TOKENS
T_PROGRAM: "programa"i
T_COMILLA: /(\"|\')/
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
T_FUN: "funcion"
T_VOID: "void"
T_FUN_ID: /~[A-Za-z]+/
T_LEFT_PAR: "("
T_RIGHT_PAR: ")"
T_LEFT_CRULY_BRAKET: "{"
T_RIGHT_CRULY_BRAKET: "}"
T_RETURN: "regresar"
T_DIBUJAR: "dibujar"
T_ADELANTE: "adelante"
T_ROTAR: "rotar"
T_MIENTRAS: "mientras"
T_CIRCULO: "circulo"
T_CUADRADO: "cuadrado"
T_TRIANGULO: "triangulo"
T_TEXTO: "texto"
T_IGUAL: "="
T_POUND: "#"
T_PLUS: "+"
T_MINUS: "-"
T_DIVITION: "/"
T_MULTIPLICATION: "*"
T_IF: "si"
T_ELSE: "sino"
T_IMPRIMIR: "imprimir"
T_MAYOR_QUE: ">"
T_MENOR_QUE: "<"
T_IGUAL_IGUAL_QUE: "=="
T_MAYOR_IGUAL_QUE: ">="
T_MENOR_IGUAL_QUE: "<="
T_DIFERENTE_QUE: "<>"
T_COLOR: /rgb\((\d+),(\d+),(\d+)\)/



T_NUM_DEG: /(36[0]|3[0-5][0-9]|[12][0-9][0-9]|[1-9]?[0-9])/
T_NUM_FLOAT: FLOAT


%import common.WS
%import common.INT
%import common.FLOAT
%import common.LETTER

%ignore WS
''', start='g_iniciar_programa', parser='lalr')

tree = daxe_parser.parse('''
programa "prueba";
var &i : entero, &j : decimal;

funcion : entero ~uno(&juan : entero, &pancho : decimal){
  var &k : entero;
  si(&juan < &pancho){
    imprimir &i;
  } sino {
    imprimir &j;
  }
  regresar &k;
}

funcion : void ~dos(&juan : entero, &pancho : decimal){
  var &k : entero;
  si(&juan < &pancho){
    imprimir &i;
  } sino {
    imprimir &j;
  }
}

dibujar(){
  var &h : decimal;

  adelante 60;
  rotar &i;
  cuadrado 5, 6, 19, rgb(10,34,23), 5;
  circulo 0,0,10,rgb(10,34,23),2;
  triangulo &j, 10, ~uno(&x,&y),5, rgb(10,34,23), 2;
  texto 1, 0, 'juancho', rgb(10,34,23), 24;

  mientras(&i < 10){
    &i = &i + 1;
  }

  ~uno(&i, &j);
}
''')

DaxeTransformer().visit(tree)
# print(DaxeTransformer().visit(tree))