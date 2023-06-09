

class Variable:
    def __init__(self, name, varType):
        self.__name = name
        self.__type = varType
        self.__value = None
        self.__dims = None

    def name(self):
        return self.__name

    def varType(self):
        return self.__type

    def value(self):
        return self.__value

    def dims(self):
        return self.__dims

    def set_i(self, i):
        self.__dims = i

    def set_j(self, j):
        self.__dims = (self.dims(), j)

    def i(self):
        # Checks if variable has dimensions, if it does, returns first dimension
        # if it doesn't have then it's not a dimensional variable
        dims = self.dims()
        if not dims:
            raise Exception(f'Trying to access non dimensional variable: \'{self.__name}\'')
        elif type(dims) is tuple:
            return dims[0]
        else:
            return dims

    def j(self):
        # Checks if variable has dimensions, if it does, returns second dimension
        dims = self.dims()
        if not dims:
            raise Exception(f'Trying to access non dimensional variable: \'{self.__name}\'')
        elif type(dims) is tuple:
            return dims[1]
        else:
            raise Exception(f'Trying to access one dimension variable: \'{self.__name}\' as a two dimensioned variable')

    def getSize(self):
        # Returns the amount of memory spaces needed
        dims = self.dims()
        if not dims:
            return 1
        elif type(dims) is tuple:
            return dims[0] * dims[1]
        else:
            return dims


class Function:
    def __init__(self, name, func_type, parameters=[]):
        self.__name = name
        self.__type = func_type
        self.__params = parameters

    def name(self):
        return self.__name

    def returnType(self):
        return self.__type

    def params(self):
        return self.__params
    
    def setParams(self, params):
        self.__params = params