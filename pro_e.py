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
    #literal(role付き)
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
            elif isinstance(n.left,mypy.nodes.OpExpr):
                return projection_exp(n.left,r,tc)
            else:
                raise Exception
        else:#二項演算 (+ - * / %)
            if r in help_func.rolesOf(n.left,tc) and r in help_func.rolesOf(n.right,tc):
                return projection_exp(n.left,r,tc) + str(n.op) + projection_exp(n.right,r,tc)
            else:
                return "Unit.id("  + projection_exp(n.left,r,tc)+","+ projection_exp(n.right,r,tc) +" )" 
        #else:#literalで＠がないのは例外扱いする
        #    raise Exception
    #比較演算子 (二つの式の比較限定)
    elif isinstance(n,mypy.nodes.ComparisonExpr):
        assert len(n.operators)==1
        assert len(n.operands)==2
        if n.operators[0] == ">" or ">=" or "==" or "<" or "<=" or "!=" or "and":
            left = projection_exp(n.operands[0],r,tc)
            right = projection_exp(n.operands[1],r,tc)
            return left+n.operators[0]+right
        else:
            raise Exception

    #関数呼び出し、メソッド呼び出し、クラス定義
    elif isinstance(n, mypy.nodes.CallExpr):
        #関数 f = variable
        if isinstance(n.callee, mypy.nodes.NameExpr): 
            exp_list:list[str] = []
            if r in help_func.rolesOf(n,tc): #f(Exp)のroleとprojection_expのroleが一致する時
                for exp_i in n.args:
                    exp_list.append(projection_exp(exp_i,r,tc))
                exp_var = ','.join(exp_list)
                return str(n.callee) + exp_var
            else:#f(Exp)のroleとprojection_expのroleが一致しない時
                for exp_i in n.args:
                    if r in help_func.rolesOf(exp_i,tc):
                        exp_list.append(projection_exp(exp_i,r,tc))
                    else:
                        n.args.remove(exp_i)
                exp_var = ','.join(exp_list)
                return "Unit.id(" + str(n.callee) + exp_var + ")"
                #if r in help_func.rolesOf(n.args,tc):
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
            if r in help_func.rolesOf(n,tc): # R in e.f(e')
                for exp_i in n.args:
                    exp_list_i.append(projection_exp(exp_i ,r,tc))
                exp_var_i = ','.join(exp_list_i)
                #for j in n.callee.expr:
                #    exp_list_j.append(projection_exp(n.callee.expr[j],r,tc))
                #exp_var_j = ','.join(exp_list_j)
                return projection_exp(n.callee.expr,r,tc) + "." + n.callee.name + "(" + exp_var_i + ")"
            else: # R not in e.f(e')
                if r in help_func.rolesOf(n.callee.expr,tc): # R in e
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
    elif isinstance(n,mypy.nodes.IntExpr):
        return str(n.value)

    else:
        raise Exception