import mypy
import mypy.visitor
import mypy.nodes
import mypy.checker
import mypy.types
from enum import Enum
import mypy.type_visitor
from pro_e import *
from help_func import *
import mypy.patterns
import ast
#import help_func
from typing import TypeVar

#import sys
#import mypycustom
#import mypytest
#import mypy.build
#from mypy.plugin import CheckerPluginInterface
#from typing import Optional, cast
#from pro_e import projection_exp

# Lvalue = Union['NameExpr', 'MemberExpr', 'IndexExpr', 'SuperExpr', 'StarExpr','TupleExpr']; 
Lvalue: mypy.nodes._TypeAlias = mypy.nodes.Expression
Self = TypeVar("Self")

# 構文木
class Stmt:
    pass

class Block(Stmt): # list[stm]
    def __init__(
            self,
            body:list[Stmt]
    ):
        super().__init__() 
        #    サブクラスで__init__を定義すると、親クラスの__init__が上書きされる
        # -> super().__init__()で親クラスの__init__と同様の処理が可能
        # -> 今回は親クラスのStmtに__init__がないためなくても良い
        self.body = body
    def __repr__(self):
        return f"{self.body}"

class Pass(Stmt):
    def __repr__(self):
        return f"pass"


class Return(Stmt):
    def __init__(self, exp:str):
        self.expr = exp

class Es(Stmt): # e1; s
    def __init__(self, exp:str):
        self.expr = exp
    def __repr__(self):
        return f"{self.expr}"

class Asg(Stmt): # id:TE = e; s
    def __init__(
            self, 
            #lv:list[str], assignment変更前
            lv:str,
            rv:str,
            type:mypy.types.Type | None, 
            ):
        self.lvalues = lv
        self.rvalue = rv
        self.type = type
    def __repr__(self):
        return f"{self.lvalues} = {self.rvalue}"
        #if self.type is None:
        #    return f"{self.lvalues} = {self.rvalue}"
        #else:
        #    return f"{self.lvalues} : {self.type} = {self.rvalue}"
        
class OpAsg(Stmt): # e1 Asgop e2; s
    def __init__(
            self, 
            lv:str, 
            rv:str, 
            op:str, 
            ):
        self.lvalue = lv
        self.rvalue = rv
        self.op = op
    def __repr__(self):
        return f"{self.lvalue} {self.op} {self.rvalue}"
        
class If(Stmt): # if e1:s1; else:s2; s
    def __init__(
            self, 
            exp:list[str], 
            body:list[Block], 
            else_body:Block, 
            
            ):
        self.expr = exp
        self.body = body
        self.else_body = else_body
    def __repr__(self):
        #b_str = ""
        #b_str += list_to_str(self.body[0].body)
        #for block in self.body[1:]:
        #    b_to_str = list_to_str(block.body)
        #    b_str = b_str + "elif:\n     " +b_to_str
        #if len(self.expr) == 1:
        #    return f"if {self.expr[0]}:\n    {self.body[0]}\nelse:\n    {self.else_body}"
        #if len(self.expr) == 2:
        return f"if {list_to_str(self.expr)}:\n    {list_to_str(self.body[0].body)} \nelse:\n    {list_to_str(self.else_body.body)}"
            #return f"if {self.expr[0]}:\n    {self.body[0]}\nelif {self.expr[1:]}:\n    {self.body[1:]}\nelse:\n    {self.else_body}"
        


#class If_else(Stmt):
#    def __init__(
#            self,
#            exp:str,
#            body:Block,
#            else_body: Stmt
#        ):
#        self.exp = exp
#        self.body = body
#        self.else_body = else_body

class Match(Stmt): # match
    def __init__(
            self, 
            sub:str, 
            pat:list[str],#list[mypy.patterns.ValuePattern.expr], 
            #guards:list[str | None], 
            bodies:list[Block], 
            
            ):
        self.subject = sub
        self.patterns = pat
        #self.guards = guards
        self.bodies = bodies

class Raise(Stmt): # raise
    def __init__(self, expr:str | None):#, from_expr:str | None):
        self.expr = expr
        #self.from_expr = from_expr

class Assert(Stmt): # assert
    expr:str
    def __init__(self,expr:str):
        self.expr = expr
    def __repr__(self):
        return f"assert {self.expr}"



