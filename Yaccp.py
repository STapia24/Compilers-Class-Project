# This is the file that runs the compiler 

from Lexer_parser import lexer, parser, SyntaxError
from Structures.QuadrupleGen import QuadrupleGen
from Structures.VirtualMachine import *
from Structures.Memory import VirtualMachine
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
    file = sys.argv[1]
else:
    file = input('Please write the file name: \n' + '->')
    print()

inputFile = openFile(file)
lexer.input(inputFile)

try:
    parser.parse(inputFile, debug = 1)
    print("Parsing completed succesfully!")
except SyntaxError as err:
    print(f'Syntax error: Unexpected symbol {err.args[0]} in line {err.args[1]}.\n')
    exit(1)
except Exception as exception:
    print(f'Unknown error: {exception.args[0]}\n')

qg = QuadrupleGen.get()
qg.printQuadruples()

try:
    vm = VirtualMachine.get()
    vm.execute()
    print('Code was compiled succesfully!')
except Exception as exception:
    print('There was an error during the compiling process')
    print(exception)
print()