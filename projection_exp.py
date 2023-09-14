import sys
import mypycustom
import mypytest
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

def projection_exp(n:mypy.nodes.Expression,r:str,tc:mypy.checker.TypeChecker) -> str:
    #Expression
    #if isinstance(n,mypy.nodes.Expression):
    #literal
    if isinstance(n, mypy.nodes.OpExpr):
        if n.op == "@":
            print(n)
            if isinstance(n.left,mypy.nodes.IntExpr) or isinstance(n.left,mypy.nodes.FloatExpr) or isinstance(n.left,mypy.nodes.StrExpr): # 1@A
                if help_func.nameExpr(n.right) == r:
                    return str(n.left.value)
                else:
                    return "Unit.id"
            #None,True,Falseは？
            if isinstance(n.left, mypy.nodes.NameExpr):
                if help_func.nameExpr(n.right) == r:
                    return str(n.left.name)
                else:
                    return "Unit.id"
        else:#literalで＠がないのは例外扱いする
            raise Exception
    #関数呼び出し、メソッド呼び出し、クラス定義
    if isinstance(n, mypy.nodes.CallExpr):
        #関数 f = variable
        if isinstance(n.callee, mypy.nodes.NameExpr): 
            exp_list = []
            if r in rolesOf(n,tc): #f(Exp)のroleとprojection_expのroleが一致する時
                for i in n.args:
                    exp_list.append(projection_exp(n.args[i],r,tc))
                exp_var = ','.join(exp_list)
                return str(n.callee) + exp_var
            else:#f(Exp)のroleとprojection_expのroleが一致しない時
                if r in rolesOf(n.args,tc):
                    for i in n.args:
                        exp_list.append(projection_exp(n.args[i],r,tc))
                    exp_var = ','.join(exp_list)
                    return "Unit.id(" + str(n.callee) + exp_var + ")"
                else:
                    for i in n.args:
                        exp_list.append(projection_exp(n.args[i],r,tc))
                    exp_var = ','.join(exp_list)
                    return "Unit.id(" + exp_var + ")"
        #method呼び出し f = memberexpr
        if isinstance(n.callee, mypy.nodes.MemberExpr):
            exp_list_i = []
            exp_list_j = []
            if r in rolesOf(n,tc): # R in e.f(e')
                for i in n.args:
                    exp_list_i.append(projection_exp(n.args[i],r,tc))
                exp_var_i = ','.join(exp_list_i)
                for j in n.callee.expr:
                    exp_list_j.append(projection_exp(n.callee.expr[j],r,tc))
                exp_var_j = ','.join(exp_list_j)
                return exp_var_j + "." + n.callee.name + "(" + exp_var_i + ")"
            else: # R not in e.f(e')
                if r in rolesOf(n.callee.expr,tc): # R in e
                    for i in n.args:
                        exp_list_i.append(projection_exp(n.args[i],r,tc))
                    exp_var_i = ','.join(exp_list_i)
                    for j in n.callee.expr:
                        exp_list_j.append(projection_exp(n.callee.expr[j],r,tc))
                    exp_var_j = ','.join(exp_list_j)
                    return "Unit.id(" + exp_var_j + "." + n.callee.name + "(" + exp_var_i + "))"
                else: # R not in e
                    for i in n.args:
                        exp_list_i.append(projection_exp(n.args[i],r,tc))
                    exp_var_i = ','.join(exp_list_i)
                    for j in n.callee.expr:
                        exp_list_j.append(projection_exp(n.callee.expr[j],r,tc))
                    exp_var_j = ','.join(exp_list_j)
                    return "Unit.id(" + exp_var_j + "," + exp_var_i + ")"
        # クラス定義
        #print("type :" + str(type(n.callee)))
        if isinstance(n.callee, mypy.nodes.IndexExpr):
            exp_list = []
            print('type: ' + str(type(n.callee.index)))
            #if isinstance(n.callee.index,mypy.nodes.NameExpr):
            if r == help_func.nameExpr(n.callee.index):
                for i in n.args:
                    exp_list.append(projection_exp(n.args[i],r,tc))
                exp_var = ','.join(exp_list)
                return help_func.nameExpr(n.callee.base) + "_" + r + "(" + exp_var + ")"
            else: # R not in Roles
                for i in n.args:
                    exp_list.append(projection_exp(n.args[i],r,tc))
                exp_var = ','.join(exp_list)
                return "Unit.id(" + exp_var + ")" 
    ##Statement
    #if isinstance(n,mypy.nodes.Statement):
    #    #pass
    #    if isinstance(n,mypy.nodes.PassStmt):
    #        return n
    #    #return
    #    if isinstance(n,mypy.nodes.ReturnStmt):
    #        expr = projection_exp(n.expr,r,tc)
    #        return "return " + expr
    #    #assignment
    #    if isinstance(n,mypy.nodes.AssignmentStmt):
    #        if r in rolesOf(n.type):
    #            rexp = projection_exp(n.rvalue, r, tc)
    #            return str(n.lvalues) + ":" + str(n.type) + "=" + rexp
    #        else:
    #            return rexp
    #    #OperatorAssignmentStmt
    #    if isinstance(n,mypy.nodes.OperatorAssignmentStmt):
    #        lexp = projection_exp(n.lvalue, r, tc)
    #        rexp = projection_exp(n.rvalue, r, tc)
    #        return lexp + str(n.op) + rexp #normalizerを適用する必要あり
    #    #ExpressionStmt
    #    if isinstance(n,mypy.nodes.ExpressionStmt):
    #        if isinstance(n.expr,mypy.nodes.CallExpr):
    #            if isinstance(n.expr.callee,mypy.nodes.MemberExpr):#method呼び出し
    #                f = n.expr.callee.name
    #                if f == "select":#selectionmethod -> match文
    #                    
#








        #Exp;Stm 


 
        
def rolesOf(n:mypy.nodes.Expression, typeChecker:mypy.checker.TypeChecker) -> set[str]:
    t0 = n.accept(typeChecker.expr_checker) #nの型情報を取得する
    if isinstance(t0, mypy.types.Instance): #Expression → Instance
        if t0.type.defn.name == "At":
            roleName = set([t0.args[1]]) # At[int,A]でいうところのA
            return roleName
        else:
            raise Exception

        
        
    #if isinstance(n,mypy.nodes.MemberExpr):
    #    rolesOf(n.expr,t)

            
    
    