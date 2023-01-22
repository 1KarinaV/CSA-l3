class Node:  ...


class Statement(Node): ...


class Expression(Node): ...


storage = {}

from tokens import *


class Literal(Expression):
    def __init__(self, type: str, value: str):
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        return str(self.value)

    def get_type(self) -> str:
        # returns data type
        if self.type == Token.FALSE or self.type == Token.TRUE:
            return "bool"
        return self.type.lower()

    def type_casting(self):
        # conversion for the value to actual value
        if self.type == Token.INT:
            return int(self.value)
        elif self.type == Token.FLOAT:
            return float(self.value)
        elif self.type == Token.STRING:
            return str(self.value)
        elif self.type == Token.TRUE:
            return True
        elif self.type == Token.FALSE:
            return False
        else:
            return None

    def eval(self):
        try:
            out = self.type_casting()
        except ValueError:
            raise ValueError(f"Error converting {self.value} to {self.type}")
        return out


class LetStatement(Statement):
    def __init__(self, name: str, expr: Expression):
        self.name = name
        self.expr = expr

    def __repr__(self) -> str:
        return f"(set {self.name} {self.expr})"

    def eval(self):
        storage[self.name] = self.expr.eval()


class AssignStatement(Statement):
    def __init__(self, name: str, expr: Expression):
        self.name = name
        self.expr = expr

    def __repr__(self) -> str:
        return f"(set {self.name} {self.expr})"

    def eval(self):
        if self.name not in storage:
            raise NameError(f'"{self.name}" not defined')
        storage[self.name] = self.expr.eval()


class Identifier(Expression):
    def __init__(self, name):
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def eval(self):
        if self.name in storage:
            return storage[self.name]
        else:
            raise NameError(f"'{self.name}' is not defined")


class BlockStatement(Statement):
    def __init__(self, statements: list[Statement]):
        self.statements = statements

    def __repr__(self) -> str:
        data = ""
        for x in self.statements:
            data += x.__repr__()
        return f"({data})"

    def eval(self):
        for x in self.statements:
            data = x.eval()


class IfStatement(Statement):
    def __init__(self, condition, true_stmt: Statement, false_stmt: Statement):
        self.condition = condition
        self.true_stmt = true_stmt
        self.false_stmt = false_stmt

    def __repr__(self) -> str:
        return f"(if ({self.condition}) ({self.true_stmt}) ({self.false_stmt}))"

    def eval(self):
        if self.condition.eval():
            self.true_stmt.eval()
        else:
            self.false_stmt.eval()


class WhileStatement(Statement):
    def __init__(self, condition: Expression, stmt: Statement):
        self.condition = condition
        self.stmt = stmt

    def __repr__(self) -> str:
        return f"(while ({self.condition}) ({self.stmt}))"

    def eval(self):
        while self.condition.eval():
            self.stmt.eval()


class ForStatement(Statement):
    def __init__(self, condition, step_expression, condition2: Expression, stmt: Statement):
        self.stmt = stmt
        self.condition = condition
        self.condition2 = condition2
        self.step_expression = step_expression

    def __repr__(self) -> str:
        return f"(for {self.step_expression}, {self.condition}, {self.condition2}, {self.stmt})"

    def eval(self):
        for self.step_expression in self.condition.eval(), self.condition2.eval():
            self.stmt.eval()


class DoWhileStatement(Statement):
    def __init__(self, condition: Expression, stmt: BlockStatement):
        self.condition = condition
        self.stmt = stmt

    def __repr__(self) -> str:
        return f"(do  {self.stmt} while {self.condition})"

    def eval(self):
        while 1:
            self.stmt.eval()
            if not self.condition.eval():
                break


class InfixExpression(Expression):
    def __init__(self, left: Expression, operator: Statement, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self) -> str:
        return f"({self.left} {self.operator} {self.right})"

    def eval(self):
        operator = {
            "%": lambda a, b: a % b,
            "^": lambda a, b: a ** b,
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a // b,
            "&": lambda a, b: a and b,
            "|": lambda a, b: a or b,
            "==": lambda a, b: a == b,
            # conditional operations
            "<": lambda a, b: a < b,
            ">": lambda a, b: a > b,
            "<=": lambda a, b: a <= b,
            ">=": lambda a, b: a >= b,
        }
        try:
            return operator[self.operator](self.left.eval(), self.right.eval())
        except TypeError:
            raise TypeError(f"can't perform {self.operator} between {self.left_type()} and  {self.left_type()}")


class PrefixExpression(Expression):
    def __init__(self, operator: Statement, right: Expression):
        self.operator = operator
        self.right = right

    def get_type(self) -> str:
        # returns data type
        return self.type.right

    def __repr__(self) -> str:
        return f"({self.operator}{self.right})"

    def eval(self):
        operator = {
            "!": lambda a: not a,
            "-": lambda a: -a,
        }
        try:
            return operator[self.operator](self.right.eval())
        except TypeError:
            raise TypeError(f"can't perform {self.operator} between {self.left_type()} and  {self.left_type()}")


class PrintStatement(Statement):
    def __init__(self, state, value: Expression):
        self.state = state
        self.value = value

    def __repr__(self) -> str:
        return f"(print {self.value})"

    def eval(self):
        if self.state == "println":
            print(self.value.eval())
        else:
            print(self.value.eval(), end="")
