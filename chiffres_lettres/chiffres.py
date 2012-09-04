#-*- coding: utf8 -*-
""" Module to define the 'countdown' game """
import ast
import operator as op
import random

CHOICES = range(1, 10) + [10, 25, 50, 75, 100]
NB_OPERANDS = 6


class CalcError(Exception):
    """ Exception raised when a solution is not valid """
    def __init__(self, message):
        Exception.__init__(self, message)

# supported operators
def mydiv(a, b) :
    if a % b == 0 :
        return op.div(a, b)
    else :
        raise CalcError("%d n'est pas divisible par %d, escroc" % (a, b))

operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
             ast.Div: mydiv}


class Chiffres:
    """ The game Countdown main class """

    def __init__(self):
        self.total = random.randint(100, 999)
        self.digits = []
        i = 0
        while i < NB_OPERANDS:
            i += 1
            self.digits.append(random.choice(CHOICES))
        self.digits = sorted(self.digits)

    def solve(self):
        """ Finds the best solution for the game """
        self.best = 0
        self.best_stack = []

        def compte(digits, result, stack):
            """ Recursive auxiliary function to solve the problem """

            if result in digits:
                return (True, stack)

            goal = abs(result - self.best)
            for digit in digits:
                if abs(result - digit) < goal:
                    self.best = digit
                    self.best_stack = stack[:]

            for idx, g in enumerate(digits):
                for h in digits[idx + 1:]:
                    new_digits = digits[:]
                    new_digits.remove(g)
                    new_digits.remove(h)

                    i, j = max(g, h), min(g, h)

                    exact, solution = compte(new_digits + [i + j],
                                             result,
                                             stack + ['%s + %s = %s' % (i, j, i + j)])
                    if exact:
                        return (True, solution)

                    exact, solution = compte(new_digits + [i * j],
                                             result,
                                             stack + ['%s * %s = %s' % (i, j, i * j)])
                    if exact:
                        return (True, solution)

                    if i != j:
                        exact, solution = compte(new_digits + [i - j],
                                                 result,
                                                 stack + ['%s - %s = %s' % (i, j, i - j)])
                        if exact:
                            return (True, solution)

                    if i % j == 0:
                        exact, solution = compte(new_digits + [i / j],
                                                 result,
                                                 stack + ['%s / %s = %s' % (i, j, i / j)])
                        if exact:
                            return (True, solution)

            return (False, stack)

        exact, res = compte(self.digits, self.total, [])

        if not exact:
            res = self.best_stack

        return exact, "\n".join(res)

    def check(self, answer):
        """ Checks if a solution is valid """
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
            """ Recursive function to evaluate an ast structure """
            if isinstance(node, ast.Num):  # <number>
                if left:
                    try:
                        self.ok_values.remove(node.n)
                    except ValueError:
                        raise CalcError(u"Euh, tu le sors d'où le %s ???"
                                        % node.n)
                else:
                    self.ok_values.append(node.n)
                return node.n
            elif isinstance(node, ast.operator):  # <operator>
                return operators[type(node)]
            elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
                try:
                    return eval_(node.op, left)(eval_(node.left, left),
                                                eval_(node.right, left))
                except ZeroDivisionError:
                    raise CalcError(u"Division par 0, BOOOOOOOOOOOOOOOOOOO")
            else:
                raise TypeError(node)

        operations = answer.split(";")
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
                raise CalcError(u"Je n'arrive pas à calculer « %s »" % left)
            try:
                eright = eval_expr(right, False)
            except SyntaxError:
                raise CalcError(u"Je n'arrive pas à calculer « %s »" % right)
            if eleft != eright:
                raise CalcError(u"Tu veux vraiment nous faire croire "
                                u"que %s = %s ???" % (left, right))
        return eval_expr(right, False)

if __name__ == '__main__' :
    c = Chiffres()
    c.digits = [5, 9, 25, 50, 75, 4, 143554545]
    #c.digits = [4, 5, 9, 25, 50, 75]
    #c.digits = [700, 3, 2]
    #c.digits = [4, 703]
    c.total  = 703
    e, s = c.solve()
    print c.digits
    print e
    print s


    c.digits = [ 788, 900, 102, 79, 77, 8765]
    c.total = 101
    e, s = c.solve()
    print c.digits
    print e
    print s
