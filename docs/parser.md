#### Parser

Syntax. C subset

```bash
# Symbols: global variable and function
program     : KW_INT def program | nil
def         : VAR idtail | * VAR init ;
idtail      : [ CONST_VAL ] ; | ( para ) block | init ;
init        : = expr | nil

# Paramenters
para        : KW_INT paradata paralist | nil
paradata    : VAR | * VAR
paralist    : , KW_INT paradata paralist | nil

# Statments
block       : { subprogram }
subprogram  : localdef subprogram | stmt subprogram | nil

localdef    : KW_INT defdata ;
defdata     : VAR varrdef | * VAR init
varrdef     : [ CONST_VAL ] | init

stmt        : altexpr ; | KW_BREAK ; | KW_CONTINUE ; | KW_RETURN expr ;
              | ifstmt | forstmt | whilestmt

ifstmt      : KW_IF ( expr ) block elsestmt
elsestmt    : KW_ELSE block | nil
forstmt     : KW_FOR ( alexpr ; altexpr ; altexpr ) { block }
whilestmt   : KW_WHILE ( expr ) { block }

# Expressions
# Note: priority should be considered
#  1: a[i], foo()
#  2: *ptr, -123, &var
#  3: mul, div
#  4: add, sub
#  5: relation
#  6: assignment
altexpr     : expr | nil         # Can be empty
expr        : cmp_expr asstail
asstail     : = cmp_expr asstail | nil

cmp_expr    : add_expr cmptail
cmptail     : cmp_ops add_expr cmptail | nil
cmp_ops     : > | < | == | !=

add_expr    : mul_expr addtail
addtail     : add_ops mul_expr addtail | nil
add_ops     : + | -

mul_expr    : factor multail
multail     : mul_ops factor multail | nil
mul_ops     : * | /

factor      : unary_op val | val
unary_op    : * | - | &

val         : VAR valtail | CONST_VAL
valtail     : [ expr ] | ( args ) | nil

# Arguments
args       : expr arglist | nil
arglist    : , expr arglist | nil
```



Samples:

```c
int a;
int a = 0;
int a = b + c;
int *a;
int *a = &b;
int a[10];
int f() {}
int f(int a, int *b) {}

int foo(int a) {
    a = 0;
    int b = a * 2 + 1;
    if(a > 0) { ; }
    
    if (a == 0) {
    	a = a + 1;
    } else {
    	;
    }
    
    for(a = 4; a > 10; ) {
    	a = a + 1;
    }
    
    while(1) {;}
    
    return a + 2;
}
```



Syntax Errors:

```c
int a, b;            // NIY: compound stmt
int a[b];            // Must be constant for declaration
int foo();           // NIY: func declaration
int a[10] = {1,2,3}; // NIY: array initialization
int foo(int c[10]){} // NIY: array as parameter
int foo(int )        // NIY: default parameter name
int foo(int a[])     // bad parameter type

for(int a = 4; a > 10; ) {	// do not init in forstmt
    a = a + 1;
}

// TBA
```



Semantic Errors:

```c
int *p = a;       // Mismatch type
int a; int a;     // re-declaration

// TBA
```

