from Structures.QuadrupleGen import *
from Structures.CustomStack import Stack
from Structures.QuadActions import isConstant
from Structures.FunctionDir import *
from Structures.Memory import *

def solveOperations(operator, leftVar, rightVar, resultVar):
        mem = Memory.get()
        
        rightVal = mem.activeMemory().getVal(rightVar)
        leftVal = mem.activeMemory().getVal(leftVar)

        if operator == '+':
            resultValue = leftVal + rightVal
        if operator == '-':
            resultValue = leftVal - rightVal
        if operator == '*':
            resultValue = leftVal * rightVal
        if operator == '/':
            resultValue = leftVal / rightVal
        if operator == '<':
            resultValue = leftVal < rightVal
        if operator == '>':
            resultValue = leftVal > rightVal
        if operator == '==':
            resultValue = leftVal == rightVal
        if operator == '!=':
            resultValue = leftVal != rightVal
        if operator == '>=':
            resultValue = leftVal >= rightVal
        if operator == '<=':
            resultValue = leftVal <= rightVal
        if operator == '&&':
            resultValue = leftVal and rightVal
        if operator == '||':
            resultValue = leftVal or rightVal

        resultAddress, _ = mem.activeMemory().findAddress(resultVar)
        memAddress[resultAddress] = resultValue



def assignParams(vm, mem, funcId):
    paramsList = FuncDirectory[funcId]['params']
    paramOrder = vm.getParams()
    for i in range(0, len(paramsList)):
        fillAddress, _ = vm.callStack().top().findAddress(paramsList[i][0], False)
        valAddress = paramOrder[i]
        fillValue = mem.activeMemory().getAddressValue(valAddress)
        mem.activeMemory().assignAddressValue(fillValue, fillAddress)

def memoryStart(mem, funcId):
    varsList = getLocalVar(funcId)
    if funcId == 'global':
        globalMemory = mem.getGlobalMemory()
        for var in varsList:
            globalMemory.initAddress(var[0], var[1], 'global')
        return globalMemory
    else:
        localMemory = MemoryChunk()
        for var in varsList:
            localMemory.initAddress(var[0], var[1], 'local')
        return localMemory



