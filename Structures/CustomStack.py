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
        st.operandsStacks().push(st.operands())
        st.setOperands(Stack())

        st.typesStacks().push(st.opTypes())
        st.setTypes(Stack())

        st.operatorsStacks().push(st.operators())
        st.setOperators(Stack())
    else:
        st.operators().push(op)


def popOp(st, op):
    # Handling of false bottom, if closing parenthesis, then retrieve the top of the
    # stacks stack to reestablish the previous state
    if op == ')':
        try:
            prevOperands = st.operandsStacks().pop()
            st.setOperands(prevOperands)
        except:
            st.setOperands(Stack())

        try:
            prevTypes = st.typesStacks().pop()
            st.setTypes(prevTypes)
        except:
            st.setTypes(Stack())

        try:
            prevOperators = st.operatorsStacks().pop()
            st.setOperators(prevOperators)
        except:
            st.setOperators(Stack())
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