from Structures.SemanticCube import get_cube


# All actions that lead to quadruple generating are to be
# found in this file, this is to make the lexer_parser code
# look a little bit cleaner


def checkTypes(left_op, right_op, operator):
        # Uses semantic cube to match types
        cube = get_cube()
        try:
            res = cube[left_op][right_op][operator]
            if res == 'error':
                raise Exception("Type Mismatch")
            return res
        except Exception as err:
            raise Exception(
                f'ERROR: Operands might not exist.\nLeft op type: {left_op}\nRight op type: {right_op}\nOperator: {operator}\nError: {err}')

def operationsActions(st, qg):
    # Get operands and types involved
    rOp = st.operands().pop()
    rType = st.op_types().pop()
    lOp = st.operands().pop()
    lType = st.op_types().pop()
    op = st.operators().pop()
    # Check typing
    resultType = checkTypes(lType, rType, op)
    # Create temporal var
    temp_var = qg.generate_temp()
    # Generate quad and store resulting operands and type in the operands and op_types stacks
    qg.generate_quadruple(op, lOp, rOp, temp_var)
    st.operands().push(temp_var)
    st.op_types().push(resultType)
    print("pushed:", {temp_var}, "it's type is", {resultType})

def normalAssignationActions(st, qg):
    rOp = ''
    lOp = st.operands().pop()
    lType = st.op_types().pop()
    op = '='
    print("This is the var to assign:", st.var_to_assign().top())
    resultVar = st.var_to_assign().pop()
    resultVarType = st.current_scope().get_var_from_id(resultVar).var_type()
    if resultVarType != lType:
         raise Exception(
              f'ERROR: Type mismatch during variable assignation \n {resultVar} was expecting: {resultVarType} and recieved: {lOp}: {lType}')
    qg.generate_quadruple(op, lOp, rOp, resultVar)

def functionAssignationActions(st, qg):
    return


#####################
# IF
# Evaluación de expresión Booleana (> x y tb)
# (gotof, 'tb' , '', salto_pendiente) -> Quad falso
# (+, i, x, t99)
# (goto '', '', salto_pendiente) -> final
# (else)
#  Quad falso
#  Código dentro del else
#  final

def createGotoFQuadIf(st, qg):
    resulting_type = st.op_types().pop()
    if resulting_type != 'bool':
        raise Exception(
            f'ERROR: Type mismatch during if condition evaluation, expected bool, recieved: {resulting_type}')
    
    # Generate gotof quad
    gotof_quad = qg.generate_quadruple('gotof', st.operands().pop(), '', '')
    # Push gotof quad to pending jumps stack
    qg.add_pending_jump(gotof_quad)

def createGotoQuadIf(qg):
    # Generate goto quad
    goto_quad = qg.generate_quadruple('goto', '', '', '')
    # updatePendingJump(qg)
    # Push goto quad to pending jumps stack
    qg.add_pending_jump(goto_quad)

def updatePendingJumpIf(qg, offset=0):
    # Update the goto or gotof in the pending jumps stack
    pending_goto = qg.pending_jumps().pop()
    pending_goto[3] = len(qg.quadruples()) + 1 + offset

#######################
# WHILE
# Evaluación de expresión Booleana (>, x, y, t3) = Quad inicial
# (gotof, 'tb' , '', salto_pendiente) -> Quad
# Codigo dentro del while
# goto Quad inicial

def whileStatementActions(st, qg):
    resulting_type = st.op_types().pop()
    if resulting_type != 'bool':
        raise Exception(
            f'ERROR: Type mismatch during if statement evaluation, expected bool, recieved: {resulting_type}')
    
    else:
        gotof_quad = qg.generate_quadruple('gotof', st.operands().pop(), '', '')
        # Push gotof quad to pending jumps stack
        qg.add_pending_jump(gotof_quad)
        qg.quadruples().append(gotof_quad)

def createGotoFQuadWhile(st, qg):
    resulting_type = st.op_types().pop()
    if resulting_type != 'bool':
        raise Exception(
            f'ERROR: Type mismatch during while condition evaluation, expected bool, recieved: {resulting_type}')
    
    # Generate gotof quad
    gotof_quad = qg.generate_quadruple('gotof', st.operands().pop(), '', '')
    # Push gotof quad to pending jumps stack
    qg.add_pending_jump(gotof_quad)

def updatePendingJumpWhile(qg, offset=-1):
    # Update the gotof in the pending jumps stack
    pending_goto = qg.pending_jumps().pop()

    # Search for pending_goto in the quadruples and get its index
    index = qg.quadruples().index(pending_goto) - 1
    # Generate goto quad
    goto_quad = qg.generate_quadruple('goto', '', '', index)
    pending_goto[3] = len(qg.quadruples()) + 1 + offset
