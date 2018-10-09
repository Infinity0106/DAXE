from lark import Transformer, Tree, Token, v_args

class DaxeTransformer(Transformer):
    def __init__(self):
        print("initial transformer")

    # def g_expresion(self, items):
    #     print(items)
    #     if len(items) == 3:
    #         items.append(Tree('a_g_end_expresion',[Token('T_A_G_TOKEN','token')]))
    #     return Tree('g_expresion',items)
