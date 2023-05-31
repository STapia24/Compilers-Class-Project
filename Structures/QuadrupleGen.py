class QuadrupleGen:
    
    # Singleton class
    __instance = None

    @classmethod
    def get(arg):
        if QuadrupleGen.__instance is None:
            QuadrupleGen()
        return QuadrupleGen.__instance

    def __init__(self):
        self.__quadruples = []
        self.__pendingJumps = []
        self.__temp_counter = 0

    def generate_temp(self):
        temp = f"t{self.__temp_counter}"
        self.__temp_counter += 1
        return temp

    def generate_quadruple(self, operator, operand1, operand2, result):
        quadruple = (operator, operand1, operand2, result)
        self.__quadruples.append(quadruple)

    def print_quadruples(self):
        for i, quad in enumerate(self.__quadruples):
            print(f"{i}: {quad}")

    def addPendingJump(self, jump):
        self.__pendingJumps.append(jump)