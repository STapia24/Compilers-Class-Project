import ply.yacc as yacc
import ply.lex as lex

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
#    "COLON",
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
    ('nonassoc', 'EQ', 'NEQ', 'LE', 'GE', 'LT', 'GT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),
)


# program
def p_program(p):
    """program : PROGRAM ID SEMICOLON var_dec func_dec main"""
    p[0] = 1
    print("Got to program")

    # main
def p_main(p):
    """main : MAIN LP RP block SEMICOLON"""
    print("Got into main")

# block
def p_block(p):
    """block : LBR statute statute1 RBR """
    print("Found a block")

# func_dec
def p_func_dec(p):
    """func_dec : FUNC return_type ID LP param_opt RP func_block func_dec
    | empty"""
    print("Function declared")

# param_opt
def p_param_opt(p):
    """param_opt : type_simple ID more_param_opt
    | empty"""
    print("Got to param_opt")

# more_param_opt
def p_more_param_opt(p):
    """more_param_opt : COMMA type_simple ID more_param_opt
    | empty"""
    print("Got to more_param_opt")

# var_dec
def p_var_dec(p):
    """ var_dec : type_simple ID dim SEMICOLON var_dec
    | type_complex ID complex_dec SEMICOLON
    | empty
    """
    print("Declared a variable")

# complex_dec
def p_complex_dec(p):
    """
    complex_dec : COMMA ID complex_dec
    | empty
    """
    print("Declared another complex type")

# dim
def p_dim(p):
    """dim : LSB CONST_INT RSB
    | LSB CONST_INT RSB LSB CONST_INT RSB
    | empty"""
    print("Dimensions while declaring variable")

# return_type
def p_return_type(p):
    """return_type : type_simple
    | VOID"""
    print("Returning a simple type or void")

# type_simple
def p_type_simple(p):
    """type_simple : INT
    | FLOAT
    | CHAR"""
    print("Found a simple type")

# type_complex
def p_type_complex(p):
    """type_complex : DATAFRAME"""
    print("Found a dataframe")

# assignation
def p_assignation(p):
    """assignation : var exp_dim_opt ASSIGN exp_or_func_assignation"""
    print("Assignation")

# exp_or_func_assignation
def p_exp_or_func_assignation(p):
    """exp_or_func_assignation : expression_assignation
    | func_call"""
    print("Assignation of exp or function call")

# expression_assignation
def p_expression_assignation(p):
    """expression_assignation : exp SEMICOLON"""
    print("Assignation of exp")

# var
def p_var(p):
    """var : ID exp_dim_opt"""
    print("Variable use")

# exp_dim_opt
def p_exp_dim_opt(p):
    """exp_dim_opt : LSB exp RSB
    | LSB exp RSB LSB exp RSB
    | empty"""
    print("Dimensions when using variable")

# if_statement
def p_if_statement(p):
    """if_statement : IF LP exp RP block else"""
    print("If statement")

# else
def p_else(p):
    """else : ELSE block
    | empty"""
    print("Else statement")

# while_statement
def p_while_statement(p):
    """while_statement : WHILE LP exp RP block"""
    print("While statement")

# read statement
def p_read(p):
    """read : READ LP var RP SEMICOLON"""
    print("Read something")

# print statement
def p_print(p):
    """print : PRINT LP opt_string RP SEMICOLON
    | PRINT LP exp RP SEMICOLON"""
    print("Prints something")

# constants
def p_constants(p):
    """constants : CONST_INT
    | CONST_FLOAT
    | CONST_CHAR"""
    print("This are constants")

# func_call
def p_func_call(p):
    """func_call : ID LP opt_args RP SEMICOLON"""
    print("Function called")

# opt_args
def p_opt_args(p):
    """opt_args : exp exp_args_more
    | empty"""
    print("Arguments for a function call")

# exp_args_more
def p_exp_args_more(p):
    """exp_args_more : COMMA exp exp_args_more
    | empty"""
    print("More arguments for a function call")

