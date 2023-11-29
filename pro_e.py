#import sys
#import mypycustom
#import mypytest
import mypy
#import mypy.build
import mypy.visitor
import mypy.nodes
import mypy.checker
import mypy.types
#from mypy.plugin import CheckerPluginInterface
#from typing import Optional, cast
import mypy.type_visitor
import help_func

#def projection_exps(n:list[mypy.nodes.Expression],r:str,tc:mypy.checker.TypeChecker) -> list[str]:
#    if isinstance(n,mypy.nodes.TupleExpr):
#        tuple_list:list[str] = []
#        for e in n.items:
#            te = projection_exp(e,r,tc)
#            tuple_list += [te]
#        return tuple_list
#    else:
#        raise Exception
    

def projection_exp(n:mypy.nodes.Expression,r:str,tc:mypy.checker.TypeChecker) -> str:
    #literal
    if isinstance(n, mypy.nodes.OpExpr):
        if n.op == "@":
            #print(n)
            if isinstance(n.left,mypy.nodes.IntExpr) or isinstance(n.left,mypy.nodes.FloatExpr) or isinstance(n.left,mypy.nodes.StrExpr): # 1@A
                if help_func.nameExpr(n.right) == r:
                    return str(n.left.value)
                else:
                    return "Unit.id"
            #None,True,Falseは？
            elif isinstance(n.left, mypy.nodes.NameExpr):
                if help_func.nameExpr(n.right) == r:
                    return str(n.left.name)
                else:
                    return "Unit.id"
            else:
                raise Exception
        else:#literalで＠がないのは例外扱いする
            raise Exception
        #else:#比較演算子
        #    if r in rolesOf(n.left,tc) and r in rolesOf(n.right,tc):
        #        return projection_exp(n.left,r,tc) + str(n.op) + projection_exp(n.right,r,tc)
        #    else:
        #        return "Unit.id("  + projection_exp(n.left,r,tc)+","+ projection_exp(n.right,r,tc) +" )" 
    #関数呼び出し、メソッド呼び出し、クラス定義
    elif isinstance(n, mypy.nodes.CallExpr):
        #関数 f = variable
        if isinstance(n.callee, mypy.nodes.NameExpr): 
            exp_list:list[str] = []
            if r in rolesOf(n,tc): #f(Exp)のroleとprojection_expのroleが一致する時
                for exp_i in n.args:
                    exp_list.append(projection_exp(exp_i,r,tc))
                exp_var = ','.join(exp_list)
                return str(n.callee) + exp_var
            else:#f(Exp)のroleとprojection_expのroleが一致しない時
                for exp_i in n.args:
                    if r in rolesOf(exp_i,tc):
                        exp_list.append(projection_exp(exp_i,r,tc))
                    else:
                        n.args.remove(exp_i)
                exp_var = ','.join(exp_list)
                return "Unit.id(" + str(n.callee) + exp_var + ")"
                #if r in rolesOf(n.args,tc):
                #    for exp_i in n.args:
                #        exp_list.append(projection_exp(exp_i ,r,tc))
                #    exp_var = ','.join(exp_list)
                #    return "Unit.id(" + str(n.callee) + exp_var + ")"
                #else:
                #    for exp_i in n.args:
                #        exp_list.append(projection_exp(exp_i ,r,tc))
                #    exp_var = ','.join(exp_list)
                #    return "Unit.id(" + exp_var + ")"
        #method呼び出し f = memberexpr
        elif isinstance(n.callee, mypy.nodes.MemberExpr):
            exp_list_i = []
            #exp_list_j = []
            if r in rolesOf(n,tc): # R in e.f(e')
                for exp_i in n.args:
                    exp_list_i.append(projection_exp(exp_i ,r,tc))
                exp_var_i = ','.join(exp_list_i)
                #for j in n.callee.expr:
                #    exp_list_j.append(projection_exp(n.callee.expr[j],r,tc))
                #exp_var_j = ','.join(exp_list_j)
                return projection_exp(n.callee.expr,r,tc) + "." + n.callee.name + "(" + exp_var_i + ")"
            else: # R not in e.f(e')
                if r in rolesOf(n.callee.expr,tc): # R in e
                    for exp_i in n.args:
                        exp_list_i.append(projection_exp(exp_i ,r,tc))
                    exp_var_i = ','.join(exp_list_i)
                    #for j in n.callee.expr:
                    #    exp_list_j.append(projection_exp(n.callee.expr[j],r,tc))
                    #exp_var_j = ','.join(exp_list_j)
                    return "Unit.id(" + projection_exp(n.callee.expr,r,tc) + "." + n.callee.name + "(" + exp_var_i + "))"
                else: # R not in e
                    for exp_i in n.args:
                        exp_list_i.append(projection_exp(exp_i ,r,tc))
                    exp_var_i = ','.join(exp_list_i)
                    #for j in n.callee.expr:
                    #    exp_list_j.append(projection_exp(n.callee.expr[j],r,tc))
                    #exp_var_j = ','.join(exp_list_j)
                    return "Unit.id(" + projection_exp(n.callee.expr,r,tc) + "," + exp_var_i + ")"
        # クラス定義
        #print("type :" + str(type(n.callee)))
        elif isinstance(n.callee, mypy.nodes.IndexExpr):
            exp_list = []
            print('type: ' + str(type(n.callee.index)))
            #if isinstance(n.callee.index,mypy.nodes.NameExpr):
            if r == help_func.nameExpr(n.callee.index):
                for exp_i in n.args:
                    exp_list.append(projection_exp(exp_i ,r,tc))
                exp_var = ','.join(exp_list)
                return help_func.nameExpr(n.callee.base) + "_" + r + "(" + exp_var + ")"
            else: # R not in Roles
                for exp_i in n.args:
                    exp_list.append(projection_exp(exp_i ,r,tc))
                exp_var = ','.join(exp_list)
                return "Unit.id(" + exp_var + ")" 
        else:
            raise Exception
    elif isinstance(n,mypy.nodes.NameExpr):
        return n.name
    else:
        raise Exception
 
        
def rolesOf(n:mypy.nodes.Expression, typeChecker:mypy.checker.TypeChecker) -> set[str]:
    t0 = n.accept(typeChecker.expr_checker) #nの型情報を取得する
    print(t0)
    if isinstance(t0, mypy.types.Instance): #Expression → Instance
        if t0.type.defn.name == "At":
            roleName = set(str([t0.args[1]])) # At[int,A]でいうところのA
            return roleName
        else:
            raise Exception
    else:
        raise Exception