def valid(self):
    if len(self.stack()) <= 0:
        raise Exception('Stack is empty.')
    return True


def isEmpty(self):
    if len(self.stack()) == 0:
        return True
    return False

#
def pushOp(st, op):
    # Handling of false bottom, if opening parenthesis, then save current state of stacks
    # in a stack of stacks, to retrieve it 
    if op == '(':
        st.operands_stacks().push(st.operands())
        st.set_operands(Stack())

        st.types_stacks().push(st.op_types())
        st.set_types(Stack())

        st.operators_stacks().push(st.operators())
        st.set_operators(Stack())
    else:
        st.operators().push(op)


def popOp(st, op):
    # Handling of false bottom, if closing parenthesis, then retrieve the top of the
    # stacks stack to reestablish the previous state
    if op == ')':
        try:
            prev_operands = st.operands_stacks().pop()
            st.set_operands(prev_operands)
        except:
            st.set_operands(Stack())

        try:
            prev_types = st.types_stacks().pop()
            st.set_types(prev_types)
        except:
            st.set_types(Stack())

        try:
            prev_operators = st.operators_stacks().pop()
            st.set_operators(prev_operators)
        except:
            st.set_operators(Stack())
    else:
        st.operators().pop()


class Stack:

    def get_second(self):
        return self.__stack[-2]

    def __init__(self):
        self.__stack = []

    def stack(self):
        return self.__stack

    def push(self, val):
        self.__stack.append(val)

    def pop(self):
        if valid(self):
            element = self.__stack.pop()
            return element

    def top(self):
        if isEmpty(self):
            return None
        return self.__stack[-1]