class VirtualMachine:

    # Singleton class
    __instance = None

    @classmethod
    def get(arg):
        if VirtualMachine.__instance is None:
            VirtualMachine()
        return VirtualMachine.__instance
    
    def __init__(self):
        if VirtualMachine.__instance:
            raise Exception(
                "VirtualMachine already declared, use 'VirtualMachine.get()'")
        else:
            VirtualMachine.__instance = self
            self.__ip = 0
            self.__callStack = Stack()
            self.__quads = QuadrupleGen.get().quadruples()
            self.__funcParams = []
            self.__jumpStack = Stack()

    def instructionPointer(self):
        return self.__ip

    def setInstructionPointer(self, index):
        self.__ip = index

    def pointToNextQuad(self):
        self.__ip = self.__ip + 1

    def execute(self):
        quads = self.__quads
        while self.instructionPointer() < len(quads):
            operator, leftOp, rightOp, result = quads[self.instructionPointer()]
            # print('Executing:', quads[self.instructionPointer()])
            mem = Memory.get()
            relops = ['+', '-', '/', '*', '<', '>', '==', '!=', '<=', '>=', '&&', '||']

            if operator == '=':
                if isConstant(leftOp):
                    mem.activeMemory().setConstVal(result, leftOp)
                else:
                    mem.activeMemory().setVal(result, leftOp)
                self.pointToNextQuad()
            elif operator in relops:
                solveOperations(operator, leftOp, rightOp, result)
                self.pointToNextQuad()
            # Four types of goto, if only goto is in operator, just jumps to quad in result
            # if 'main' is in left operand, starts global memory and pushes it to memory stacks
            # if 'ENDFUNC' is in left operand it sets the instruction pointer to the pending jump and deletes the memory
            # if gotof, it evaluates the expression then if false, it jumps to the marked quadruple
            # if true then it just sets pointer to next quadruple
            elif operator == 'goto' and leftOp == 'main':
                if result == 1:
                    localMemory = memoryStart(mem, 'global')
                    mem.localMemoryStacks().push(localMemory)                    
                    self.pointToNextQuad()
                else:
                    self.setInstructionPointer(result)
                    localMemory = memoryStart(mem, 'global')
            elif operator == 'goto' and leftOp == 'ENDFUNC':
                self.setInstructionPointer(self.jumpStack().pop())
                mem.localMemoryStacks().pop()
            elif operator == 'goto':
                self.setInstructionPointer(result)
            elif operator == 'gotof':
                compareRes = mem.activeMemory().getVal(leftOp)
                if compareRes == False:
                    self.setInstructionPointer(result)
                else:
                    self.pointToNextQuad()
            
            elif operator == 'print':
                # Checks if the value is a string
                if isinstance(result, str):
                    writing = result[1:-1]  # Remove surrounding double quotes
                # Iterate over each character in the writing string
                    for i in range(len(writing)):
                    # If a backslash is found:
                        if writing[i] == '\\':
                        # Check the next character
                            if writing[i + 1] == '"':  # Escape \"
                                writing = writing[:i] + writing[i + 1:]  # Remove the backslash
                            elif writing[i + 1] == 'n':  # Escape \n
                                writing = writing[:i] + '\n' + writing[i + 2:]  # Replace \n with newline character
                            elif writing[i + 1] == '\\':  # Escape \\
                                writing = writing[:i] + '\\' + writing[i + 2:]  # Keep the backslash
                    print(writing, end='')
                else:
                    print(mem.activeMemory().getVal(result[-1]), end='')
                print()
                self.pointToNextQuad()
            # Receives the input from the user and tries to match it with its type
            elif operator == 'read':
                userInput = input('-> ')
                val = None
                valType = None
                try:
                    val = int(userInput)
                    valType = 'int'
                except ValueError:
                    try:
                        val = float(userInput)
                        valType = 'float'
                    except ValueError:
                        val = userInput[0]
                        valType = 'char'
                result = result[0]
                mem.activeMemory().setConstVal(result, val, valType)
                self.pointToNextQuad()
            # Creates the memory space for the function called
            elif operator == 'ERA':
                localMemory = memoryStart(mem, result)
                self.callStack().push(localMemory)
                self.pointToNextQuad()
            #Saves the jump to make then executes the GOSUB (Which is a jump to the function)
            elif operator == 'GOSUB':
                self.jumpStack().push(self.instructionPointer()+1)
                funcStart = getFunc(result) - 1
                self.setInstructionPointer(funcStart)
                # After running the function, clears parameters and deletes the memory segment
                # for the function
                assignParams(self, mem, result)
                self.clearParams()
                mem.localMemoryStacks().push(self.callStack().pop())
            # Assigns parameters to the function that is currently being executed
            elif operator == 'PARAM':
                paramAddress, _ = mem.activeMemory().findAddress(leftOp)
                self.addParam(paramAddress)
                self.pointToNextQuad()
            # Returns the value of the function
            elif operator == 'RETURN':
                resultAddress, _ = mem.activeMemory().findAddress(result)
                resultVal = mem.activeMemory().getAddressValue(resultAddress)
                self.callStack().push(resultVal)
                self.pointToNextQuad()
            # Marks the end of a function, it returns to the quadruple that was being executed
            # prior to calling the function to continue its execution
            elif operator == 'ENDFUNC':
                self.setInstructionPointer(self.jumpStack().pop())
                mem.localMemoryStacks().pop()
            # Special operation for assigning values between scopes
            # Used when assigning the result of a function call to a variable
            elif operator == 'FASSGN':
                resultAddress, _ = mem.activeMemory().findAddress(leftOp)
                resultVal = self.callStack().pop()
                mem.activeMemory().assignAddressValue(resultVal, resultAddress)
                self.pointToNextQuad()
            else:
                raise Exception(
                    f'Unrecognized operation in quadruple: ({operator}, {leftOp}, {rightOp}, {result})')
            
    def addParam(self, param):
        self.__funcParams.append(param)

    def getParams(self):
        return self.__funcParams

    def clearParams(self):
        self.__funcParams = []

    def jumpStack(self):
        return self.__jumpStack

    def callStack(self):
        return self.__callStack

    