# statements
def p_statements(p):
    """statements : assignation
    | if_statement
    | while_statement
    | read
    | func_call
    | return
    | print
    | data_funcs"""
    print("Called a statement")

def p_data_funcs(p):
    """data_funcs : mean
    | median
    | mode
    | std
    | variance
    | hist
    | plot
    | sctplot"""
    print("Found a data function")


def p_opt_string(p):
    """opt_string : CONST_STRING"""
    print("String found")    

#statute1
def p_statute1(p):
    """statute1 : statute statute1
    | empty"""
    print("Jumped to statute1")

#statute
def p_statute(p):
    """statute : statements statute1
    | empty"""
    print("Found a statute")

# func_block
def p_func_block(p):
    """ func_block : LBR var_dec statute RBR """
    print("A func_block")

# return
def p_return(p):
    """ return : RETURN LP exp RP SEMICOLON """
    print("Returns something")

# exp
def p_exp(p):
    """ exp : or_exp OR or_exp
    | or_exp
    """
    print("Found an exp")

def p_or_exp(p):
    """ or_exp : and_exp AND and_exp
    | and_exp
    """
    print("Found an or_exp")

def p_and_exp(p):
    """ and_exp : op_exp EQ op_exp
    | op_exp GE op_exp
    | op_exp LE op_exp
    | op_exp GT op_exp
    | op_exp LT op_exp
    | op_exp NEQ op_exp
    | op_exp
    """
    print("Found an and_exp")

def p_op_exp(p):
    """ op_exp : term PLUS term
    | term MINUS term
    | term
    """
    print("Found an op_exp")

def p_term(p):
    """term : factor MULT factor
    | factor DIV factor
    | factor
    """
    print("Found a term")

def p_factor(p):
    """factor : LP exp RP
    | constants
    | var
    | func_call
    """
    print("Found a factor")

def p_mean(p):
    """ mean : MEAN LP complex_var RP SEMICOLON """
    # Code to handle the mean calculation
    print("Mean")

def p_mode(p):
    """ mode : MODE LP complex_var RP SEMICOLON """
    # Code to handle the mode calculation
    print("Mode")

def p_median(p):
    """ median : MEDIAN LP complex_var RP SEMICOLON """
    # Code to handle the median calculation
    print("Median")

def p_std(p):
    """ std : STD LP complex_var RP SEMICOLON """
    # Code to handle the standard deviation calculation
    print("Standar Deviation")

def p_variance(p):
    """ variance : VARIANCE LP complex_var RP SEMICOLON """
    # Code to handle the variance calculation
    print("Variance")

def p_hist(p):
    """ hist : HIST LP complex_var RP SEMICOLON """
    # Code to handle the histogram generation
    print("Histogram")

def p_plot(p):
    """ plot : PLOT LP complex_var RP SEMICOLON """
    # Code to handle the plot generation
    print("Plot")

def p_sctplot(p):
    """ sctplot : SCTPLOT LP complex_var RP SEMICOLON """
    # Code to handle the scatter plot generation
    print("Scatterplot")

# Complex variable use
def p_complex_var(p):
    """ complex_var : ID
    | ID PERIOD"""
    # Code to handle complex variable reference
    print("Complex var use")

# epsilon
def p_empty(p):
    """ empty : """
    pass
    print("Got to an empty production")

# Error rule for syntax errors
def p_error(p):
    print("FAIL")
    if p:
        print(f"Syntax error at line {p.lineno}, column {p.lexpos}")
    else:
        print("Syntax error: Unexpected end of file")


# Build lexer
lexer = lex.lex()

# Build the parser
parser = yacc.yacc()


def parse_input_file(filename):
    with open(filename, 'r') as file:
        input_code = file.read()

    # Lex and parse the input code
    lexer.input(input_code)
#    for token in lexer:
#        print(token)

    result = parser.parse(input_code, lexer=lexer)
    if result:
        print("Parsing completed succesfully!")
    else:
        print("Parsing failed")
    print(result)


parse_input_file('input.txt')

