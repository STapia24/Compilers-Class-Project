from Structures.SymbolTable import SymbolTable
from Structures.Memory import Memory
from Structures.CustomStack import pushOp, popOp
from Structures.QuadrupleGen import *
from Structures.SemanticCube import *
from Structures.QuadActions import *
import ply.yacc as yacc
import ply.lex as lex


def initTableAndQuads():
    SymbolTable()
    QuadrupleGen()

reserved = {
    "program": "PROGRAM",
    "main": "MAIN",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "func": "FUNC",
    "mean": "MEAN",
    "median": "MEDIAN",
    "mode": "MODE",
    "std": "STD",
    "variance": "VARIANCE",
    "hist": "HIST",
    "plot": "PLOT",
    "sctplot": "SCTPLOT",
    "return": "RETURN",
    "read": "READ",
    "print": "PRINT",
    "void": "VOID",
    "int": "INT",
    "float": "FLOAT",
    "char": "CHAR",
    "dataframe": "DATAFRAME",
}

tokens = [
    "LSB",
    "RSB",
    "LP",
    "RP",
    "LBR",
    "RBR",
    "COMMA",
    "SEMICOLON",
    "PERIOD",
    "ID",
    "AND",
    "OR",
    "GT",
    "LE",
    "GE",
    "LT",
    "EQ",
    "NEQ",
    "ASSIGN",
    "PLUS",
    "MINUS",
    "MULT",
    "DIV",
    "CONST_INT",
    "CONST_FLOAT",
    "CONST_CHAR",
    "CONST_STRING"
]

tokens = tokens + list(reserved.values())

# Regular expressions for tokens
t_LSB = r"\["
t_RSB = r"\]"
t_LP = r"\("
t_RP = r"\)"
t_LBR = r"\{"
t_RBR = r"\}"
t_COMMA = r","
t_SEMICOLON = r";"
t_PERIOD = r"\."
t_AND = r"&&"
t_OR = r"\|\|"
t_GT = r">"
t_LT = r"<"
t_EQ = r"=="
t_NEQ = r"!="
t_LE = r"<="
t_GE = r">="
t_ASSIGN = r"="
t_PLUS = r"\+"
t_MINUS = r"-"
t_MULT = r"\*"
t_DIV = r"\/"

# Ignored characters (spaces and tabs)
t_ignore = " \t\r\f"

# ID tokens and reserved words lookup
def t_ID(t):
    r"[a-zA-Z_]\w*"
    t.type = reserved.get(t.value, "ID")
    return t

def t_CONST_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_CONST_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_CONST_CHAR(t):
    r"'(\\'|\\n|\\\\|[^\n']|)'"
    if t.value == r"'\'":
        t.value = r'\\'
    elif t.value == r"'\n'":
        t.value = '\n'
    elif t.value == r"'\''":
        t.value = "'"
    elif t.value == r"''":
        t.value = ''
    else:
        t.value = t.value[1]
    return t


def t_CONST_STRING(t):
    r'"(\\"|[^\n"])+"'
    return t

# Define a rule to handle newlines
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NEQ', 'LE', 'GE', 'LT', 'GT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),
)

############## GRAMMAR ##############

# program
def p_program(p):
    '''program : PROGRAM ID SEMICOLON goto_main var_dec save_vars_in_fd func_dec solve_main_quad main'''
    p[0] = tuple[1:]
    # print("Got to program")

    # main
def p_main(p):
    '''main : MAIN LP RP block SEMICOLON'''
    # print("Got into main")

# block
def p_block(p):
    '''block : LBR statute statute1 RBR '''
    # print("Found a block")

# func_dec
def p_func_dec(p):
    '''func_dec : FUNC return_type ID save_id save_func push_scope LP param_opt save_params_in_fd RP func_block pop_scope func_dec
    | empty'''
    # print("Function declared")

# param_opt
def p_param_opt(p):
    '''param_opt : type_simple save_type ID save_id save_operand_1 save_params more_param_opt'''
    # print("Got to param_opt")