#block
def projection_block(s_list:list[mypy.nodes.Statement],r:str,tc:mypy.checker.TypeChecker)-> list[Stmt]:
    #for i in range(len(s_list)):
    if s_list == []:
        return []
    else:
        #print(len(s_list))
        s = s_list[0]
        # 分岐あり(e;s -> match)
        if isinstance(s,mypy.nodes.ExpressionStmt):
            t = s.expr.accept(tc.expr_checker) # 型情報入手
            if isinstance(t,mypy.types.Instance) and \
                "enum" in t.type.defn.name and \
                    r in rolesOf(s.expr,tc) and \
                        isinstance(s.expr,mypy.nodes.CallExpr) and \
                            isinstance(s.expr.callee,mypy.nodes.MemberExpr) and \
                                s.expr.callee.name == "select":# enum型かつロールが合っているかつメソッド名がselectのとき
                if len(s.expr.args) == 1:# args:list[expression] <- このリストの要素は一つしかあり得ない
                    pro_args = projection_exp(s.expr.args[0],r,tc)
                    return [Match(projection_exp(s.expr,r,tc),[pro_args],[Block(projection_block(s_list[1:],r,tc))])]
                else:
                    raise Exception
            else:
                raise Exception
        else:# 分岐がない単一の文
            #print(s)
            return [projection_stm(s,r,tc)] + projection_block(s_list[1:],r,tc) # それぞれの文をプロジェクションする
    #assert False



# projection Statement（単一の文）
def projection_stm(s:mypy.nodes.Statement,r:str,tc:mypy.checker.TypeChecker) -> Stmt:
    #Pass
    if isinstance(s,mypy.nodes.PassStmt):
        return Pass()
    #Return
    elif isinstance(s,mypy.nodes.ReturnStmt):
        if s.expr is None:
            raise Exception
        exp = projection_exp(s.expr,r,tc)
        return Return(exp) 
    #Assignment変更前
    #elif isinstance(s,mypy.nodes.AssignmentStmt):
    #    lv = s.lvalues
    #    lv_pro:list[str] = []
    #    for i in range(len(lv)):
    #        l = projection_exp(lv[i],r,tc)
    #        lv_pro += [l] 
    #        rvs = projection_exp(s.rvalue,r,tc)
    #        t = s.type
    #        if t is None and r in rolesOf(s.rvalue,tc):#型を明示していない場合（型推論で行う場合）
    #            return Asg(lv_pro,rvs,t)
    #        elif t is None and r not in rolesOf(s.rvalue,tc):
    #            return Es(rvs)
    #        else:#型明示
    #            if r in rolesOf_t(t,tc): 
    #                return Asg(lv_pro,rvs,t) 
    #            else:
    #                return Es(rvs) 
    #    else:
    #        raise Exception
        
    #Assinment変更後
    elif isinstance(s,mypy.nodes.AssignmentStmt):
        lv = s.lvalues
        if len(lv) == 1:
            l = projection_exp(lv[0],r,tc)
            rvs = projection_exp(s.rvalue,r,tc)
            t = s.type
            if t is None and r in rolesOf(s.rvalue,tc):#型を明示していない場合（型推論で行う場合）
                return Asg(l,rvs,t)
            elif t is None and r not in rolesOf(s.rvalue,tc):
                return Es(rvs)
            else:#型明示
                if r in rolesOf_t(t,tc): 
                    return Asg(l,rvs,t) 
                else:
                    return Es(rvs) 
        else:
            raise Exception
        
    #OperatorAssignment
    elif isinstance(s,mypy.nodes.OperatorAssignmentStmt):
        l = projection_exp(s.lvalue,r,tc)
        rv = projection_exp(s.rvalue,r,tc)
        return OpAsg(l,rv,s.op)
    #if
    elif isinstance(s,mypy.nodes.IfStmt):
        assert len(s.expr)==len(s.body)
        exprs_projected:list[str] = []
        bodies_projected:list[Block] = []
        for i in range(len(s.expr)):
            exp = projection_exp(s.expr[i],r,tc)
            stm = projection_block(s.body[i].body,r,tc)
            exprs_projected += [exp]
            bodies_projected += [Block(stm)]
        if s.else_body is None:
            raise Exception
        else_projected = projection_block(s.else_body.body,r,tc)
        return If(exprs_projected,bodies_projected,Block(else_projected))
    #Es
    elif isinstance(s,mypy.nodes.ExpressionStmt):
        exp = projection_exp(s.expr,r,tc)
        return Es(exp)
    #raise
    elif isinstance(s,mypy.nodes.RaiseStmt):
        if s.expr is None:
            raise Exception
        exp = projection_exp(s.expr,r,tc)
        return Raise(exp)
    #assert
    elif isinstance(s,mypy.nodes.AssertStmt):
        exp = projection_exp(s.expr,r,tc)
        return Assert(exp)

    #import
    #elif isinstance(s,mypy.nodes.ImportAll):
    #    return ImportAll(s.id,s.relative)
    #others
    else:
        raise Exception("unexpected syntax",s)

    

def merge_exp(e1:str,e2:str) -> str:
    if e1 == e2:
        return e1
    else:
        raise Exception

