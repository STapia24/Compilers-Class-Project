from Structures.CustomStack import Stack

# Assigning ranges for the memory scopes
ranges = {
    'global': { 'int': 1000, 'float': 2000, 'bool': 3000, 'char': 4000 },
    'local': { 'int': 10000, 'float': 11000, 'bool': 12000, 'char': 13000 },
    'temp': { 'int': 20000, 'float': 21000, 'bool': 22000, 'char': 23000 }
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
        self.__remainingMemory = {
            'int': memSize, 'float': memSize, 'bool': memSize, 'char': memSize}

    def getVars(self, addressType):
        if addressType == 'int':
            return self.__int
        if addressType == 'float':
            return self.__float
        if addressType == 'bool':
            return self.__bool
        if addressType == 'char':
            return self.__char

    def findAddress(self, varId, recursiveLookup=True):
        # print(f"-> finding address for '{varId}'")
        ints = self.getVars('int')
        if varId in ints:
            return ints[varId], 'int'

        floats = self.getVars('float')
        if varId in floats:
            return floats[varId], 'float'

        bools = self.getVars('bool')
        if varId in bools:
            return bools[varId], 'bool'

        chars = self.getVars('char')
        if varId in chars:
            return chars[varId], 'char'
        
        # Looks among the constants in case variable has not been found
        if recursiveLookup:
            memory = Memory.get()
            constants = memory.getConsts()
            try:
                address, varType = constants.findAddress(varId, False)
            except:
                address = None
            if not address:
                globalMem = memory.getGlobalMemory()
                address, varType = globalMem.findAddress(varId, False)
                if not address:
                    raise Exception(
                        f"Could not find address for variable '{varId}'")
            return address, varType
        raise Exception(f"Could not find address for variable '{varId}'")

    def initAddress(self, varId, addressType, scope):
        try:
            assignedAddress = self.getVars(addressType)
            # the index is the base memory address and we set it to the address
            memoryIndex = ranges[scope][addressType]
            assignedAddress[varId] = memoryIndex
            # set the new index in memory
            ranges[scope][addressType] = memoryIndex + 1
            # inits
            memAddress[memoryIndex] = None
        except Exception as err:
            print(err)
        self.__remainingMemory[addressType] -= 1
        if self.__remainingMemory[addressType] <= 0:
            raise Exception(f'Ran out of memory for \'{addressType}\' type')

    def setVal(self, resId, valueId):
        valueAddress, _ = self.findAddress(valueId)
        setThisAddress, _ = self.findAddress(resId)
        memAddress[setThisAddress] = memAddress[valueAddress]

    def setConstVal(self, resId, value, valueType=None):
        if valueType == None:
            address, _ = self.findAddress(resId)
            memAddress[address] = value
        else:
            address, var_type = self.findAddress(resId)
            if valueType == var_type:
                memAddress[address] = value
            else:
                raise Exception(
                    f'Type mismatch: unable to assign {value} of type \'{valueType}\' to variable \'{resId}\' of type \'{var_type}\''
                )

    def print(self):
        # Used only for debugging
        ints = self.getVars('int')
        print('ints', ints)
        floats = self.getVars('float')
        print('floats', floats)
        bools = self.getVars('bool')
        print('bools', bools)
        chars = self.getVars('char')
        print('chars', chars)

    def getVal(self, varId):
        address, _ = self.findAddress(varId)
        if not address:
            # If there's no address then it means it's a constant and thus has to be searched as one
            memory = Memory.get()
            constants = memory.getConsts()
            constantValue = constants.getVal(varId)
            return constantValue
        return memAddress[address]
    
    def getAddressValue(self, address):
        try:
            return memAddress[address]
        except:
            raise Exception(
                f"Accessing empty memory address '{address}'")

    def assignAddressValue(self, value, address):
        try:
            memAddress[address] = value
            # print("Stored:", value, "in address:", address)
        except:
            raise Exception(
                f"Assigning to an empty memory address '{address}'")




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