# more_param_opt
def p_more_param_opt(p):
    '''more_param_opt : COMMA param_opt
    | empty'''
    # print("Got to more_param_opt")

# var_dec
def p_var_dec(p):
    ''' var_dec : type_simple ID save_id save_var dim SEMICOLON var_dec
    | empty
    '''
    p[0] = tuple(p[1:])
    # print("Declared a variable")

# complex_dec
def p_complex_dec(p):
    '''
    complex_dec : COMMA ID complex_dec
    | empty
    '''
    # print("Declared another complex type")

# dim
def p_dim(p):
    '''dim : LSB CONST_INT RSB
    | empty'''
    p[0] = tuple(p[1:])
    # print("Dimensions while declaring variable")

# return_type
def p_return_type(p):
    '''return_type : type_simple
    | VOID save_type'''
    p[0] = p[1]
    #print("Returning a simple type or void")

# type_simple
def p_type_simple(p):
    '''type_simple : INT save_type
    | FLOAT save_type
    | CHAR save_type'''
    p[0] = p[1]
#    print("Found a simple type")

# type_complex
def p_type_complex(p):
    '''type_complex : DATAFRAME'''
    # print("Found a dataframe")

# assignation
def p_assignation(p):
    '''assignation : var assignation_var ASSIGN exp_or_func_assignation'''
    p[0] = tuple(p[1:])
    # print("Assignation")

# exp_or_func_assignation
def p_exp_or_func_assignation(p):
    '''exp_or_func_assignation : expression_assignation
    | func_call assign_func'''
    p[0] = tuple(p[1:])
    # print("Assignation of exp or function call")

# expression_assignation
def p_expression_assignation(p):
    '''expression_assignation : exp normal_assign SEMICOLON'''
    p[0] = tuple(p[1:])
    # print("Assignation of exp")

# var
def p_var(p):
    '''var : ID exp_dim_opt'''
    p[0] = p[1]
    # print("Variable use")

# Exp_dim_opt
def p_exp_dim_opt(p):
    '''exp_dim_opt : LSB exp RSB
    | empty'''
    # print("Dimensions when using variable")

# if_statement
def p_if_statement(p):
    '''if_statement : IF LP super_exp RP create_gotof block else update_pending_jump_1'''
    p[0] = tuple(p[1:])
    # print("If statement")

# else
def p_else(p):
    '''else : create_goto ELSE block
    | empty'''
    p[0] = tuple(p[1:])
    # print("Else statement")

# while_statement
def p_while_statement(p):
    '''while_statement : WHILE LP super_exp RP create_gotof_while block update_pending_jump_while'''
    p[0] = tuple(p[1:])
    # print("While statement")

# read statement
def p_read(p):
    '''read : READ LP var read_quad RP SEMICOLON'''
    p[0] = tuple(p[1:])
    # print("Read something")

# print statement
def p_print(p):
    '''print : PRINT LP CONST_STRING print_quad RP SEMICOLON
    | PRINT LP exp print_quad RP SEMICOLON'''
    p[0] = tuple(p[1:])
    # print("Prints something")
 
# constants
def p_constants(p):
    '''constants : CONST_INT current_type_is_int
    | CONST_FLOAT current_type_is_float
    | CONST_CHAR current_type_is_char'''
    # print("This are constants")
    p[0] = p[1]

# func_call
def p_func_call(p):
    '''func_call : ID set_return_quad LP opt_args assign_params RP assign_gosub SEMICOLON'''
    p[0] = tuple(p[1:])
    # print("Function called")

# opt_args
def p_opt_args(p):
    '''opt_args : exp save_params exp_args_more'''
    p[0] = tuple(p[1:])
    # print("Arguments for a function call")

# exp_args_more
def p_exp_args_more(p):
    '''exp_args_more : COMMA opt_args
    | empty'''
    p[0] = p[1]
    # print("More arguments for a function call")

