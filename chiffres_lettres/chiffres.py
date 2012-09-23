#-*- coding: utf8 -*-
""" Module to define the 'countdown' game """
import ast
import operator as op
from collections import namedtuple
import random

CHOICES = range(1, 10) + [10, 25, 50, 75, 100]
NB_OPERANDS = 6


class CalcError(Exception):
    """ Exception raised when a solution is not valid """
    def __init__(self, message):
        Exception.__init__(self, message)

# supported operators


def mysub(a, b):
    if a != b:
        return op.sub(a, b)
    else:
        raise CalcError("%d-%d = 0, c'est pas super utile…" % (a, b))


def mydiv(a, b):
    if a % b == 0:
        return op.div(a, b)
    else:
        raise CalcError("%d n'est pas divisible par %d, escroc" % (a, b))

operators = {ast.Add: op.add, ast.Sub: mysub, ast.Mult: op.mul,
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
        def compte(digits):
            """ Recursive auxiliary function to solve the problem """

            for digit in digits:
                if digit.n == self.total:
                    # Terminal case : if the total is in the list, it's ok
                    return digit
                elif self.best is None or abs(self.total - digit.n) < abs(self.total - self.best.n):
                    # We keep trace of the clothest result found
                    self.best = digit

            for idg, g in enumerate(digits):
                for idh, h in enumerate(digits[idg + 1:]):
                    # We test all the combinations (not permutations). All we miss are
                    # not commutative operations (- and /), but only the case where g > h
                    # are significative, so we reorder them. We also copy the digit list and remove
                    # the two digits we are working on, as they will be replaced by the result of their operation
                    new_digits = digits[:]
                    new_digits.pop(idg)
                    new_digits.pop(idg + idh) # There is an hidden +1-1 (-1 because we have removed one before)
                    i, j = max(g, h, key=lambda x: x.n), min(g, h, key=lambda x: x.n)

                    # Iterate over operators and recursion
                    for astop, op in operators.iteritems():
                        try:
                            r = compte(new_digits + [digit_ast(n=op(i.n, j.n), ast=ast.BinOp(i.ast, astop, j.ast))])
                            # Stop if we have found a solution
                            if r:
                                return r
                        except CalcError:
                            pass

            return None

        digit_ast = namedtuple('digit_ast', ['n', 'ast'])
        self.best = None

        r = compte([digit_ast(d, ast.Num(d)) for d in self.digits])
        return r is not None, r if r is not None else self.best

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

if __name__ == '__main__':
    opstr = {ast.Add: u'+', ast.Sub: u'-', ast.Mult: u'×', ast.Div: u'÷'}

    def pretty_lisp(astree):
        """ Print ast tree in algebra formula """

        if isinstance(astree, ast.Num):
            return unicode(astree.n)
        elif isinstance(astree, ast.BinOp):
            return u'(%s%s%s)' % (pretty_lisp(astree.left), opstr[astree.op], pretty_lisp(astree.right))

    c = Chiffres()
    #c.digits = [5, 9, 25, 50, 75, 4, 143554545]
    c.digits = [4, 5, 9, 25, 50, 75]
    #c.digits = [700, 3, 2]
    #c.digits = [4, 703]
    c.total = 703
    print c.digits
    print pretty_lisp(c.solve()[1].ast).encode('utf8')


    #c.digits = [ 788, 900, 102, 79, 77, 8765]
    #c.total = 101
    #s = c.solve()
    #print c.digits
    #print s
