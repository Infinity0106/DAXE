from lark.visitors import Visitor_Recursive
from function_dir import FunctionsDir
from quadruplets import Quadruplets

class DaxeVisitor(Visitor_Recursive):
    def __init__(self):
        self.f_table = None
        self.quads = Quadruplets()

    def a_t_programa(self, items):
        # print("1.Create DirFunc")
        self.f_table = FunctionsDir()

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
        del self.f_table

    def a_t_fun(self, items):
        #TODO: nothing to prepare
        print("7.Prepare DirFunc to add new function")

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

    def a_t_end_function(self, items):
        # print("12.Delete current VarTable it's no longer required")
        self.f_table.delete_current_var_table()

    def a_g_end_expresion(self, items):
        print("9. if poper.top() == rel.op then procede with 4 but different")
        self.quads.algorithm_with([">","<","==",">=","<=","<>"])

    def a_g_relacional(self, items):
        print("8. poper.push(rel.op)")
        token = items.children[0].children[0]
        self.quads.add_operator(token.value)

    def a_g_exp_1(self, items):
        print("2. poper.push(+ or -)")
        token = items.children[0].children[0]
        self.quads.add_operator(token.value)
    
    def a_g_exp_term(self, items):
        print("4. all process with + or -")
        self.quads.algorithm_with(["-","+"])

    def a_g_termino_1(self, items):
        print("3. poper.push(* or /")
        token = items.children[0].children[0]
        self.quads.add_operator(token.value)
    
    def a_g_termino_term(self, items):
        print("5. all process with * or /")
        self.quads.algorithm_with(["*","/"])
    
    def a_g_factor_left_par(self, items):
        print("6. poper.push(false bottom)")
        self.quads.add_operator("(")

    def a_g_factor_right_par(self, items):
        print("7. poper.pop(false bottom)")
        self.quads.pop_operator()

    def a_g_var_cte(self, items):
        print("1. pilao.push(id.name) and ptypes.push(id.type)")
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
            if(items.children[0].type == 'T_NUM_INT'):
                id_name = items.children[0]
                type = "entero"
            if(items.children[0].type == 'T_NUM_FLOAT'):
                id_name = items.children[0]
                type = "decimal"
        self.quads.add_id(id_name, type)

    def a_g_asignacion(self, items):
        print("10. agregar id de la asignacion")
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
        print("11 agregar = en operadores")
        token = items.children[0]
        self.quads.add_operator(token.value)

    def a_g_end_asignacion(self, items):
        print("12 validar si hay un =")
        self.quads.algorithm_with(["="])

    def a_g_escritura(self, items):
        print("add key of printing")
        self.quads.gen_custom_quad("PRINT")

    def a_g_dibujar_rotar(self, items):
        print("generate quad at the end for rotation movement")
        self.quads.gen_custom_quad("ROT")

    def a_g_dibujar_adelante(self, items):
        print("generate quad at the end for forward movement")
        self.quads.gen_custom_quad("MOVF")

    def a_g_condicional_1(self, items):
        print("""1. exp_type = PTypes.pop()
                if(exp_type != bool) error
                else
                    result = pilao.pop()
                    generate_quad gotoF, result, None, ____
                    Pjumps.push(count-1)
                """)
        token = items.children[0]
        self.quads.start_if(token)

    def a_g_condicional_2(self, items):
        print("end = pjumps.pop(); fill(end, counter)")
        self.quads.end_if()

    def a_g_condicional_3(self, items):
        print("""gen GOTO
                false = pjumps.pop()
                pjumps.push(count-1)
                fill(false, count)""")
        self.quads.else_if()

    def a_g_ciclo_start(self, items):
        print("pjumps.push(count)")
        self.quads.while_start()

    def a_g_ciclo_mid(self, items):
        print("""exp_type=ptypes.pop()
                if(exp_type != bool) error
                result = pilao.pop
                genquad gotof, result, none, none
                pjumps.push(count-1)
        """)
        token = items.children[0]
        self.quads.while_mid(token)

    def a_g_ciclo_end(self, items):
        print("""end = pjumps.pop
                return = pjumps.pop
                gen goto ,none,none,return
                fill(end, count)""")
        self.quads.while_end()

