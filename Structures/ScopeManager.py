from Structures.VarsFunctions import Variable, Function


class Scope:
    def __init__(self):
        self.__funcs = {}
        self.__vars = {}
        self.__scopes = {}
        self.__parent = None

    def funcs(self):
        return self.__funcs

    def vars(self):
        return self.__vars
    
    def scopes(self):
        # a scope can have other scopes, ex: global has class scopes, class scope have method scopes
        return self.__scopes

    def parent(self):
        return self.__parent

    def setParent(self, parent):
        self.__parent = parent

    # Search for a funcion within the scope, if not found raises exception ERR: Function was not declared
    def func(self, funcName):
        if funcName in self.funcs():
            return self.funcs()[funcName]
        else:
            raise Exception(
                f'Function \'{funcName}\' was not declared')
    
    # Returns a variable within the scope, if not found raises exception ERR: Variable was not declared
    def var(self, varName):
        if varName in self.vars():
            return self.vars()[varName]
        else:
            raise Exception(
                f'Variable \'{varName}\' was not declared')

    def addFunc(self, newName, funcType=None):
        if newName in self.funcs():
            raise Exception(
                f'Function \'{newName}\' is already declared in this scope')
        self.__funcs[newName] = Function(newName, funcType, [])
        return self.__funcs[newName]

    def addVar(self, new_name, var_type=None, is_const=False):
        if new_name in self.vars() and not is_const:
            raise Exception(
                f'Variable \'{new_name}\' is already declared in this scope')
        self.__vars[new_name] = Variable(new_name, var_type)

    def getVarFromId(self, varId):
        # Looks for a variable by its id in the current scope, if not found
        # then looks for the variable in other scopes if not found: ERR: Variable not declared
        if varId in self.vars():
            return self.vars()[varId]
        else:
            parent_scope = self.parent()
            if parent_scope:
                var = parent_scope.getVarFromId(varId)
                if var:
                    return var
                return None
            else:
                raise Exception(
                    f'Variable \'{varId}\' not declared')

    def getFuncFromId(self, funcId):
        # Looks for a function by its id in the current scope, if not found
        # then looks for the function in other scopes if not found: ERR: Funtion not declared
        if funcId in self.funcs():
            return self.funcs()[funcId]
        else:
            parent_scope = self.parent()
            if parent_scope:
                func = parent_scope.getFuncFromId(funcId)
                if func:
                    return func
            else:
                raise Exception(
                    f'Function \'{funcId}\' not declared')