# statements
def p_statements(p):
    '''statements : assignation
    | if_statement
    | while_statement
    | read
    | func_call
    | return
    | print
    | data_funcs'''
    p[0] = p[1]
    # print("Called a statement")

def p_data_funcs(p):
    '''data_funcs : mean
    | median
    | mode
    | std
    | variance
    | hist
    | plot
    | sctplot'''
    p[0] = p[1]
    # print("Found a data function")

#statute1
def p_statute1(p):
    '''statute1 : statute statute1
    | empty'''
    p[0] = p[1]
    # print("Jumped to statute1")

#statute
def p_statute(p):
    '''statute : statements statute1
    | empty'''
    p[0] = p[1]
    # print("Found a statute")

# func_block
def p_func_block(p):
    ''' func_block : LBR var_dec save_vars_in_fd statute set_endfunc_quad RBR '''
    p[0] = tuple(p[1:])
    # print("Inside function block")

# return
def p_return(p):
    ''' return : RETURN LP exp set_return_stmt RP SEMICOLON '''
    p[0] = tuple(p[1:])
    # print("Returns something")

# super_exp
def p_super_exp(p):
    ''' super_exp : exp relop push_op exp check_relop_stack
    | exp
    '''
    p[0] = tuple(p[1:])
    # print("Found a super_exp")

def p_relop(p):
    ''' relop : EQ
    | GE 
    | LE 
    | GT 
    | LT 
    | NEQ 
    | AND
    | OR
    '''
    p[0] = p[1]

def p_exp(p):
    ''' exp : term check_stack_exp PLUS push_op exp
            | term check_stack_exp MINUS push_op exp
            | term check_stack_exp
    '''
    p[0] = tuple(p[1:])
    # print("Found an exp")

def p_term(p):
    '''term : factor check_stack_term MULT push_op term
            | factor check_stack_term DIV push_op term
            | factor check_stack_term
    '''
    p[0] = tuple(p[1:])
    # print("Found a term")

def p_factor(p):
    '''factor : LP push_op super_exp RP pop_op save_operand
    | constants save_operand
    | var save_operand
    | func_call save_call_operand
    '''
    p[0] = tuple(p[1:])
    # print("Found a factor")

def p_mean(p):
    ''' mean : MEAN LP complex_var RP SEMICOLON '''
    # Code to handle the mean calculation
    # print("Mean")

def p_mode(p):
    ''' mode : MODE LP complex_var RP SEMICOLON '''
    # Code to handle the mode calculation
    # print("Mode")

def p_median(p):
    ''' median : MEDIAN LP complex_var RP SEMICOLON '''
    # Code to handle the median calculation
    # print("Median")

def p_std(p):
    ''' std : STD LP complex_var RP SEMICOLON '''
    # Code to handle the standard deviation calculation
    # print("Standar Deviation")

def p_variance(p):
    ''' variance : VARIANCE LP complex_var RP SEMICOLON '''
    # Code to handle the variance calculation
    # print("Variance")

def p_hist(p):
    ''' hist : HIST LP complex_var RP SEMICOLON '''
    # Code to handle the histogram generation
    # print("Histogram")

def p_plot(p):
    ''' plot : PLOT LP complex_var RP SEMICOLON '''
    # Code to handle the plot generation
    # print("Plot")

def p_sctplot(p):
    ''' sctplot : SCTPLOT LP complex_var RP SEMICOLON '''
    # Code to handle the scatter plot generation
    # print("Scatterplot")

# Complex variable use
def p_complex_var(p):
    ''' complex_var : ID
    | ID PERIOD'''
    # Code to handle complex variable reference
    # print("Complex var use")

# epsilon
def p_empty(p):
    ''' empty : '''
    pass
#    print("Got to an empty production")

######### Semantic nodes functions #########
def p_goto_main(p):
    '''
    goto_main :
    '''
    qg = QuadrupleGen.get()
    saveMainQuad(qg)
    saveFuncToDir('global', len(qg.quadruples()) + 1)

def p_solve_main_quad(p):
    '''
    solve_main_quad :
    '''
    qg = QuadrupleGen.get()
    solveMainQuad(qg)

