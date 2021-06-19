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

def run_file(name, data, debug):
    print('-' * 80)
    print(f'Executing {name}')
    print('-' * 80)
    lexer = Lexer()
    start_time = perf_counter()
    tokens = lexer.tokenize(data)
    parser = Parser()
    tree = parser.parse(tokens)
    processor = Processor(tree, debug=debug)
    processor.run(tree) 
    end_time = perf_counter() - start_time
    print('-' * 80)
    print(f'Execution finished in {end_time:.2f}s')

def get_file_contents(filename):
    with open(filename) as f:
        return f.read()

def main():
    arg1 = argv(1)
    debug = argv(2) == 'debug'
    if arg1:
        filename = arg1
        if os.path.exists(filename + '.dty'):
            run_file(filename, get_file_contents(filename + '.dty'), debug)
        elif arg1 == 'runall':
            for filename in os.listdir('tests/'):
                filename = os.path.join('tests/', filename)
                if filename.endswith('.dty'):
                    run_file(filename[:-3], get_file_contents(filename), debug)
        else:
            print(f'File {arg1} does not exist.')


if __name__ == '__main__':
    main()
