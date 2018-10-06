from lark import Transformer
from lark.visitors import Visitor_Recursive
from function_dir import FunctionsDir

class DaxeTransformer(Visitor_Recursive):
    def __init__(self):
        self.f_table = None

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

    def g_t_end_function(self, items):
        # print("12.Delete current VarTable it's no longer required")
        self.f_table.delete_current_var_table()