def p_save_vars_in_fd(p):
    '''
    save_vars_in_fd :
    '''
    st = SymbolTable.get()
    saveLocalVars(st)

def p_save_params_in_fd(p):
    '''
    save_params_in_fd :
    '''
    st = SymbolTable.get()
    saveParams(st)

def p_push_op(p):
    '''
    push_op :
    '''
    st = SymbolTable.get()
    pushOp(st, p[-1])

def p_pop_op(p):
    '''
    pop_op :
    '''
    st = SymbolTable.get()
    popOp(st, p[-1])

def p_save_id(p):
    '''
    save_id :
    '''
    st = SymbolTable.get()
    # print("The id is:", p[-1])
    st.setCurrId(p[-1])

def p_save_type(p):
    '''
    save_type : 
    '''
    st = SymbolTable.get()
    # print("The type is:", p[-1])
    st.setCurrType(p[-1])

def p_save_var(p):
    '''
    save_var : 
    '''
    st = SymbolTable.get()
    st.saveVar()
    
def p_save_operand(p):
    '''
    save_operand :
    '''
    st = SymbolTable.get()
    st.operands().push(p[-1])
    #print("pushing:", p[-1])
    st.opTypes().push(st.currentType())

def p_save_operand_1(p):
    '''
    save_operand_1 :
    '''
    st = SymbolTable.get()
    st.operands().push(p[-2])
    st.opTypes().push(st.currentType())

def p_check_relop_stack(p):
    '''
    check_relop_stack :
    '''
    st = SymbolTable.get()
    qg = QuadrupleGen.get()
    #print(st.operands().top(), st.operators().top())
    if st.operators().top() in ['>=', '<=', '>', '<', '!=', '==']:
        operationsActions(st, qg)

def p_check_stack_exp(p):
    '''
    check_stack_exp :
    '''
    st = SymbolTable.get()
    qg = QuadrupleGen.get()
    if st.operators().top() == '+' or st.operators().top() == '-':
        operationsActions(st, qg)

def p_check_stack_term(p):
    '''
    check_stack_term :
    '''
    st = SymbolTable.get()
    qg = QuadrupleGen.get()
    if st.operators().top() == '*' or st.operators().top() == '/':
        operationsActions(st, qg)

def p_normal_assign(p):
    '''
    normal_assign :
    '''
    st = SymbolTable.get()
    qg = QuadrupleGen.get()
    normalAssignationActions(st, qg)

def p_assignation_var(p):
    '''
    assignation_var :
    '''
    st = SymbolTable.get()
    st.setCurrId(p[-1])
    #print("pushing:", st.current_id(), "as the var to assign")
    st.varToAssign().push(st.currentId())

def p_current_type_is_int(p):
    '''
    current_type_is_int :
    '''
    st = SymbolTable.get()
    st.setCurrType('int')
    st.setCurrId(p[-1])
    st.currentScope().addVar(st.currentId(), 'int', True)
    mem = Memory.get()
    mem.addConstant(st.currentId(), 'int')

def p_current_type_is_float(p):
    '''
    current_type_is_float :
    '''
    st = SymbolTable.get()
    st.setCurrType('float')
    st.setCurrId(p[-1])
    st.currentScope().addVar(st.currentId(), 'float', True)
    mem = Memory.get()
    mem.addConstant(st.currentId(), 'float')

def p_current_type_is_char(p):
    '''
    current_type_is_char :
    '''
    st = SymbolTable.get()
    st.setCurrType('char')
    st.setCurrId(p[-1])
    st.currentScope().addVar(st.currentId(), 'char', True)
    mem = Memory.get()
    mem.addConstant(st.currentId(), 'char')

def p_create_goto(p):
    '''create_goto : update_pending_jump'''
    qg = QuadrupleGen.get()
    createGotoQuadIf(qg)

def p_create_gotof(p):
    '''create_gotof : '''
    st = SymbolTable.get()
    qg = QuadrupleGen.get()
    createGotoFQuadIf(st, qg)

