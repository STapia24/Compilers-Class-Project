# Function Directory contains a dictionary with
# key: funcId (The function name)
# val:
#   dir -> quad index -> (Index of the quad where it begins)
#   return -> endfunc quad -> (Index of the quad where it ends)
#   returnVar -> id to return -> (Name of the variable that it returns)
#   params -> list of str tuples(id, type) -> (Name, type) of the vars in parameters
#   localVars -> st of str tuples(id, type) -> (Name, type) of the local vars inside the func

FuncDirectory = {}
func_prefix = ''

def exists(funcId):
    if funcId not in FuncDirectory:
        raise Exception(f'Function \'{funcId}\' not found in function directory')
    return funcId


def isNewFunction(funcId):
    if funcId in FuncDirectory:
        raise Exception(f'Function \'{funcId}\' already declared in function directory')
    return funcId

# Used just for debugging
def get():
    return FuncDirectory


def setReturnQuad(funcId, returningQuad):
    funcId = exists(funcId)
    FuncDirectory[funcId]['return'] = returningQuad

# Called when assignation of function, returnTo is the returning quad + 1
def setReturnQuadVal(funcId, returnTo):
    funcId = exists(funcId)
    FuncDirectory[funcId]['return'].set_res(returnTo)


def setReturnVarId(funcId, returnVarId):
    funcId = exists(funcId)
    FuncDirectory[funcId]['return_var'] = returnVarId


def getReturnVarId(funcId):
    funcId = exists(funcId)
    return FuncDirectory[funcId]['return_var']


def saveFuncToDir(funcId, startingQuadPosition):
    funcId = isNewFunction(funcId)
    # Creates a new function with empty values
    FuncDirectory[funcId] = {
        'dir': startingQuadPosition, 'return': None, 'return_var': None, 'params': None, 'localVars': None}


def setFuncStartingQuad(funcId, startingQuadPosition):
    funcId = exists(funcId)
    FuncDirectory[funcId]['dir'] = startingQuadPosition


def getFunc(funcId):
    # gets the starting quad index
    funcId = exists(funcId)
    return FuncDirectory[funcId]['dir']


def getParams(funcId):
    return FuncDirectory[funcId]['params']


def saveParams(st):
    # gets function object using scope name to get params
    currScope = st.currentScope()
    funcId = st.currentScopeName()
    params = st.currentParams()
    funcObj = currScope.getFuncFromId(funcId)
    funcObj.setParams(params)

    funcId = exists(funcId)
    FuncDirectory[funcId]['params'] = params

    for param in params:
        st.currentScope().addVar(param[0], param[1])


def saveLocalVars(st):
    # gets all vars from current scope and saves them to directory
    localVars = st.currentScope().vars()
    funcId = st.currentScopeName()
    funcId = exists(funcId)
    formattedVars = []
    for key in localVars:
        try:
            formattedVars.append(
                (localVars[key].name(), localVars[key].varType()))
        except Exception as err:
            print(err)
    FuncDirectory[funcId]['localVars'] = formattedVars


def saveTempVar(st, varName, varType):
    # saves temp vars as local vars to be used in ERA
    funcId = st.currentScopeName()
    funcId = exists(funcId)
    FuncDirectory[funcId]['localVars'].append((varName, varType))


def getLocalVar(funcId):
    funcId = exists(funcId)
    return FuncDirectory[funcId]['localVars']