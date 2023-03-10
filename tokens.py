from enum import Enum
import re
from collections import namedtuple

TokenInfo = namedtuple("Tokens", ["name", "value"])


class NewEnum(Enum):

    def __eq__(self, b) -> bool:
        if isinstance(b, str):
            return self.name == b
        else:
            return self.name == b.name

    def __hash__(self):
        return id(self.name)


ILLEGAL = 'ILLEGAL'
EOF = 'EOF'


class Token(NewEnum):
    # data types
    STRING = re.compile(r'(".*")')
    FLOAT = re.compile(r'\d+\.\d+')
    INT = re.compile(r'\d+')
    # brackets
    LPAREN = re.compile(r'\(')
    RPAREN = re.compile(r'\)')
    LBRACE = re.compile(r'\{')
    RBRACE = re.compile(r'\}')
    LSQUARE = re.compile(r'\[')
    RSQUARE = re.compile(r'\]')
    # oeprators
    EQUAL = re.compile(r'\=\=')
    ASSIGN = re.compile(r'\=')
    # athemetic operators
    PLUS = re.compile(r'\+')
    MINUS = re.compile(r'\-')
    TIMES = re.compile(r'\*')
    DIVIDE = re.compile(r'/')
    MODULUS = re.compile(r'%')
    POWER = re.compile(r'\^')
    # logical operators
    AND = re.compile(r'&&')
    OR = re.compile(r'\|\|')
    NOT = re.compile(r'!')
    # conditional operators
    SMALL = re.compile(r'<')
    SMALLEQ = re.compile(r'<\=')
    LARGE = re.compile(r'>')
    LARGEEQ = re.compile(r'>\=')
    NOTEQ = re.compile(r'!\=')
    # keywords
    IF = re.compile(r'if')
    FOR = re.compile(r'for')
    WHILE = re.compile(r'while')
    DO = re.compile(r'do')
    TRUE = re.compile(r'true')
    FALSE = re.compile(r'false')
    FUNC = re.compile(r'func')
    ELSE = re.compile(r'else')
    NAN = re.compile(r'nan')
    LET = re.compile(r'let')
    READ = re.compile(r'read')
    PRINT = re.compile(r'print')
    LINE = re.compile(r'line')
    RETURN = re.compile(r'return')
    # variables
    ID = re.compile(r'[_a-zA-Z][_a-zA-Z0-9]*')
    # comments
    COMMENT = re.compile(r'#.*')
    # delimier
    COMMA = re.compile(r',')
    SEMICOLON = re.compile(r';')
    WHITESPACE = re.compile(r'(\t|\n|\s|\r)+')


Priority = NewEnum("priority", [
    "LOWEST",
    "LOWER",
    "LOW",
    "HIGH",
    "HIGHER",
    "HIGHEST",
])

precedence = {
    Token.EQUAL.name: Priority.LOWER,  # ==
    Token.NOTEQ.name: Priority.LOWER,  # !=
    Token.SMALL.name: Priority.LOW,  # <
    Token.LARGE.name: Priority.LOW,  # >
    Token.PLUS.name: Priority.HIGH,  # +
    Token.MINUS.name: Priority.HIGH,  # -
    Token.TIMES.name: Priority.HIGHER,  # *
    Token.DIVIDE.name: Priority.HIGHER,  # /
    Token.LPAREN.name: Priority.HIGHEST,  # ()
}


def get_precedence(token: Token) -> Priority:
    return precedence.get(token.name, Priority.LOWEST)
