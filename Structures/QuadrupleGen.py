class QuadrupleGen:
       
    # Singleton class
    __instance = None

    @classmethod
    def get(arg):
        if QuadrupleGen.__instance is None:
            QuadrupleGen()
        return QuadrupleGen.__instance

    def __init__(self):
        if QuadrupleGen.__instance:
            raise Exception(
                "Quadruple Generator already declared, use 'QuadrupleGen.get()'")
        else:
            QuadrupleGen.__instance = self
            self.__quadruples = []
            self.__pendingJumps = []
            self.__tempCounter = 0

    def quadruples(self):
        return self.__quadruples
    
    def pendingJumps(self):
        return self.__pendingJumps
    
    def tempCounter(self):
        return self
    
    def generateTemp(self):
        temp = f"t{self.__tempCounter}"
        self.__tempCounter += 1
        return temp

    def generateQuadruple(self, operator, operand1, operand2, result, addQuad=True):
        if addQuad:
            quadruple = [operator, operand1, operand2, result]
            self.__quadruples.append(quadruple)
            print(f"-> Generated and added quadruple: {quadruple}")
        else:
            quadruple = [operator, operand1, operand2, result]
            print(f"-> Generated quadruple: {quadruple}")
        return quadruple


    def printQuadruples(self):
        for i, quad in enumerate(self.__quadruples):
            print(f"{i}: {quad}")

    def addPendingJump(self, jump):
        self.__pendingJumps.append(jump)