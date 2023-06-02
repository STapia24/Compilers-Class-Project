from Structures.VarsFunctions import Variable, Function


class Scope:
    def __init__(self):
        self.__funcs = {}
        self.__vars = {}
        self.__parent = None

    def funcs(self):
        return self.__funcs

    def vars(self):
        return self.__vars

    def parent(self):
        return self.__parent

    def set_parent(self, parent):
        self.__parent = parent

    # Search for a funcion within the scope, if not found raises exception ERR: Function was not declared
    def func(self, func_name):
        if func_name in self.funcs():
            return self.funcs()[func_name]
        else:
            raise Exception(
                f'Function \'{func_name}\' was not declared')
    
    # Returns a variable within the scope, if not found raises exception ERR: Variable was not declared
    def var(self, var_name):
        if var_name in self.vars():
            return self.vars()[var_name]
        else:
            raise Exception(
                f'Variable \'{var_name}\' was not declared')

    def add_func(self, new_name, func_type=None):
        if new_name in self.funcs():
            raise Exception(
                f'Function \'{new_name}\' is already declared in this scope')
        self.__funcs[new_name] = Function(new_name, func_type, [])
        return self.__funcs[new_name]

    def add_var(self, new_name, var_type=None, is_const=False):
        if new_name in self.vars() and not is_const:
            raise Exception(
                f'Variable \'{new_name}\' is already declared in this scope')
        self.__vars[new_name] = Variable(new_name, var_type)

    def get_var_from_id(self, var_id):
        # Looks for a variable by its id in the current scope, if not found
        # then looks for the variable in other scopes if not found: ERR: Variable not declared
        if var_id in self.vars():
            return self.vars()[var_id]
        else:
            parent_scope = self.parent()
            if parent_scope:
                var = parent_scope.get_var_from_id(var_id)
                if var:
                    return var
                return None
            else:
                raise Exception(
                    f'Variable \'{var_id}\' not declared')

    def get_func_from_id(self, func_id):
        # Looks for a function by its id in the current scope, if not found
        # then looks for the function in other scopes if not found: ERR: Funtion not declared
        if func_id in self.funcs():
            return self.funcs()[func_id]
        else:
            parent_scope = self.parent()
            if parent_scope:
                func = parent_scope.get_func_from_id(func_id)
                if func:
                    return func
            else:
                raise Exception(
                    f'Function \'{func_id}\' not declared')