# merging
# 同じstm,expはそのまま残す,後に続くStmも同じでないとマージされない
def merge(s1:Stmt, s2:Stmt) -> Stmt: 
    # Block (list[stm])
    if isinstance(s1,Block) and isinstance(s2,Block):
        #merge_list:list[Stmt] = []
        # listの要素にマージの再帰を定義する
        # s=[s1, s2, s3 ...]  s'=[s1', s2', s3' ...]のとき
        # s ⊔ s' = [s1 ⊔ s1', s2 ⊔ s2', s3 ⊔ s3', ...]
        for t1 in s1.body:
            for t2 in s2.body:
                ms = merge(t1,t2)
        return ms
                #merge_list += [merge(t1,t2)]
        #return merge_list    
    # return
    elif isinstance(s1,Return) and isinstance(s2,Return):
        if s1.expr == s2.expr:
            return s1
        else:
            raise Exception
    # AsgOp
    elif isinstance(s1,OpAsg) and isinstance(s2,OpAsg):
        if s1.lvalue == s2.lvalue and s1.rvalue == s2.rvalue:
            return OpAsg(s1.lvalue,s1.rvalue,s1.op)
        else:
            raise Exception #merge(s1.stmt,s2.stmt)
    # e;s
    elif isinstance(s1,Es) and isinstance(s2,Es):
        if s1.expr == s2.expr:
            return s1
        else:
            raise Exception
    # if
    elif isinstance(s1,If) and isinstance(s2,If):
        exps:list[str] = []
        stms:list[Block] = []
        assert len(s1.expr) == len(s2.expr) and len(s1.expr) == len(s1.body) and len(s2.expr) == len(s2.body)# if文に直す
        if len(s1.expr) == 0:
            else_stm = Block([merge(s1.else_body,s2.else_body)])
        else:# len(s1.expr) != 0
            for i in range(len(s1.expr)):
                exp1 = s1.expr[i]
                exp2 = s2.expr[i]
                stm1 = s1.body[i]
                stm2 = s2.body[i]
                exps += [merge_exp(exp1,exp2)]
                stms += [Block([merge(normalize(stm1),normalize(stm2))])]
        return If(exps,stms,else_stm)
    # match
    elif isinstance(s1,Match) and isinstance(s2,Match):
        # guards:list[expression]
        # bodies: list[statement]
        # guardsが被ったらbodiesをマージして、被ってないならlistに加える
        # -> 新たなguards,bodiesとして定義し直せばいい
        if s1.subject == s2.subject:
            stm_list:list[Block] = [] # merge後のbodies
            newpatterns:list[str] = [] #merge後のpatterns
            # s1の各patternとs2のpatternを比較する
            for i in range(len(s1.patterns)):
                pat1 = s1.patterns[i]
                for j in range(len(s2.patterns)):
                    pat2 = s2.patterns[j]
                    if pat1 == pat2: #同じpatternならStmをmergeする
                        mbodies = merge(s1.bodies[i],s2.bodies[j])
                        stm_list += [Block([mbodies])]
                        newpatterns += [pat1]
                        # mergeしたものの元の要素は削除
                        s1.patterns.remove(pat1)
                        s1.bodies.remove(s1.bodies[i])
                        s2.patterns.remove(pat2)
                        s2.bodies.remove(s1.bodies[j])
            # patternが一致しなくて残ったものをリストに加える
            all_patterns = newpatterns + s1.patterns + s2.patterns
            all_stm = stm_list + s1.bodies + s2.bodies
            return Match(s1.subject,all_patterns,all_stm) 
        else:
            raise Exception
    # Raise
    elif isinstance(s1,Raise) and isinstance(s2,Raise):
        if s1.expr == s2.expr:
            return s1
        else:
            raise Exception
    #others
    else:
        raise Exception
            
                

        
        #if s1.expr == s2.expr:
        #    return If(s1.expr,merge(s1.body,s2.body),merge(s1.else_body,s2.else_body))
        #else:
        #    raise Exception
    

# Noop
def noop(exp:str):# 射影後のExpression(String型)
    if "Unit.id" in exp:
        return "" # blank
    else:
        return exp # そのまま値を返す

#normalizing
def normalize(s:Stmt) -> Stmt: 
    if isinstance(s, Pass): # pass
        return s
    elif isinstance(s, Return): # return 
        return s
    elif isinstance(s, Es): # expressionStmt
        # ここでは stmt.expr が削る対象だったら s.stmt を return する
        return Es("")
    elif isinstance(s,OpAsg): # operator assignment
        if noop(s.lvalue) == noop(s.rvalue) == "":
            return OpAsg("","","")
        elif noop(s.lvalue) == "" and noop(s.rvalue) != "":
            return Es(s.rvalue)
        elif noop(s.lvalue) != "" and noop(s.rvalue) == "":
            return Es(s.lvalue)
        else: # noop(s.lvalue) != "" and noop(s.rvalue) != "":
            return s
    #elif isinstance(s,If):
    #elif isinstance(s,Match):


        
    #elif isinstance(s,OpAsg):
    #    if noop(s.rvalue)
    # elif...
    assert False
