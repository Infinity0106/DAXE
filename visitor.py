from lark.visitors import Visitor_Recursive
from function_dir import FunctionsDir
from quadruplets import Quadruplets
from virtual_machine import DaxeVM
from custom_stack import Stack
import pprint

class DaxeVisitor(Visitor_Recursive):
    def __init__(self):
        self.f_table = None
        self.quads = Quadruplets()
        self.fun_name = Stack()

    def a_t_programa(self, items):
        # print("1.Create DirFunc")
        self.f_table = FunctionsDir()
        self.quads.link_fun_dir(self.f_table)

    def a_t_id_programa(self, items):
        # print("2.Add id-name and type program a DirFunc")
        self.f_table.create_program(items.children[0].value, "void")

    def a_t_var(self, items):
        # print("3.If current Func doesn't have a VarTable then Create VarTable and link it to current Func")
        self.f_table.create_var_table()

    def a_t_var_id_y_tipo(self, items):
        # print("""5.Search for id-name in current VarTable
        #         if found a Error 'multiple declaration'
        #         if not add id-name and current-type to current VarTable""")
        # print("""11.Search for id-name in current VarTable
        #         if found a Error "multiple declaration"
        #         if not add id-name and current-type to current VarTable""")
        self.f_table.add_variable(items.children[0].value)

    def a_t_var_type(self, items):
        # print("4.Current-type = type")
        self.f_table.set_current_type(items.children[0].value)

    def a_t_end_program(self, items):
        # print("6.Delete DirFunc and current VarTable(Global)")
        # pprint.pprint(self.quads.records)
        # pprint.pprint(self.quads.operators.stack)
        # pprint.pprint(self.quads.operands.stack)
        DaxeVM(self.quads.records, self.f_table, self.quads.memory)
        del self.f_table

    # def a_t_fun(self, items):
        #TODO: nothing to prepare
        # print("7.Prepare DirFunc to add new function")

    def a_t_var_void(self, items):
        # print("8.Current-type = void")
        self.f_table.set_current_type(items.children[0].value)

    def a_t_fun_id(self, items):
        # print("""9.Search for id-name in DirFunc
        #         if found a Error "multiple declaration"
        #         if not add id-name and current-type to it.""")
        self.f_table.add_function(items.children[0].value)
        
    def a_t_fun_l_par(self, items):
        # print("10.Create a VarTable and link it to current Func")
        self.f_table.create_function_vars()
    
    def a_t_fun_r_par(self, items):
        # print("4. insert into dirfunc the number of parameters defined")
        self.f_table.create_params_of_function()

    def a_g_fun_start_exec(self, items):
        # print("inter into dir func the current quadruple tocunter to determine where the proceadure starts")
        self.f_table.define_func_start_point(self.quads.current_quad())
    
    def a_g_return(self, items):
        token = self.first_token(items)
        fun = self.f_table.get_current_fun_table()
        type = None
        if token.type == "T_NUM_FLOAT":
            type = "decimal"
        elif token.type == "T_NUM_INT":
            type = "entero"
        elif token.type == "T_FUN_ID":
            type = self.quads.types.top()
            token = self.quads.operands.pop()
        else:
            type = self.f_table.get_type_of(token.value)
        if fun['type'] != type:
            raise Exception("Type missmatch in return (expected: %s) (given: %s) at %s:%s"%(fun['type'], type, token.line, token.column))
        value = self.quads.token_to_dir(token);
        self.quads.gen_quad("RETURN", None, None, value)

    def a_t_end_function(self, items):
        # print("12.Delete current VarTable it's no longer required")
        self.f_table.delete_current_var_table(self.quads.num_aviables)
        self.quads.gen_quad("ENDPROC",None,None,None)
        self.quads.reset_tmp_counter()
        self.f_table.reset_local_counter()

    def a_g_end_expresion(self, items):
        # print("9. if poper.top() == rel.op then procede with 4 but different")
        self.quads.algorithm_with([">","<","==",">=","<=","<>"])

    def a_g_relacional(self, items):
        # print("8. poper.push(rel.op)")
        token = items.children[0].children[0]
        self.quads.add_operator(token.value)

    def a_g_exp_1(self, items):
        # print("2. poper.push(+ or -)")
        token = items.children[0].children[0]
        self.quads.add_operator(token.value)
    
    def a_g_exp_term(self, items):
        # print("4. all process with + or -")
        self.quads.algorithm_with(["-","+"])

    def a_g_termino_1(self, items):
        # print("3. poper.push(* or /")
        token = items.children[0].children[0]
        self.quads.add_operator(token.value)
    
    def a_g_termino_term(self, items):
        # print("5. all process with * or /")
        self.quads.algorithm_with(["*","/"])
    
    def a_g_factor_left_par(self, items):
        # print("6. poper.push(false bottom)")
        self.quads.add_operator("(")

    def a_g_factor_right_par(self, items):
        # print("7. poper.pop(false bottom)")
        self.quads.pop_operator()

    def a_g_var_cte(self, items):
        # print("1. pilao.push(id.name) and ptypes.push(id.type)")
        variables=self.f_table.get_current_vars_table()
        id_name=""
        type=""
        if(hasattr(items.children[0],'type')):
            if(items.children[0].type == 'T_VAR_ID'):
                if items.children[0].value in variables:
                    id_name = items.children[0]
                    type = variables[items.children[0].value]["type"]
                else:
                    raise Exception("Variable not defined %s, at: %s:%s"%(items.children[0].value, items.children[0].line, items.children[0].column))
            if(items.children[0].type == 'T_NUM_INT'):
                id_name = items.children[0]
                type = "entero"
            if(items.children[0].type == 'T_NUM_FLOAT'):
                id_name = items.children[0]
                type = "decimal"
        else:
            return
            # dont have to add a funciton becais we add it at the end_instance action
            # id_name = items.children[0].children[0].children[0]
            # type = self.f_table.get_fun_table_by_id(id_name.value)['type']
        self.quads.add_id(id_name, type)

    def a_g_asignacion(self, items):
        # print("10. agregar id de la asignacion")
        #TODO: poder insertar arreglos
        variables=self.f_table.get_current_vars_table()
        id_name=""
        type=""
        if(len(items.children) == 1):
            if(items.children[0].type == 'T_VAR_ID'):
                if items.children[0].value in variables:
                    id_name = items.children[0]
                    type = variables[items.children[0].value]["type"]
                else:
                    raise Exception("Variable not defined %s, at: %s:%s"%(items.children[0].value, items.children[0].line, items.children[0].column))
        self.quads.add_id(id_name, type)

    def a_g_asignacion_igual(self, items):
        # print("11 agregar = en operadores")
        token = items.children[0]
        self.quads.add_operator(token.value)

    def a_g_end_asignacion(self, items):
        # print("12 validar si hay un =")
        self.quads.algorithm_with(["="])

    def a_g_escritura(self, items):
        # print("add key of printing")
        self.quads.gen_custom_quad("PRINT")

    def a_g_dibujar_rotar(self, items):
        # print("generate quad at the end for rotation movement")
        self.quads.gen_custom_quad("ROT")

    def a_g_dibujar_adelante(self, items):
        # print("generate quad at the end for forward movement")
        self.quads.gen_custom_quad("MOVF")

    def a_g_condicional_1(self, items):
        # print("""1. exp_type = PTypes.pop()
        #         if(exp_type != bool) error
        #         else
        #             result = pilao.pop()
        #             generate_quad gotoF, result, None, ____
        #             Pjumps.push(count-1)
        #         """)
        token = items.children[0]
        self.quads.start_if(token)

    def a_g_condicional_2(self, items):
        # print("end = pjumps.pop(); fill(end, counter)")
        self.quads.end_if()

    def a_g_condicional_3(self, items):
        # print("""gen GOTO
        #         false = pjumps.pop()
        #         pjumps.push(count-1)
        #         fill(false, count)""")
        self.quads.else_if()

    def a_g_ciclo_start(self, items):
        # print("pjumps.push(count)")
        self.quads.while_start()

    def a_g_ciclo_mid(self, items):
        # print("""exp_type=ptypes.pop()
        #         if(exp_type != bool) error
        #         result = pilao.pop
        #         genquad gotof, result, none, none
        #         pjumps.push(count-1)""")
        token = items.children[0]
        self.quads.while_mid(token)

    def a_g_ciclo_end(self, items):
        # print("""end = pjumps.pop
        #         return = pjumps.pop
        #         gen goto ,none,none,return
        #         fill(end, count)""")
        self.quads.while_end()

    def a_g_funcion_call_start(self, items):
        # print("Verify that the procedure exists in the dirfunc")
        self.quads.add_operator("(")
        self.fun_name.push(items.children[0])
        self.f_table.validate_existence(self.fun_name.top())

    def a_g_funcion_era(self, items):
        # print("""generate action era size (activation record expansion new size)
        #         start the paramter counter (k) in 1
        #         add a pointer to the first paramter type in the paramtertable""")
        self.quads.gen_era(self.fun_name.top().value, self.f_table.get_params_of(self.fun_name.top().value))

    def a_g_funcion_param(self, items):
        # print("argument = pilao.pop(), argumenttype = ptypes.pop, verify type with paramter, generate parameter argument argument number")
        self.quads.gen_parameter()

    def a_g_funcion_params_more(self, items):
        # print("k++ move to the next paramter")
        self.quads.more_params()

    def a_g_funcion_verify_params(self, items):
        # print("verify that the last paramter points to null")
        self.quads.verify_params_len(items.children[0])

    def a_g_funcion_end_instance(self, items):
        # print("generate action gosub,prodecure_name, none, inital-address")
        tmp_fun_name = self.fun_name.pop()
        fun_table = self.f_table.get_fun_table_by_id(tmp_fun_name.value)
        self.quads.gen_quad("GOSUB",None,None,tmp_fun_name.value)
        if fun_table["type"] != "void":
            self.quads.gen_return_assign(tmp_fun_name.value, fun_table["return"], fun_table["type"])
        self.quads.pop_operator()

    def a_g_cuadrado_init(self, items):
        # print("init quad for drawing")
        self.quads.draw_era_sub("SCUAD")

    def a_g_cuadrado_end(self, items):
        # print("end quad of drawing")
        self.quads.draw_era_sub("ECUAD")

    def a_g_circulo_init(self, items):
        # print("init quad for drawing")
        self.quads.draw_era_sub("SCIR")

    def a_g_circulo_end(self, items):
        # print("end quad of drawing")
        self.quads.draw_era_sub("ECIR")

    def a_g_triangulo_init(self, items):
        # print("init quad for drawing")
        self.quads.draw_era_sub("STRI")
    
    def a_g_triangulo_end(self, items):
        # print("end quad of drawing")
        self.quads.draw_era_sub("ETRI")
    
    def a_g_texto_init(self, items):
        # print("init quad for drawing")
        self.quads.draw_era_sub("STXT")
    
    def a_g_texto_end(self, items):
        # print("end quad of drawing")
        self.quads.draw_era_sub("ETXT")

    def a_g_exp_param(self, items):
        # print("generate expression params for drawing")
        self.quads.draw_params()

    def a_g_draw_p_one(self, items):
        # print("increment the paramter number")
        self.quads.more_params()

    def a_g_draw_t_color(self, items):
        # print("get color of the fill")
        token = items.children[0]
        self.quads.gen_draw_quad(token)

    def a_g_draw_stroke(self, items):
        # print("hello")
        token = items.children[0]
        self.quads.gen_draw_quad(token)

    def a_g_draw_txt_body(self, items):
        # print("Add text as a parameter")
        token = items.children[1]
        self.quads.gen_draw_quad(token)

    def a_g_main(self, items):
        # print("fill goto main the first quad")
        self.f_table.add_function(items.children[0].value)
        self.quads.fill_main()

    def first_token(self, items):
        if hasattr(items, 'children'):
            return self.first_token(items.children[0])
        return items;