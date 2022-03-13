# -*- coding: utf8 -*-
""" Module to define the 'countdown' game """
import ast
import logging
import operator as op
import random
from collections import namedtuple

logger = logging.getLogger("pipobot.chiffres_lettres.chiffres")

try:
    import chiffresc

    CHIFFRESC = True
    CHIFFRESC_OP = {0: ast.Add, 1: ast.Sub, 2: ast.Mult, 3: ast.Div, 4: None}
except ImportError:
    logger.info(
        "Unable to find C implementation for chiffres solving, "
        "falling back to python one"
    )
    CHIFFRESC = False


CHOICES = list(range(1, 10)) + [10, 25, 50, 75, 100]
NB_OPERANDS = 6


class CalcError(Exception):
    """Exception raised when a solution is not valid"""

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
        return op.floordiv(a, b)
    else:
        raise CalcError("%d n'est pas divisible par %d, escroc" % (a, b))


operators = {ast.Add: op.add, ast.Sub: mysub, ast.Mult: op.mul, ast.Div: mydiv}

# evaluation routines


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


def eval_(node, left, ok_values):
    """Recursive function to evaluate an ast structure"""

    if isinstance(node, ast.Num):  # <number>
        if left:
            try:
                ok_values.remove(node.n)
            except ValueError:
                raise CalcError("Euh, tu le sors d'où le %s ???" % node.n)
        else:
            ok_values.append(node.n)
        return node.n
    elif isinstance(node, ast.operator):  # <operator>
        return operators[type(node)]
    elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
        try:
            return eval_(node.op, left, ok_values)(
                eval_(node.left, left), eval_(node.right, left), ok_values
            )
        except ZeroDivisionError:
            raise CalcError("Division par 0, BOOOOOOOOOOOOOOOOOOO")
    else:
        raise TypeError(node)


class Chiffres:
    """The game Countdown main class"""

    digit_ast = namedtuple("digit_ast", ["n", "ast"])

    def __init__(self):
        self.total = random.randint(100, 999)
        self.digits = []
        i = 0
        while i < NB_OPERANDS:
            i += 1
            self.digits.append(random.choice(CHOICES))
        self.digits = sorted(self.digits)

    def solve_c(self):
        """Solve using C library"""
        r = chiffresc.solve6(self.total, *self.digits)

        def transform_ast(tuple_ast):
            """Transform a tuple ast from C to digit_ast"""

            left, op, right, total = tuple_ast
            if CHIFFRESC_OP[op] is None:
                return ast.Num(total)
            else:
                return ast.BinOp(
                    transform_ast(left), CHIFFRESC_OP[op], transform_ast(right)
                )

        return r[3] == self.total, self.digit_ast(n=r[3], ast=transform_ast(r))

    def solve_python(self):
        """Solve using Python native"""

        def compte(digits):
            """Recursive auxiliary function to solve the problem"""

            for digit in digits:
                if digit.n == self.total:
                    # Terminal case : if the total is in the list, it's ok
                    return digit
                elif self.best is None or abs(self.total - digit.n) < abs(
                    self.total - self.best.n
                ):
                    # We keep trace of the closest result found
                    self.best = digit

            for idg, g in enumerate(digits):
                for idh, h in enumerate(digits[idg + 1 :]):
                    # We test all the combinations (not permutations).
                    # All we miss are not commutative operations (- and /),
                    # but only the case where g > h are significative,
                    # so we reorder them. We also copy the digit list and remove
                    # the two digits we are working on, as they will be replaced
                    # by the result of their operation
                    new_digits = digits[:]
                    new_digits.pop(idg)
                    new_digits.pop(idg + idh)
                    # There is an hidden +1-1 (-1 because we have removed 1 before)
                    if g.n != h.n:
                        i, j = max(g, h, key=lambda x: x.n), min(
                            g, h, key=lambda x: x.n
                        )
                    else:
                        i, j = g, h

                    # Iterate over operators and recursion
                    for astop, ope in operators.items():
                        try:
                            r = compte(
                                new_digits
                                + [
                                    self.digit_ast(
                                        n=ope(i.n, j.n),
                                        ast=ast.BinOp(i.ast, astop, j.ast),
                                    )
                                ]
                            )
                            if r is not None:
                                return r
                        except CalcError:
                            pass

            return None

        self.best = None

        r = compte([self.digit_ast(d, ast.Num(d)) for d in self.digits])
        return r is not None, r if r is not None else self.best

    def solve(self):
        """Finds the best solution for the game"""

        return self.solve_c() if CHIFFRESC else self.solve_python()

    def check(self, answer):
        """Checks if a solution is valid"""
        self.ok_values = list(self.digits)

        operations = answer.split(";")
        for operation in operations:
            try:
                left, right = operation.split("=", 2)
            except ValueError:
                raise CalcError("Erreur de syntaxe dans %s" % operation)
            left = left.strip()
            right = right.strip()
            try:
                eleft = eval_expr(left, True)
            except SyntaxError:
                raise CalcError("Je n'arrive pas à calculer « %s »" % left)
            try:
                eright = eval_expr(right, False)
            except SyntaxError:
                raise CalcError("Je n'arrive pas à calculer « %s »" % right)
            if eleft != eright:
                raise CalcError(
                    "Tu veux vraiment nous faire croire "
                    "que %s = %s ???" % (left, right)
                )
        return eval_expr(right, False)


if __name__ == "__main__":
    opstr = {ast.Add: "+", ast.Sub: "-", ast.Mult: "×", ast.Div: "÷"}

    c = Chiffres()
    c.digits = [1, 8, 9, 25, 10, 100]
    c.total = 364
    print(c.digits)
    s = c.solve()[1]

    def pretty_lisp(astree):
        """Print ast tree in algebra formula"""

        if isinstance(astree, ast.Constant):
            return str(astree.n)
        elif isinstance(astree, ast.BinOp):
            return "(%s%s%s)" % (
                pretty_lisp(astree.left),
                opstr[astree.op],
                pretty_lisp(astree.right),
            )
        else:
            raise Exception("WTF is %s (type : %s)" % (astree, type(astree)))

    print(f"{pretty_lisp(s.ast)} = {s.n}")
