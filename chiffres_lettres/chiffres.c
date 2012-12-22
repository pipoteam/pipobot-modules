/* chiffres.c

Implementation in C of the algorithm to solve "Le compte est bon" 
With python interface

*/
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

/* Structures needed by the algorithm */

enum operator { ADD, SUB, MULT, DIV, NUL } ;

struct ast {
    void* left;
    void* right;
    enum operator op ;
    int n;
}; /* Basic ast structure */

/* Intermediate function to generate ast for operation */
struct ast* gen_ast_op(struct ast* left, struct ast* right, enum operator op, int result)
{
    struct ast* ast ; 
    ast = malloc(sizeof(struct ast)) ;
    ast->left  = (void*) left ;
    ast->right = (void*) right ;
    ast->op = op ;
    ast->n = result ;
    return ast ;
}
 
// Solving function
void solve(struct ast* digits[], int num_digit, int total, struct ast* best)
{
    int i, j, k, l, r;

    /* Keep trace of the best result found */
    for (i=0; i < num_digit; i++) {
        if (best->n == -1 || abs(digits[i]->n -total) < abs(best->n - total)) {
            memcpy(best, digits[i], sizeof(struct ast)) ;
        }
    }

    struct ast* a ;
    struct ast* b ;

    for (i=0; i < num_digit-1; i++) {
        for (j=i+1; j < num_digit; j++) {
            /* We tests all the combination (not permutations). All we miss are
              not commutative operations (- and /), but only the case where g > h
              are significative, so we reorder them. We also copy the digit list and 
              remove the two digits we are working on, as they will 
              be replaced by the result of their operation */

            /* We copy list of digits NOT including keys i and j */
            struct ast** ndigits = malloc((num_digit-1)*sizeof(struct ast*)) ;
            l=0 ;
            for (k=0; k<num_digit; k++) {
                if (k == i || k == j) { continue ; }
                ndigits[l] = digits[k] ;
                l++ ;
            }
            
            /* Reorder (cf. ↑) */
            if (digits[i]->n > digits[j]->n) {
                a = digits[i] ;
                b = digits[j] ;
            } else {
                a = digits[j] ;
                b = digits[i] ;
            }

            
            /* Test for operations */
            ndigits[l] = gen_ast_op(a, b, ADD, a->n+b->n) ;
            solve(ndigits, (num_digit-1), total, best) ;

            if (a->n != b->n) {
                ndigits[l] = gen_ast_op(a, b, SUB, a->n-b->n) ;
                solve(ndigits, (num_digit-1), total, best) ;
            }
            
            ndigits[l] = gen_ast_op(a, b, MULT, a->n*b->n) ;
            solve(ndigits, (num_digit-1), total, best) ;

            if (a->n % b->n == 0) {
                ndigits[l] = gen_ast_op(a, b, ADD, a->n+b->n) ;
                solve(ndigits, (num_digit-1), total, best) ;
            }
        }
    }
}

/* Simple ast printer */
void printer_lisp(struct ast* ast) {
    if (ast == NULL) { return ; }

    printf("(") ;
    printer_lisp(ast->left) ;
    switch (ast->op) {
        case NUL:
            printf("%d",ast->n) ;
            break;
        case ADD:
            printf("+") ;
            break ;
        case SUB:
            printf("-") ;
            break ;
        case MULT:
            printf("*") ;
            break ;
        case DIV:
            printf("/") ;
            break ;
    }
    printer_lisp(ast->right) ;
    printf(")") ;
}
            
int main(int argc, char* argv[])
{
    int i ;
    struct ast best ;
    best.n = -1 ;
    int chiffres[] = {4, 5, 9, 25, 50, 75} ;
    int total = 703 ;
    int nchiffres  = 6 ;

    struct ast** digits = malloc(nchiffres * sizeof(struct ast*)) ;
    struct ast* digit ;

    for (i=0; i<nchiffres; i++) {
        digit = malloc(sizeof(struct ast)) ;
        digit->left  = NULL ;
        digit->op    = NUL ;
        digit->right = NULL ;
        digit->n     = chiffres[i] ;
        digits[i] = digit ;
    }

    solve(digits, nchiffres, total, &best) ;
    printf("A fini\n") ;
    printf("Best : %d\n", best.n) ;
    printer_lisp(&best) ;
    printf("\n") ;
}
