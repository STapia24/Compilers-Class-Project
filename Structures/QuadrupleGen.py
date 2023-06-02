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
            self.__pending_jumps = []
            self.__temp_counter = 0

    def quadruples(self):
        return self.__quadruples
    
    def pending_jumps(self):
        return self.__pending_jumps
    
    def temp_counter(self):
        return self
    
    def generate_temp(self):
        temp = f"t{self.__temp_counter}"
        self.__temp_counter += 1
        return temp

    def generate_quadruple(self, operator, operand1, operand2, result):
        quadruple = [operator, operand1, operand2, result]
        self.__quadruples.append(quadruple)
        print(f"-> Generated quadruple: {quadruple}")
        return quadruple


    def print_quadruples(self):
        for i, quad in enumerate(self.__quadruples):
            print(f"{i}: {quad}")

    def add_pending_jump(self, jump):
        self.__pending_jumps.append(jump)