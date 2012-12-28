/* chiffres.c

Implementation in C of the algorithm to solve "Le compte est bon" 
With python interface

*/
#ifndef NOPYTHON
#include <Python.h>
#endif

#include <stdlib.h>
#include <string.h>

/* Structures needed by the algorithm */

enum operator { ADD, SUB, MULT, DIV, NUL } ;

struct ast {
    void* left;
    void* right;
    enum operator op ;
    int n;
}; /* Basic ast structure */

/*
 * Intermediate functions to manuipulate ast structures
 */

/* Generate an ast structure suitable for an operation */
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

/* Recursive free of an ast structure and its left and right childs */
void free_ast(struct ast* ast)
{
    if (ast->left != NULL) {
        free_ast(ast->left) ;
    }

    if (ast->right != NULL) {
        free_ast(ast->right) ;
    }

    free(ast) ;
}
 
/* Recursive copy of an ast structure and its left and right childs */
struct ast* cpy_ast(struct ast* src)
{
    struct ast* left ;
    struct ast* right ;
    struct ast* dest ;
    left = (struct ast*) NULL ;
    right = (struct ast*) NULL ;

    if (src->left != NULL)
        left = cpy_ast(src->left) ;

    if (src->right != NULL)
        right = cpy_ast(src->right) ;

    dest = malloc(sizeof(struct ast)) ;
    memcpy(dest, src, sizeof(struct ast)) ; 
    dest->left = (void*) left ;
    dest->right = (void*) right ;

    return dest ;
}

/* 
 * Solving function 
 */
void solve(struct ast* digits[], int num_digit, int total, struct ast** best)
{
    int i, j, k, l;

    /* Keep trace of the best result found */
    for (i=0; i < num_digit; i++) {
        if (*best == NULL || abs(digits[i]->n - total) < abs((*best)->n - total)) {
            if (*best != NULL) {
                free_ast(*best) ;
            }
            *best = cpy_ast(digits[i]) ;
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
            free(ndigits[l]) ;

            if (a->n != b->n) {
                ndigits[l] = gen_ast_op(a, b, SUB, a->n-b->n) ;
                solve(ndigits, (num_digit-1), total, best) ;
                free(ndigits[l]) ;
            }
            
            ndigits[l] = gen_ast_op(a, b, MULT, a->n*b->n) ;
            solve(ndigits, (num_digit-1), total, best) ;
            free(ndigits[l]) ;

            if (a->n % b->n == 0) {
                ndigits[l] = gen_ast_op(a, b, DIV, a->n/b->n) ;
                solve(ndigits, (num_digit-1), total, best) ;
                free(ndigits[l]) ;
            }

            free(ndigits) ;
        }
    }
}

#ifndef NOPYTHON

static PyObject* solve6(PyObject *self, PyObject *args)
{
    PyObject* ret;
    /* Initial numbers */
    int nchiffres = 6 ;
    int chiffres[6] ;
    int total ;

    if (!PyArg_ParseTuple(args, "iiiiiii", &total, &chiffres[0], &chiffres[1], 
                          &chiffres[2], &chiffres[3], &chiffres[4], &chiffres[5]))
        return NULL;


    /* Prepare structures for solve */
    struct ast** digits = malloc(nchiffres * sizeof(struct ast*)) ;
    struct ast* digit ;
    struct ast* best = NULL;

    int i ;
    for (i=0; i<nchiffres; i++) {
        digit = malloc(sizeof(struct ast)) ;
        digit->left  = NULL ;
        digit->op    = NUL ;
        digit->right = NULL ;
        digit->n     = chiffres[i] ;
        digits[i] = digit ;
    }

    /* Solve ! */
    solve(digits, nchiffres, total, &best) ;

    /* Free digits and best */
    for (i=0; i<nchiffres; i++) {
        free(digits[i]) ;
    }
    free(digits) ;

    ret = Py_BuildValue("i", best->n);
    free_ast(best) ;

    return ret ;
}


static PyMethodDef ChiffrecMethods[] = {
    {"solve6",  solve6, METH_VARARGS,
     "Solve chiffres with 6 numbers"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

void
initchiffresc(void)
{
    (void) Py_InitModule("chiffresc", ChiffrecMethods);
}

int main(int argc, char *argv[])
{
    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(argv[0]);

    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();

    /* Add a static module */
    initchiffresc() ;

    return 0 ;
}

#else /* NOPYTHON */

#include <stdio.h>

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
    /* Initial numbers */
    int chiffres[] = {4, 5, 9, 25, 50, 75} ;
    int total = 703 ;
    int nchiffres  = 6 ;

    /* Prepare structures for solve */
    struct ast** digits = malloc(nchiffres * sizeof(struct ast*)) ;
    struct ast* digit ;
    struct ast* best = NULL;

    int i ;
    for (i=0; i<nchiffres; i++) {
        digit = malloc(sizeof(struct ast)) ;
        digit->left  = NULL ;
        digit->op    = NUL ;
        digit->right = NULL ;
        digit->n     = chiffres[i] ;
        digits[i] = digit ;
    }

    /* Solve ! */
    solve(digits, nchiffres, total, &best) ;

    /* Show the results */
    printf("A fini\n") ;
    printf("Best : %d\n", best->n) ;
    printer_lisp(best) ;
    printf("\n") ;

    /* Free digits and best */
    for (i=0; i<nchiffres; i++) {
        free(digits[i]) ;
    }
    free(digits) ;
    free_ast(best) ;

    return 0 ;
}

#endif /* NOPYTHON */
