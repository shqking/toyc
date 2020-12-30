`toyc` is a toy compiler for C subset, which is implemented in Python3. `toyc` translates C-like source code into the X86 assembly. It currently does not support other architectures.

**C subset**: only a subset of C grammar is supported:

- only `int` type is supported
- only **1-D array** and **pointer** is supported
- only a number of arithmetic and relational operators are supported.
- only decimal integers are constant
- global variables and function calls are supported
- **DO NOT** support `do-while`, `switch`, `goto`, `header `, `macros`,  `typedefs`, `struct`,  `qualifiers`, `library functions`, `bitwise operators`, `strings`. (Hope that we may update our tool in the near future.)

Please refer to the lexer and parser part for more details of our grammar.

**Optimizations**:  After parsing, several passes are implemented

- CFG and callgraph would be built, therefore unreachable code can be removed

- data flow analysis can be performed
- constant propagation
- common subexpression elimination
- peephole and register selection for backend

**How to use**: given a source code, simply run `python3 toyc.py -i src.c` and you would obtain the corresponding assembly file `src.c.S` and the log file `src.c.LOG` where details of every phase (including tokenization, AST building, the symbol table, CFG, call graph, optimization passes, instruction selection) are recorded.

- option `--opt` should be add if you want to enable optimization passes.

- We need use another **assembler** separately to get the object file for our compiled/generated assembly code.

- Since **library functions** are not supported in our grammar, in order to check the correctness of the generated assembly code, another test driver is needed as well to print out the computation results of our generated code.

  -  Take `test/fib.c` as an example. Function `fib()` generates the Fibonacci number and we need another file to call this function and dump the result.

    ```shell
    python3 toyc.py -i fib.c
    gcc -c fib.c.S -o fib.o
    gcc -c drive.c -o drive.o
    gcc fib.o drive.o -o a.out
    ./a.out
    ```



In the following, each phase is demonstrated in details.

[Lexer](./docs/lexer.md)

[Parser](./docs/parser.md)

TBA



------

Please raise issues if you have any question. Thanks.