# This is the file that runs the compiler 

from Lexer_parser import lexer, parser
from Structures.QuadrupleGen import QuadrupleGen
from Structures.VirtualMachine import VirtualMachine
import time
import sys


def openFile(fileName):
    try:
        file = open(fileName, 'r')
    except FileNotFoundError:
        print('Error: file not found\n')
        exit(1)
    except Exception as exception:
        print('Error: unable to open file\n')
        print(exception)
        exit(1)

    lines = file.read()
    file.close()
    return lines

if len(sys.argv) >= 2:
    file = 'Tests/' + sys.argv[1]
else:
    file = 'Tests/' + input('Please write the file name: ')

inputFile = openFile(file)
lexer.input(inputFile)

try:
    parser.parse(inputFile, debug = 0)
    pass
except SyntaxError as err:
    print(f'Syntax error: Unexpected symbol {err.args[0]} in line {err.args[1]}.\n')
    exit(1)
except Exception as exception:
    print(f'Semantic error: {exception.args[0]}\n')
    exit(1)

#qg = QuadrupleGen.get()
#qg.printQuadruples()

try:
    vm = VirtualMachine.get()
    print('Jumping into compilation...')
    time.sleep(2)
    print("The result is")
    vm.execute()
    print("Compilation went smoothly! Thanks for trying YACCP")
except Exception as exception:
    print('There was an error during the compiling process')
    print(exception)
    exit(1)