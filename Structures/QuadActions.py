from Structures.SemanticCube import checkTypes
from Structures.FunctionDir import *


# All actions that lead to quadruple generating are to be
# found in this file, this is to make the lexer_parser code
# look a little bit cleaner

############ Main Handling ############

def saveMainQuad(qg):
    mainQuad = qg.generateQuadruple('goto', 'main', '', '')
    qg.addPendingJump(mainQuad)

def solveMainQuad(qg):
    mainQuad = qg.pendingJumps().pop()
    mainQuad[3] = len(qg.quadruples())


############ Var or constant assignations ############

def operationsActions(st, qg):
    # Get operands and types involved
    rOp = st.operands().pop()
    rType = st.opTypes().pop()
    lOp = st.operands().pop()
    lType = st.opTypes().pop()
    op = st.operators().pop()
    # Check typing
    resultType = checkTypes(lType, rType, op)
    # Create temporal var
    tempVar = qg.generateTemp()
    # Generate quad and store resulting operands and type in the operands and op_types stacks
    qg.generateQuadruple(op, lOp, rOp, tempVar)
    st.operands().push(tempVar)
    st.opTypes().push(resultType)
    # print("pushed:", {temp_var}, "it's type is", {resultType})

def normalAssignationActions(st, qg):
    rOp = ''
    lOp = st.operands().pop()
    lType = st.opTypes().pop()
    op = '='
    # print("This is the var to assign:", st.var_to_assign().top())
    resultVar = st.varToAssign().pop()
    resultVarType = st.currentScope().getVarFromId(resultVar).varType()
    if resultVarType != lType:
         raise Exception(
              f'ERROR: Type mismatch during variable assignation \n {resultVar} was expecting: {resultVarType} and recieved: {lOp}: {lType}')
    qg.generateQuadruple(op, lOp, rOp, resultVar)

############ Function call assignation ############

###############################################################
# Function Call
# (ERA, '', '', funcName) 
# solve params // ex. (+, A, B, tx)
# (PARAM, tx, '', parameterName) -> Repeat for each parameter
# (GOSUB, '', '', funcName)
# ENDFUNC
###############################################################

def functionAssignationActions(st, qg, params):
    resultVar = st.varToAssign().pop()
    resultVarType = st.currentScope().getVarFromId(resultVar).varType()
    funcId = params[-1][0]
    funcReturnType = st.currentScope().getFuncFromId(funcId).returnType()
    if resultVarType != funcReturnType:
        raise Exception(
            f'Problem while assigning variable {resultVar}: types do not match.\nVariable to assign: {resultVar}\nFunction: {funcId}\nFunction return type: {funcReturnType}')
    qg.generateQuadruple('FASSGN', resultVar, '', funcId)

def paramAssignQuads(st, qg):
    funcName = st.currentParams().pop(0)
    paramValues = st.currentParams()
    function = st.currentScope().getFuncFromId(funcName)
    # Gets parameter names
    paramNames = []
    paramsList = function.params()
    for param in paramsList:
        paramNames.append(param[0])
    # For each parameter does type check then creates the param quadruple (PARAM, value, '', varName)
    for i in range(len(paramNames)):
        leftType = st.currentScope().getVarFromId(paramNames[i]).varType()
        rightParams = getParams(funcName)
        rightType = None
        for param in rightParams:
            if param[0] == paramNames[i]:
                rightType = param[1]
        if leftType != rightType:
            raise Exception(
                f'Type mismatch: expected \'{rightType}\' parameter but received \'{leftType}\'')
        qg.generateQuadruple('PARAM', paramValues[i][0], '', paramNames[i])

def gosubJump(st, qg):
    funcJump = qg.pendingJumps().pop()
    op, left, right, res = funcJump
    qg.generateQuadruple(op, left, right, res)

def setReturn(st, qg):
    functionType = st.currentScope().getFuncFromId(st.currentScopeName()).returnType()
    varType = st.currentScope().getVarFromId(st.operands().top()).varType()
    if functionType != varType:
        raise Exception(f'Problem while returning value for function \'{st.currentScopeName()}\': types do not match.\nFunction type: {functionType}\nVariable type: {varType}')
    qg.generateQuadruple('RETURN', '', '', st.operands().top())
    setReturnVarId(st.currentScopeName(), st.operands().pop())
    qg.generateQuadruple('goto', 'ENDFUNC', '', '')

