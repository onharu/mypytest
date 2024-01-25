import mypy
import mypy.visitor
import mypy.nodes
import mypy.checker
import mypy.types
import mypy.type_visitor
import help_func

# Expression    
def projection_exp(n:mypy.nodes.Expression,r:str,tc:mypy.checker.TypeChecker) -> str:
    #literal(role付き)
    if isinstance(n, mypy.nodes.OpExpr):
        if n.op == "@":
            if isinstance(n.left,mypy.nodes.IntExpr) or \
                isinstance(n.left,mypy.nodes.FloatExpr): # 1@A()
                if help_func.nameExpr(n.right) == r:
                    return str(n.left.value)
                else:
                    return "Unit.id"
            elif isinstance(n.left,mypy.nodes.StrExpr): # "a"@A()
                if help_func.nameExpr(n.right) == r:
                    return '"' + n.left.value + '"'
                else:
                    return "Unit.id"
            # None,True,False
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
                return "Unit.id"+ "(" + projection_exp(n.left,r,tc)+","+ projection_exp(n.right,r,tc) +" )" 
    #比較演算子 (二つの式の比較限定)
    elif isinstance(n,mypy.nodes.ComparisonExpr):
        print("comparison")
        assert len(n.operators)==1
        assert len(n.operands)==2
        if n.operators[0] == ">" or ">=" or "==" or "<" or "<=" or "!=" or "and":
            left = projection_exp(n.operands[0],r,tc)
            right = projection_exp(n.operands[1],r,tc)
            print("left : "+left)
            print("right : "+right)
            return left+n.operators[0]+right
        else:
            raise Exception
    #field
    elif isinstance(n,mypy.nodes.MemberExpr):
        return projection_exp(n.expr,r,tc)+"."+n.name
    #関数呼び出し、メソッド呼び出し、クラス定義
    elif isinstance(n, mypy.nodes.CallExpr):
        #関数 f = variable
        if isinstance(n.callee, mypy.nodes.NameExpr): 
            exp_list:list[str] = []
            if n.callee.name == "print":
                for exp_i in n.args:
                        exp_list.append(projection_exp(exp_i,r,tc))
                        exp_var = ','.join(exp_list)
                return n.callee.name + "(" + exp_var + ")"
            else:
                #exp_list:list[str] = []
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
                    return "Unit.id"+ "(" + str(n.callee) + exp_var + ")"
        #method呼び出し f = memberexpr
        elif isinstance(n.callee, mypy.nodes.MemberExpr):
            exp_list_i = []
            if r in help_func.rolesOf(n,tc): # R in e.f(e')
                for exp_i in n.args:
                    exp_j = projection_exp(exp_i ,r,tc)
                    if exp_j == "Unit.id":
                        pass
                    else:
                        exp_list_i.append(exp_j)
                exp_var_i = ','.join(exp_list_i)
                return projection_exp(n.callee.expr,r,tc) + "." + n.callee.name + "(" + exp_var_i + ")"
            else: # R not in e.f(e')
                if r in help_func.rolesOf(n.callee.expr,tc): # R in e
                    for exp_i in n.args:
                        exp_list_i.append(projection_exp(exp_i ,r,tc))
                    exp_var_i = ','.join(exp_list_i)
                    return "Unit.id" + "(" + projection_exp(n.callee.expr,r,tc) + "." + n.callee.name + "(" + exp_var_i + "))"
                else: # R not in e
                    for exp_i in n.args:
                        exp_list_i.append(projection_exp(exp_i ,r,tc))
                    exp_var_i = ','.join(exp_list_i)
                    #return "Unit.id" + "(" + projection_exp(n.callee.expr,r,tc) + "," + exp_var_i + ")"
                    return ""
        # クラス定義
        elif isinstance(n.callee, mypy.nodes.IndexExpr):
            exp_list = []
            id_list = []
            if isinstance(n.callee.index,mypy.nodes.TupleExpr):
                for id in n.callee.index.items:
                    id1 = help_func.nameExpr(id)
                    #print(id1)
                    id_list += [id1]
                ids = ",".join(id_list)
                if r in ids: # R in Roles
                    for exp_i in n.args:
                        e = projection_exp(exp_i ,r,tc)
                        #print(e)
                        exp_list.append(e)
                    exp_var = ','.join(exp_list)
                    return help_func.nameExpr(n.callee.base) + "[" + ids + "](" + exp_var + ")"
                else: # R not in Roles
                    for exp_i in n.args:
                        exp_list.append(projection_exp(exp_i ,r,tc))
                    exp_var = ','.join(exp_list)
                    return help_func.noop("Unit.id" + "(" + exp_var + ")" )
            else:
                raise Exception
        else:
            raise Exception
    elif isinstance(n,mypy.nodes.NameExpr):
        if n.name == "self":
            return n.name
        else:
            t = help_func.get_type(tc,n)
            if r in help_func.rolesOf_t(t,tc):
                return n.name
            else:
                return "Unit.id"
    elif isinstance(n,mypy.nodes.IntExpr):
        return str(n.value)
    elif isinstance(n,mypy.nodes.StrExpr):
        return repr(n.value) # 文字列を''で囲む
    elif isinstance(n,mypy.nodes.IndexExpr):
        print("n.index : "+str(n.index))
        print("n.base : "+str(n.base))
        print("n.analyzed : "+str(n.analyzed))
        return projection_exp(n.base,r,tc)+"["+projection_exp(n.index,r,tc)+"]"
    elif isinstance(n,mypy.nodes.TupleExpr):
        item_list:list[str] = [ ]
        for exp in n.items:
            item_list.append(str(exp))
        items = ','.join(item_list)
        print("items = "+items)
        return items



    else:
        raise Exception("unexcepted syntax",n)