#!/usr/bin/env python3

from src import *
import sys
import os
from time import perf_counter

def argv(n):
    try:
        return sys.argv[n]
    except:
        pass
    return None

def main():
    filename = argv(1)
    debug = argv(2) == 'debug'
    lexer = Lexer()
    if filename:
        if os.path.exists(filename + '.dty'):
            with open(filename + '.dty') as f:
                print('-' * 80)
                print(f'Executing {filename}')
                print('-' * 80)
                start_time = perf_counter()
                tokens = lexer.tokenize(f.read())
                parser = Parser()
                tree = parser.parse(tokens)
                processor = Processor(tree, debug=debug)
                processor.run(tree) 
                end_time = perf_counter() - start_time
                print('-' * 80)
                print(f'Execution finished in {end_time:.2f}s')


if __name__ == '__main__':
    main()