def saveFuncCallOp(st):
    # Saves function return variable in operands Stack
    st.operands().push(getReturnVarId(st.currentScopeName()))
    # Saves return var as current
    currentVar = st.currentScope().getVarFromID(getReturnVarId(st.currentScopeName()))
    # Saves return var type in opTypes Stack
    st.opTypes().push(currentVar.varType())
    print("Pushed:", currentVar, "to operand stack and", currentVar.varType(), "to opType stack")

############ Non-linear Statements ############

###############################################################
# IF
# Boolean expresion eval // ex. (>, x, y, tb)
# (gotof, 'tb' , '', pendingJump) -> false jump quad
# if block
# (goto '', '', pendingJump) -> final
#  ELSE
#  solve false jump quad
#  else block
#  solve final pendingJump
###############################################################

def createGotoFQuadIf(st, qg):
    resultingType = st.opTypes().pop()
    if resultingType != 'bool':
        raise Exception(
            f'ERROR: Type mismatch during if condition evaluation, expected bool, recieved: {resultingType}')
    
    # Generate gotof quad
    gotofQuad = qg.generateQuadruple('gotof', st.operands().pop(), '', '')
    # Push gotof quad to pending jumps stack
    qg.addPendingJump(gotofQuad)

def createGotoQuadIf(qg):
    # Generate goto quad
    gotoQuad = qg.generateQuadruple('goto', '', '', '')
    # updatePendingJump(qg)
    # Push goto quad to pending jumps stack
    qg.addPendingJump(gotoQuad)

def updatePendingJumpIf(qg):
    # Update the goto or gotof in the pending jumps stack
    pendingGoto = qg.pendingJumps().pop()
    gotoType = pendingGoto[0]

    if gotoType == 'goto':
        pendingGoto[3] = len(qg.quadruples())
    else:
        pendingGoto[3] = len(qg.quadruples()) + 1
        

#####################################################################
# WHILE
# Boolean expresion eval // ex. (>, x, y, tb) = initial quad
# (gotof, 'tb' , '', pendingJump) -> false jump quad
# While block
# create goto initial quad
# solve false jump
######################################################################

def whileStatementActions(st, qg):
    resultingType = st.opTypes().pop()
    if resultingType != 'bool':
        raise Exception(
            f'ERROR: Type mismatch during if statement evaluation, expected bool, recieved: {resultingType}')
    
    else:
        gotofQuad = qg.generateQuadruple('gotof', st.operands().pop(), '', '')
        # Push gotof quad to pending jumps stack
        qg.addPendingJump(gotofQuad)
        qg.quadruples().append(gotofQuad)

def createGotoFQuadWhile(st, qg):
    resultingType = st.opTypes().pop()
    if resultingType != 'bool':
        raise Exception(
            f'ERROR: Type mismatch during while condition evaluation, expected bool, recieved: {resultingType}')
    
    # Generate gotof quad
    gotofQuad = qg.generateQuadruple('gotof', st.operands().pop(), '', '')
    # Push gotof quad to pending jumps stack
    qg.addPendingJump(gotofQuad)

def updatePendingJumpWhile(qg):
    # Update the gotof in the pending jumps stack
    pendingGoto = qg.pendingJumps().pop()

    # Search for pendingGoto in the quadruples and get its index
    index = qg.quadruples().index(pendingGoto) - 1
    # Generate goto quad
    qg.generateQuadruple('goto', '', '', index)
    pendingGoto[3] = len(qg.quadruples())



# Missing array actions


################# Reusable functions #################

# Used to flatten tuples of tuples recursively
def flattenData(data):
    if isinstance(data, tuple):
        if len(data) == 0:
            return ()
        else:
            return flattenData(data[0]) + flattenData(data[1:])
    else:
        if data == None:
            return ()
        return (data,)
    
def isConstant(operand):
    # Checks for a boolean constant
    if operand == 'True' or operand == 'False':
        return True
    # Checks for a numeric constants
    return type(operand) == int or type(operand) == float