def p_update_pending_jump(p):
    '''update_pending_jump : '''
    qg = QuadrupleGen.get()
    updatePendingJumpIf(qg)

def p_update_pending_jump_1(p):
    '''update_pending_jump_1 : '''
    qg = QuadrupleGen.get()
    updatePendingJumpIf(qg)

def p_create_gotof_while(p):
    '''create_gotof_while : '''
    st = SymbolTable.get()
    qg = QuadrupleGen.get()
    createGotoFQuadWhile(st, qg)

def p_update_pending_jump_while(p):
    '''update_pending_jump_while : '''
    qg = QuadrupleGen.get()
    updatePendingJumpWhile(qg)

def p_read_quad(p):
    '''
    read_quad :
    '''
    qg = QuadrupleGen.get()
    qg.generateQuadruple('read', '', '', p[-1])
    
def p_print_quad(p):
    '''
    print_quad :
    '''
    writeVar = ''
    if type(p[-1]) == str:
        writeVar = p[-1]
    else:
        writeVar = flattenData(p[-1])
    qg = QuadrupleGen.get()
    qg.generateQuadruple('print', '', '', writeVar)

def p_set_return_stmt(p):
    '''
    set_return_stmt :
    '''
    st = SymbolTable.get()
    qg = QuadrupleGen.get()
    setReturn(st, qg)

def p_assign_func(p):
    '''
    assign_func :
    '''
    st = SymbolTable.get()
    qg = QuadrupleGen.get()
    functionAssignationActions(st, qg, p)

def p_save_call_operand(p):
    '''
    save_call_operand :
    '''
    st = SymbolTable.get()
    saveFuncCallOp(st)

def p_set_return_quad(p):
    '''
    set_return_quad :
    '''
    qg = QuadrupleGen.get()
    st = SymbolTable.get()
    funcId = p[-1]
    gosubJump = qg.generateQuadruple('GOSUB', '', '', funcId, False)
    qg.addPendingJump(gosubJump)
    st.resetCurrentParams() # To clear params
    # Saves function name in new params, pushes a false bottom then creates the ERA quadruple
    st.currentParams().append(funcId)
    #st.operators().push('(')
    qg.generateQuadruple('ERA', '', '', funcId)


def p_assign_gosub(p):
    '''
    assign_gosub :
    '''
    st = SymbolTable.get()
    qg = QuadrupleGen.get()
    gosubJump(st, qg)


def p_assign_params(p):
    '''
    assign_params :
    '''
    st = SymbolTable.get()
    qg = QuadrupleGen.get()
    # For functions without params
    try:
        st.operators().pop()
    except Exception:
        pass
    paramAssignQuads(st, qg)

def p_save_params(p):
    '''
    save_params :
    '''
    st = SymbolTable.get()
    st.currentParams().append((st.operands().pop(), st.opTypes().pop()))

def p_set_endfunc_quad(p):
    '''
    set_endfunc_quad :
    '''
    st = SymbolTable.get()
    qg = QuadrupleGen.get()
    returningQuad = qg.generateQuadruple('ENDFUNC', '', '', '')
    setReturnQuad(st.currentScopeName(), returningQuad)

def p_save_func(p):
    '''
    save_func :
    '''
    st = SymbolTable.get()
    qg = QuadrupleGen.get()
    st.saveFunc()
    saveFuncToDir(st.currentId(), len(qg.quadruples())+ 1)

def p_push_scope(p):
    '''
    push_scope :
    '''
    st = SymbolTable.get()
    st.pushNewScope()

def p_pop_scope(p):
    '''
    pop_scope :
    '''
    st = SymbolTable.get()
    st.popScope()



# Error rule for syntax errors
def p_error(p):
    if p:
        print(f"Syntax error at line {p.lineno}, column {p.lexpos}")
        exit(1)
    else:
        pass


# Build lexer and parser
lexer = lex.lex()
parser = yacc.yacc()

