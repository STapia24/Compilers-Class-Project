from Structures.CustomStack import Stack
from Structures.ScopeManager import Scope


class SymbolTable:

    # Singleton class
    __instance = None

    @classmethod
    def get(arg):
        if SymbolTable.__instance is None:
            SymbolTable()
        return SymbolTable.__instance
    
    def __init__(self):
        if SymbolTable.__instance:
            raise Exception(
                "Symbol Table already declared, use 'SymbolTable.get()'.")
        else:
            SymbolTable.__instance = self
            self.__scopeStack = Stack()
            self.__scopeStack.push(('global', Scope()))
            self.__currentType = None
            self.__currentId = None
            self.__lastSavedFunc = None
            self.__operands = Stack()
            self.__operandTypes = Stack()
            self.__operators = Stack()
            self.__operandsStacks = Stack()
            self.__typesStacks = Stack()
            self.__operatorsStacks = Stack()
            self.__varToAssign = Stack()
            self.__currentParams = []

    def currentScopeName(self):
        return self.scopeStack().top()[0]

    def currentScope(self):
        return self.scopeStack().top()[1]

    def scopeStack(self):
        return self.__scopeStack

    def setCurrType(self, newType):
        def isValid():
            if newType == 'int' or newType == 'float' or newType == 'char':
                return True
            # This is only valid for functions
            if newType == 'void':
                return True
            return False

        if isValid():
            self.__currentType = newType
        else:
            raise Exception(f"Invalid type: '{newType}'.")

    def currentType(self):
        return self.__currentType

    def setCurrId(self, newId):
        self.__currentId = newId

    def currentId(self):
        return self.__currentId

    def lastSavedFunc(self):
        return self.__lastSavedFunc

    def setLastSavedFunc(self, savedFunc):
        self.__lastSavedFunc = savedFunc

    def saveVar(self):
            # print("saving var:", self.currentId(), "it's type is:", self.currentType())
            self.currentScope().addVar(self.currentId(), self.currentType())

    def saveTempVar(self, name, varType):
        self.currentScope().addVar(name, varType)

    def saveFunc(self):
        scope = self.currentScope()
        saved_func = scope.addFunc(self.currentId(), self.currentType())
        self.setLastSavedFunc(saved_func)

    def saveParameter(self):
        self.lastSavedFunc().params().append((self.currentType(), self.currentId()))
        self.currentScope().addVar(self.currentId(), self.currentType())

    def pushNewScope(self):
        name = self.currentId()
        scope_obj = Scope()
        scope_obj.setParent(self.currentScope())
        self.currentScope().scopes()[name] = scope_obj
        self.scopeStack().push((name, scope_obj))

    def popScope(self):
        self.scopeStack().pop()            

    def operands(self):
        return self.__operands

    def opTypes(self):
        return self.__operandTypes

    def operators(self):
        return self.__operators

    # Stacks of stacks used when false bottom is pushed into a stack
    def operandsStacks(self):
        return self.__operandsStacks

    def typesStacks(self):
        return self.__typesStacks

    def operatorsStacks(self):
        return self.__operatorsStacks

    def setOperands(self, val):
        self.__operands = val

    def setTypes(self, val):
        self.__operandTypes = val

    def setOperators(self, val):
        self.__operators = val

    def varToAssign(self):
        return self.__varToAssign

    def currentParams(self):
        return self.__currentParams

    def resetCurrentParams(self):
        self.__currentParams = []
