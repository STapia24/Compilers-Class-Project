from Structures.CustomStack import Stack

# Assigning ranges for the memory scopes
ranges = {
    'global': { 'int': 1000, 'float': 2000, 'bool': 3000, 'char': 4000 },
    'local': { 'int': 10000, 'float': 11000, 'bool': 12000, 'char': 13000 },
    'temp': { 'int': 20000, 'float': 21000, 'bool': 22000, 'char': 23000 },
    'const': { 'int': 30000, 'float': 31000, 'bool': 32000, 'char': 33000 },
}
 
memAddress = {}


def printMemoryAddress():
    print(memAddress)


class MemoryChunk:
    def __init__(self, memSize=1000):
        self.__int = {}
        self.__float = {}
        self.__bool = {}
        self.__char = {}
        self.__memory_left = {
            'int': memSize, 'float': memSize, 'bool': memSize, 'char': memSize}

    def getVars(self, address_type):
        if address_type == 'int':
            return self.__int
        if address_type == 'float':
            return self.__float
        if address_type == 'bool':
            return self.__bool
        if address_type == 'char':
            return self.__char

    def findAddress(self, var_id):

        ints = self.get_vars('int')
        if var_id in ints:
            return ints[var_id], 'int'

        floats = self.get_vars('float')
        if var_id in floats:
            return floats[var_id], 'float'

        bools = self.get_vars('bool')
        if var_id in bools:
            return bools[var_id], 'bool'

        chars = self.get_vars('char')
        if var_id in chars:
            return chars[var_id], 'char'
        
        # Looks among the constants in case variable has not been found
        memory = Memory.get()
        constants = memory.getConsts()
        try:
            address, varType = constants.findAddress(var_id)
        except:
            address = None
        if not address:
            globalMem = memory.getGlobalMemory()
            address, varType = globalMem.findAddress(var_id)
            if not address:
                raise Exception(
                    f"Could not find address for variable '{var_id}'")
        return address, varType

    def initAddress(self, var_id, address_type, scope):
        try:
            assignedAddress = self.getVars(address_type)
            # the index is the base memory address and we set it to the address
            memoryIndex = ranges[scope][address_type]
            assignedAddress[var_id] = memoryIndex
            # set the new index in memory
            ranges[scope][address_type] = memoryIndex + 1
            # inits
            memAddress[memoryIndex] = None
        except Exception as err:
            print(err)
        self.__memory_left[address_type] -= 1
        if self.__memory_left[address_type] <= 0:
            raise Exception(f'Ran out of memory for \'{address_type}\' type')

    def setVal(self, res_id, value_id):
        valueAddress, _ = self.findAddress(value_id)
        address_to_set, _ = self.findAddress(res_id)
        memAddress[address_to_set] = memAddress[valueAddress]

    def setConstVal(self, res_id, value, value_type=None):
        if value_type == None:
            address, _ = self.findAddress(res_id)
            memAddress[address] = value
        else:
            address, var_type = self.findAddress(res_id)
            if value_type == var_type:
                memAddress[address] = value
            else:
                raise Exception(
                    f'Type mismatch: unable to assign {value} of type \'{value_type}\' to variable \'{res_id}\' of type \'{var_type}\''
                )

    def print(self):
        # Used only for debugging
        ints = self.get_vars('int')
        print('ints', ints)
        floats = self.get_vars('float')
        print('floats', floats)
        bools = self.get_vars('bool')
        print('bools', bools)
        chars = self.get_vars('char')
        print('chars', chars)

    def getVal(self, var_id):
        address, _ = self.findAddress(var_id)
        if not address:
            # If there's no address then it means it's a constant and thus has to be searched as one
            memory = Memory.get()
            constants = memory.getConsts()
            constant_value = constants.getVal(var_id)
            return constant_value
        return memAddress[address]

    def solveQuad(self, operator, result_var, left_var, right_var):
        right_value = self.getVal(right_var)
        left_value = self.getVal(left_var)

        if operator == '+':
            result_value = left_value + right_value
        if operator == '-':
            result_value = left_value - right_value
        if operator == '*':
            result_value = left_value * right_value
        if operator == '/':
            result_value = left_value / right_value
        if operator == '<':
            result_value = left_value < right_value
        if operator == '>':
            result_value = left_value > right_value
        if operator == '==':
            result_value = left_value == right_value
        if operator == '!=':
            result_value = left_value != right_value
        if operator == '>=':
            result_value = left_value >= right_value
        if operator == '<=':
            result_value = left_value <= right_value
        if operator == '&&':
            result_value = left_value and right_value
        if operator == '||':
            result_value = left_value or right_value

        result_address, _ = self.findAddress(result_var)
        memAddress[result_address] = result_value



class Memory:

    # Singleton class
    __instance = None

    @ classmethod
    def get(arg):
        if Memory.__instance is None:
            Memory()
        return Memory.__instance
    
    def __init__(self):
        if Memory.__instance:
            raise Exception(
                "Memory already declared, use 'Memory.get()'")
        else:
            Memory.__instance = self
            self.__global = MemoryChunk()
            self.__consts = MemoryChunk()
            self.__localStacks = Stack()
            self.__localStacks.push(self.__global)

    def getGlobalMemory(self):
        return self.__global

    def getConsts(self):
        return self.__consts

    # Constants are always stored in global scope to access them from anywhere since the value doesn't change and might be needed somewhere else
    def addConstant(self, constant, constant_type):
        consts = self.getConsts()
        consts.initAddress(constant, constant_type, 'global')
        consts.setConstVal(constant, constant)

    def localMemoryStacks(self):
        return self.__localStacks

    def activeMemory(self):
        # Returns the most recent local memory
        return self.localMemoryStacks().top()

    def getAddressValue(self, address):
        try:
            return memAddress[address]
        except:
            raise Exception(
                f"Accessing empty memory address '{address}'")

    def assignAddressValue(self, value, address):
        try:
            memAddress[address] = value
        except:
            raise Exception(
                f"Assigning to an empty memory address '{address}'")
