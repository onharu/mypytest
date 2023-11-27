#class MyVisitor(mypy.visitor.NodeVisitor[None], CheckerPluginInterface):
#    type_checker : mypy.checker.TypeChecker
#
#    def __init__(self, checker:mypy.checker.TypeChecker):
#        #print("init success")
#        self.type_checker = checker
#    
#    def visit_func_def(self, defn: mypy.nodes.FuncDef) -> None:
#        #print("visit def")
#        defn.body.accept(self)
#
#    def visit_block(self, b: mypy.nodes.Block) -> None:
#        #print("visit block")
#        for s in b.body:
#            s.accept(self)
#
#    def visit_return_stmt(self, s :mypy.nodes.ReturnStmt) -> None:
#        #print("visit return stmt")
#        s.expr.accept(self)
#        #print(s.expr.accept(self.type_checker.expr_checker))
#        t = s.expr.accept(self.type_checker.expr_checker) 
#        #print("printing class of:" + str(t))
#        #print(type(t))  # mypy.types.Instance
#        if isinstance(t, mypy.types.Instance):
#            print(t.type.defn.name)
#            #print("printing class of t.args:" + str(t.args))
#            #print(type(t.args))
#        pass
#        '''
#        if s.expr is not None:
#            print(type(s.expr.accept(self.type_checker.expr_checker)))
#        pass
#'''
#
#    #addition
#    #for文
#    def visit_for_stmt(self, f: mypy.nodes.ForStmt) -> None:
#        #print("visit for")
#        f.body.accept(self)
#    #if文
#    def visit_if_stmt(self, i: mypy.nodes.IfStmt) -> None:
#        #print("visit if")
#        for i0 in i.body:
#            i0.accept(self)
#        if i.else_body is not None:
#            i.else_body.accept(self)
#    #代入文
#    def visit_assignment_stmt(self, a: mypy.nodes.AssignmentStmt) -> None:
#        #print("visit assign")
#        t = a.rvalue.accept(self.type_checker.expr_checker)
#        #print("printing class of:" + str(t)) 
#        #print(type(t))  # mypy.types.Instance
#        if isinstance(t, mypy.types.Instance):
#            t0 = t.type.defn.name
#            #print(t0)
#            #print("printing class of t.args:" + str(t.args[1]))
#            print(type(t))
#
#
#
#    def visit_expression_stmt(self, e: mypy.nodes.ExpressionStmt) -> None:
#        print("visit expr_stmt")
#        if isinstance(e.expr,mypy.nodes.CallExpr):
#            callee = e.expr.callee
#            if isinstance(callee, mypy.nodes.NameExpr):
#                #print(str(callee.name))
#                #sprint(type(e))
#                if str(callee.name) == "check":
#                    print("visit check")
#                    role = help_func.nameExpr(e.expr.args[1])
#                    p = pro_e.projection_exp(e.expr.args[0],role,self.type_checker)
#                    print(type(e.expr.args[1]))
#                    print("printing  "+str(p))
#    
#
#
#
#
'''
    def roleof(self, e:mypy.nodes.Expression) -> str:
        t = e.accept(self.type_checker.expr_checker)
        if isinstance(t,mypy.types.Instance):
            t0 = str(t.args[0])
            return t0
        else:
            raise Exception("error")
'''

# If文 nest version
#def projection_if(#一番後ろのブロックのif文の処理
#        r:str,
#        exp:mypy.nodes.Expression,
#        body:mypy.nodes.Block,
#        else_projected:Stmt,
#        tc:mypy.checker.TypeChecker
#        ) -> Stmt:
#    body_projected = projection_block(body.body,r,tc) # body:Block, body.body:list[Statement]
#    if r in rolesOf(exp,tc):# expのロール内にプロジェクトするロールがある場合
#        expr = pro_e.projection_exp(exp,r,tc)
#        return If_else(expr,Block(body_projected),else_projected)
#    else:
#        return merge(body_projected,else_projected)
#    
#def projection_if_elif(#if文全体の処理（else節処理済み）
#        r:str,
#        exps:list[mypy.nodes.Expression],
#        bodies:list[mypy.nodes.Block],
#        else_projected:Stmt,
#        tc:mypy.checker.TypeChecker
#        ):
#    assert len(exps) == len(bodies)
#    if len(exps)==0:
#        return else_projected
#    else:
#        exp = exps[-1] # [-1]でリストの末尾の要素を取れる
#        exprs_rest = exps[:-1] # [:-1]で末尾の手前の要素から順に処理
#        body = bodies[-1]
#        bodies_rest = bodies[:-1]
#        el = projection_if(r, exp, body, else_projected,tc)
#        return projection_if_elif(r, exprs_rest, bodies_rest, el, tc)
#    
#def projection_if_elif_main(
#        r:str,
#        exprs:list[mypy.nodes.Expression], 
#        bodies:list[mypy.nodes.Block], 
#        else_stm:mypy.nodes.Block,
#        tc:mypy.checker.TypeChecker
#        ):
#  else_projected = projection_block(else_stm.body,r,tc)
#  return projection_if_elif(r, exprs, bodies, else_projected,tc)
#
#if s.else_body is None:
        #    raise Exception
        #return projection_if_elif_main(r,s.expr,s.body,s.else_body,tc) # else_bodyはblockなのだが、今はStmt型になっている

list = [1,2,3,4,5]
for i in range(len(list)):
  i = i + 5
  print(i)
print(list)
