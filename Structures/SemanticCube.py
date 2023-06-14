I = 'int'
F = 'float'
C = 'char'
B = 'bool'
E = 'err'

# Some values are repeated for faster search time, instead of checking for permutations
# it will find the permutation in the cube

def getCube():
    # This is a dictionary of dicionaries where we have I, F, C and B as keys for 
    # the first and second sets of dictionaries and then the operators as the third key
    cube = {}
    cube[I] = {}
    cube[I][I] = {}
    cube[I][F] = {}
    cube[I][C] = {}
    cube[I][B] = {}

    cube[I][I]['+'] = I
    cube[I][I]['-'] = I
    cube[I][I]['/'] = I
    cube[I][I]['*'] = I
    cube[I][I]['&&'] = E
    cube[I][I]['||'] = E
    cube[I][I]['>'] = B
    cube[I][I]['<'] = B
    cube[I][I]['>='] = B
    cube[I][I]['<='] = B
    cube[I][I]['=='] = B
    cube[I][I]['!='] = B

    cube[I][F]['+'] = F
    cube[I][F]['-'] = F
    cube[I][F]['/'] = F
    cube[I][F]['*'] = F
    cube[I][F]['&&'] = E
    cube[I][F]['||'] = E
    cube[I][F]['>'] = B
    cube[I][F]['<'] = B
    cube[I][F]['>='] = B
    cube[I][F]['<='] = B
    cube[I][F]['=='] = B
    cube[I][F]['!='] = B

    cube[I][C]['+'] = E
    cube[I][C]['-'] = E
    cube[I][C]['/'] = E
    cube[I][C]['*'] = E
    cube[I][C]['&&'] = E
    cube[I][C]['||'] = E
    cube[I][C]['>'] = E
    cube[I][C]['<'] = E
    cube[I][C]['>='] = E
    cube[I][C]['<='] = E
    cube[I][C]['=='] = E
    cube[I][C]['!='] = E

    cube[I][B]['+'] = E
    cube[I][B]['-'] = E
    cube[I][B]['/'] = E
    cube[I][B]['*'] = E
    cube[I][B]['&&'] = E
    cube[I][B]['||'] = E
    cube[I][B]['>'] = E
    cube[I][B]['<'] = E
    cube[I][B]['>='] = E
    cube[I][B]['<='] = E
    cube[I][B]['=='] = E
    cube[I][B]['!='] = E

    cube[F] = {}
    cube[F][I] = {}
    cube[F][F] = {}
    cube[F][C] = {}
    cube[F][B] = {}

    cube[F][I]['+'] = F
    cube[F][I]['-'] = F
    cube[F][I]['/'] = F
    cube[F][I]['*'] = F
    cube[F][I]['&&'] = E
    cube[F][I]['||'] = E
    cube[F][I]['>'] = B
    cube[F][I]['<'] = B
    cube[F][I]['>='] = B
    cube[F][I]['<='] = B
    cube[F][I]['=='] = B
    cube[F][I]['!='] = B

    cube[F][F]['+'] = F
    cube[F][F]['-'] = F
    cube[F][F]['/'] = F
    cube[F][F]['*'] = F
    cube[F][F]['&&'] = E
    cube[F][F]['||'] = E
    cube[F][F]['>'] = B
    cube[F][F]['<'] = B
    cube[F][F]['>='] = B
    cube[F][F]['<='] = B
    cube[F][F]['=='] = B
    cube[F][F]['!='] = B

    cube[F][C]['+'] = E
    cube[F][C]['-'] = E
    cube[F][C]['/'] = E
    cube[F][C]['*'] = E
    cube[F][C]['&&'] = E
    cube[F][C]['||'] = E
    cube[F][C]['>'] = E
    cube[F][C]['<'] = E
    cube[F][C]['>='] = E
    cube[F][C]['<='] = E
    cube[F][C]['=='] = E
    cube[F][C]['!='] = E

    cube[F][B]['+'] = E
    cube[F][B]['-'] = E
    cube[F][B]['/'] = E
    cube[F][B]['*'] = E
    cube[F][B]['&&'] = E
    cube[F][B]['||'] = E
    cube[F][B]['>'] = E
    cube[F][B]['<'] = E
    cube[F][B]['>='] = E
    cube[F][B]['<='] = E
    cube[F][B]['=='] = E
    cube[F][B]['!='] = E

    cube[C] = {}
    cube[C][I] = {}
    cube[C][F] = {}
    cube[C][C] = {}
    cube[C][B] = {}

    cube[C][I]['+'] = E
    cube[C][I]['-'] = E
    cube[C][I]['/'] = E
    cube[C][I]['*'] = E
    cube[C][I]['&&'] = E
    cube[C][I]['||'] = E
    cube[C][I]['>'] = E
    cube[C][I]['<'] = E
    cube[C][I]['>='] = E
    cube[C][I]['<='] = E
    cube[C][I]['=='] = E
    cube[C][I]['!='] = E

    cube[C][F]['+'] = E
    cube[C][F]['-'] = E
    cube[C][F]['/'] = E
    cube[C][F]['*'] = E
    cube[C][F]['&&'] = E
    cube[C][F]['||'] = E
    cube[C][F]['>'] = E
    cube[C][F]['<'] = E
    cube[C][F]['>='] = E
    cube[C][F]['<='] = E
    cube[C][F]['=='] = E
    cube[C][F]['!='] = E

    cube[C][C]['+'] = E
    cube[C][C]['-'] = E
    cube[C][C]['/'] = E
    cube[C][C]['*'] = E
    cube[C][C]['&&'] = E
    cube[C][C]['||'] = E
    cube[C][C]['>'] = E
    cube[C][C]['<'] = E
    cube[C][C]['>='] = E
    cube[C][C]['<='] = E
    cube[C][C]['=='] = B
    cube[C][C]['!='] = B

    cube[C][B]['+'] = E
    cube[C][B]['-'] = E
    cube[C][B]['/'] = E
    cube[C][B]['*'] = E
    cube[C][B]['&&'] = E
    cube[C][B]['||'] = E
    cube[C][B]['>'] = E
    cube[C][B]['<'] = E
    cube[C][B]['>='] = E
    cube[C][B]['<='] = E
    cube[C][B]['=='] = E
    cube[C][B]['!='] = E

    cube[B] = {}
    cube[B][I] = {}
    cube[B][F] = {}
    cube[B][C] = {}
    cube[B][B] = {}

    cube[B][I]['+'] = E
    cube[B][I]['-'] = E
    cube[B][I]['/'] = E
    cube[B][I]['*'] = E
    cube[B][I]['&&'] = E
    cube[B][I]['||'] = E
    cube[B][I]['>'] = E
    cube[B][I]['<'] = E
    cube[B][I]['>='] = E
    cube[B][I]['<='] = E
    cube[B][I]['=='] = E
    cube[B][I]['!='] = E

    cube[B][F]['+'] = E
    cube[B][F]['-'] = E
    cube[B][F]['/'] = E
    cube[B][F]['*'] = E
    cube[B][F]['&&'] = E
    cube[B][F]['||'] = E
    cube[B][F]['>'] = E
    cube[B][F]['<'] = E
    cube[B][F]['>='] = E
    cube[B][F]['<='] = E
    cube[B][F]['=='] = E
    cube[B][F]['!='] = E

    cube[B][C]['+'] = E
    cube[B][C]['-'] = E
    cube[B][C]['/'] = E
    cube[B][C]['*'] = E
    cube[B][C]['&&'] = E
    cube[B][C]['||'] = E
    cube[B][C]['>'] = E
    cube[B][C]['<'] = E
    cube[B][C]['>='] = E
    cube[B][C]['<='] = E
    cube[B][C]['=='] = E
    cube[B][C]['!='] = E

    cube[B][B]['+'] = E
    cube[B][B]['-'] = E
    cube[B][B]['/'] = E
    cube[B][B]['*'] = E
    cube[B][B]['&&'] = B
    cube[B][B]['||'] = B
    cube[B][B]['>'] = E
    cube[B][B]['<'] = E
    cube[B][B]['>='] = E
    cube[B][B]['<='] = E
    cube[B][B]['=='] = B
    cube[B][B]['!='] = B

    return cube

def checkTypes(leftOp, rightOp, operator):
        # Uses semantic cube to match types
        cube = getCube()
        try:
            res = cube[leftOp][rightOp][operator]
            if res == 'error':
                raise Exception("Type Mismatch")
            return res
        except Exception as err:
            raise Exception(
                f'ERROR: Operands missing \nLeft op type: {leftOp}\nRight op type: {rightOp}\nOperator: {operator}\nError: {err}')