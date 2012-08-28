#-*- coding: utf8 -*-
import ast
import operator as op
import random
import threading

CHOICES = range(1, 10) + [10, 25, 50, 75]
NB_OPERANDS = 6

class CalcError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

# supported operators
operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
             ast.Div: op.div}

class Chiffres:
    def __init__(self):
        self.total = random.randint(200, 800)
        self.digits = []
        i = 0
        while i < NB_OPERANDS:
            i += 1
            self.digits.append(random.choice(CHOICES))
        self.digits = sorted(self.digits)

    def solve(self):
        self.best = 0
        self.best_stack = []

        def compte(digits, result, stack = []):

            if len(digits) == 1 and digits[0] == result:
                return (True, stack)

            elif len(digits) == 1 :
               if abs(result - digits[0]) < abs(result - self.best) :
                   self.best =  digits[0]
                   self.best_stack = stack[:]

            for idx, i in enumerate(digits) :
                for j in digits[idx+1:] :
                    new_digits = digits[:]
                    new_digits.remove(i)
                    new_digits.remove(j)

                    i,j = max(i,j), min(i,j)

                    b,s = compte(new_digits+[i+j],result,stack+['%s + %s = %s' % (i,j, i+j)])
                    if b : return (True, s)

                    b,s = compte(new_digits+[i*j],result,stack+['%s * %s = %s' % (i,j, i*j)])
                    if b : return (True, s)

                    if i != j :
                        b,s = compte(new_digits+[i-j],result,stack+['%s - %s = %s' % (i,j, i-j)])
                        if b : return (True,s)

                    if i%j == 0 :
                        b,s = compte(new_digits+[i/j],result,stack+['%s / %s = %s' % (i,j, i/j)])
                        if b : return (True, s)

            return (False, stack)
        
        exact, res = compte(self.digits, self.total, []) 

        if not exact:
            res = self.best_stack

        return exact, "\n".join(res)

    def check(self, answer):
        self.ok_values = list(self.digits)

        def eval_expr(expr, left):
            """
            >>> eval_expr('2^6')
            4
            >>> eval_expr('2**6')
            64
            >>> eval_expr('1 + 2*3**(4^5) / (6 + -7)')
            -5.0
            """
            return eval_(ast.parse(expr).body[0].value, left)

        def eval_(node, left):
            if isinstance(node, ast.Num): # <number>
                if left:
                    try:
                        self.ok_values.remove(node.n)
                    except ValueError:
                        raise CalcError(u"Euh, tu le sors d'où le %s ???" % node.n)
                else:
                    self.ok_values.append(node.n)
                return node.n
            elif isinstance(node, ast.operator): # <operator>
                return operators[type(node)]
            elif isinstance(node, ast.BinOp): # <left> <operator> <right>
                return eval_(node.op, left)(eval_(node.left, left), eval_(node.right, left))
            else:
                raise TypeError(node)

        def check_solution(sol):
            operations = sol.split(";")
            for operation in operations:
                try:
                    left, right = operation.split("=", 2)
                except ValueError:
                    raise CalcError(u"Erreur de syntaxe dans %s" % operation)
                left = left.strip()
                right = right.strip()
                try:
                    eleft = eval_expr(left, True)
                except SyntaxError:
                    raise CalcError(u"Je n'arrive pas à calculer ça : « %s »" % left)
                try:
                    eright = eval_expr(right, False)
                except SyntaxError:
                    raise CalcError(u"Je n'arrive pas à calculer ça : « %s »" % right)
                if eleft != eright:
                    raise CalcError(u"Tu veux vraiment nous faire croire que %s = %s ???" % (left, right))
            return eval_expr(right, False)

        return check_solution(answer)

if __name__ == "__main__":
    c = Chiffres()
    print c.numbers
    print c.total
    print c.solve()
