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

def functionAssignationActions():
    return
