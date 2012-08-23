#-*- coding: utf8 -*-
import random

CHOICES = range(1, 10) + [10, 25, 50, 75]
NB_OPERANDS = 6

class Chiffres:
    def __init__(self):
        self.total = random.randint(100, 1000)
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

        return exact, Chiffres.format_output(res)

    @staticmethod
    def format_output(lst_operations):
        return "\n".join(lst_operations)

if __name__ == "__main__":
    c = Chiffres()
    print c.numbers
    print c.total
    print c.solve()
