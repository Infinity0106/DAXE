from lark import Lark, tree
from visitor import DaxeVisitor
from transformer import DaxeTransformer
import sys

daxe_parser = Lark('''
g_iniciar_programa: g_nombre_programa g_variables? g_funciones* g_main

g_nombre_programa: a_t_programa T_COMILLA a_t_id_programa T_COMILLA T_PUNTO_COMA

g_variables: a_t_var a_t_var_id_y_tipo [a_g_var_array_left a_g_var_array_size a_g_var_array_right] g_variables_1 T_PUNTO_COMA
g_variables_1: [(T_COMMA a_t_var_id_y_tipo [a_g_var_array_left a_g_var_array_size a_g_var_array_right])*]

g_funciones: a_t_fun T_PUNTO_PUNTO g_funciones_1
g_funciones_1: a_t_var_type g_funciones_2 g_funciones_5
             | a_t_var_void g_funciones_2 g_funciones_4
g_funciones_2: a_t_fun_id a_t_fun_l_par [g_funciones_3] a_t_fun_r_par
g_funciones_3: a_t_var_id_y_tipo [(T_COMMA a_t_var_id_y_tipo)*]
g_funciones_4: T_LEFT_CRULY_BRAKET g_variables? a_g_fun_start_exec (g_estatutos)* a_t_end_function
g_funciones_5: T_LEFT_CRULY_BRAKET g_variables? a_g_fun_start_exec (g_estatutos)* T_RETURN a_g_return T_PUNTO_COMA a_t_end_function

g_main: a_g_main T_LEFT_PAR T_RIGHT_PAR T_LEFT_CRULY_BRAKET [g_variables] (g_estatutos)* a_t_end_program

g_dibujar_acciones: g_dibujar_acciones_1 T_PUNTO_COMA
g_dibujar_acciones_1: T_ADELANTE g_expresion a_g_dibujar_adelante
                    | T_ROTAR g_expresion a_g_dibujar_rotar

g_estatutos: g_condicional
           | g_ciclo
           | g_dibujar_acciones
           | g_dibujar_objetos
           | g_asignacion
           | g_escritura
           | g_llamada_funcion T_PUNTO_COMA

g_dibujar_objetos: a_g_cuadrado_init a_g_exp_param a_g_draw_p_one a_g_exp_param a_g_draw_p_one a_g_exp_param a_g_draw_p_one a_g_draw_t_color a_g_draw_p_one a_g_draw_stroke a_g_cuadrado_end
                 | a_g_circulo_init a_g_exp_param a_g_draw_p_one a_g_exp_param a_g_draw_p_one a_g_exp_param a_g_draw_p_one a_g_draw_t_color a_g_draw_p_one a_g_draw_stroke a_g_circulo_end
                 | a_g_triangulo_init a_g_exp_param a_g_draw_p_one a_g_exp_param a_g_draw_p_one a_g_exp_param a_g_draw_p_one a_g_exp_param a_g_draw_p_one a_g_draw_t_color a_g_draw_p_one a_g_draw_stroke a_g_triangulo_end
                 | a_g_texto_init a_g_exp_param a_g_draw_p_one a_g_exp_param a_g_draw_p_one a_g_draw_txt_body a_g_draw_p_one a_g_draw_t_color a_g_draw_p_one a_g_draw_stroke a_g_texto_end

g_escritura: T_IMPRIMIR g_expresion a_g_escritura T_PUNTO_COMA

g_ciclo: a_g_ciclo_start T_LEFT_PAR g_expresion a_g_ciclo_mid T_LEFT_CRULY_BRAKET [(g_estatutos)*] a_g_ciclo_end

g_asignacion: a_g_asignacion a_g_asignacion_igual g_expresion a_g_end_asignacion

g_expresion: g_exp [a_g_relacional g_exp a_g_end_expresion]

g_relacional: T_MAYOR_QUE
            | T_MENOR_QUE
            | T_MAYOR_IGUAL_QUE
            | T_MENOR_IGUAL_QUE
            | T_IGUAL_IGUAL_QUE
            | T_DIFERENTE_QUE

g_exp: g_termino a_g_exp_term [(a_g_exp_1 g_termino a_g_exp_term)*]
g_exp_1: T_PLUS
       | T_MINUS
       
g_termino: g_factor a_g_termino_term [(a_g_termino_1 g_factor a_g_termino_term)*]
g_termino_1: T_MULTIPLICATION
           | T_DIVITION

g_factor: a_g_factor_left_par g_expresion a_g_factor_right_par
        | g_var_cte

g_var_cte: a_g_var_cte

g_condicional: T_IF T_LEFT_PAR g_expresion a_g_condicional_1 g_condicional_1 [a_g_condicional_3 g_condicional_1] a_g_condicional_2
g_condicional_1: T_LEFT_CRULY_BRAKET [(g_estatutos)*] T_RIGHT_CRULY_BRAKET

g_llamada_funcion: a_g_funcion_call_start a_g_funcion_era [a_g_funcion_param [(a_g_funcion_params_more a_g_funcion_param)*]] a_g_funcion_verify_params a_g_funcion_end_instance

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
a_t_fun_r_par: T_RIGHT_PAR
a_g_fun_start_exec: 
a_t_end_function: T_RIGHT_CRULY_BRAKET

a_g_end_expresion: 
a_g_relacional: g_relacional
a_g_exp_1: g_exp_1
a_g_exp_term: 
a_g_termino_1: g_termino_1
a_g_termino_term: 
a_g_factor_left_par: T_LEFT_PAR
a_g_factor_right_par: T_RIGHT_PAR
a_g_var_cte: a_var_id [a_access_array_start a_access_array a_access_array_end]
           | T_NUM_FLOAT
           | T_NUM_INT
           | g_llamada_funcion
a_g_asignacion: a_var_id [a_access_array_start a_access_array a_access_array_end]
a_g_asignacion_igual: T_IGUAL
a_g_end_asignacion: T_PUNTO_COMA

a_g_escritura:
a_g_dibujar_adelante:
a_g_dibujar_rotar:

a_g_condicional_1: T_RIGHT_PAR
a_g_condicional_2:
a_g_condicional_3: T_ELSE
a_g_ciclo_start: T_MIENTRAS
a_g_ciclo_mid: T_RIGHT_PAR
a_g_ciclo_end: T_RIGHT_CRULY_BRAKET

a_g_funcion_call_start: T_FUN_ID
a_g_funcion_era: T_LEFT_PAR
a_g_funcion_param: g_expresion
a_g_funcion_params_more: T_COMMA
a_g_funcion_verify_params: T_RIGHT_PAR
a_g_funcion_end_instance:
a_g_return: g_expresion

a_g_cuadrado_init: T_CUADRADO
a_g_cuadrado_end: T_PUNTO_COMA
a_g_circulo_init: T_CIRCULO
a_g_circulo_end: T_PUNTO_COMA
a_g_triangulo_init: T_TRIANGULO
a_g_triangulo_end: T_PUNTO_COMA
a_g_texto_init: T_TEXTO
a_g_texto_end: T_PUNTO_COMA
a_g_exp_param: g_expresion
a_g_draw_p_one: T_COMMA
a_g_draw_t_color: T_COLOR
a_g_draw_stroke: T_NUM_INT
a_g_draw_txt_body: T_COMILLA T_ID T_COMILLA

a_g_main: T_DIBUJAR

a_g_var_array_left:T_LEFT_BRAKET
a_g_var_array_size: T_NUM_INT
a_g_var_array_right:T_RIGHT_BRAKET
a_var_id: T_VAR_ID
a_access_array_start: T_LEFT_BRAKET
a_access_array: g_expresion
a_access_array_end: T_RIGHT_BRAKET

// TOKENS
T_PROGRAM: "programa"i
T_COMILLA: /(\"|\')/
T_ID: /[A-Za-z0-9!@#$%^&*(),.?:{}|<>]+/
T_PUNTO_COMA: ";"
T_VAR: "var"i
T_VAR_ID: /&[A-Za-z]+/
T_PUNTO_PUNTO: ":"
T_VAR_TYPE: /entero|decimal/
T_LEFT_BRAKET: "["
T_RIGHT_BRAKET: "]"
T_NUM_INT: SIGNED_INT
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
T_COLOR: /rgb\(\s*(?:(?:\d{1,2}|1\d\d|2(?:[0-4]\d|5[0-5]))\s*,?\s*){3}\)/



T_NUM_DEG: /(36[0]|3[0-5][0-9]|[12][0-9][0-9]|[1-9]?[0-9])/
T_NUM_FLOAT: SIGNED_FLOAT


%import common.WS
%import common.INT
%import common.FLOAT
%import common.SIGNED_INT
%import common.SIGNED_FLOAT
%import common.LETTER
%import common.NEWLINE

COMMENT: "//" /(.)+/ NEWLINE
       | "(*" /(.|\\n|\\r)+/ "*)"

%ignore WS
%ignore COMMENT
''', start='g_iniciar_programa')

try:
  file_name = sys.argv[1]
  parse_str = open(file_name, "r")
except IndexError:
  raise Exception("No file passed as argument")

tree_parsed = daxe_parser.parse(parse_str.read())

# NOTE: if you want to append empty trees with LALR, should be with
# a transformer then use a visitor

# NOTE: debug to output a image of the tree parsed
# tree.pydot__tree_to_png(tree_parsed, "__output__.png")


DaxeVisitor().visit(tree_parsed)
