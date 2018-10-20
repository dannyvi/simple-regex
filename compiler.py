"""compile a regex pattern to an nfa machine.

"""

import string

from parsing_table import (semantic, all_symbols, grammar,
                           generate_syntax_table)
from graph import Machine
from regex_nfa import induct_cat, induct_or, induct_star, basis


class Lexer:
    """parse a letter and return a lexeme."""

    def __init__(self, letter):
        self.value = letter
        if letter in "()|*":
            self.type = letter
        elif letter == "$":
            self.type = '$'
        elif letter in string.ascii_letters + \
                string.digits + string.punctuation:
            self.type = 'a'

class RegexCompiler:
    """Regex compiler reads a regex pattern, and return an nfa Machine of graph.


    """

    def __init__(self):
        self.syntax_table = generate_syntax_table()
        # self.current_state = 0
        self.state_stack = [0]
        self.arg_stack = []
        self.machin_lit = ""

    def parse(self, stream):
        stream = stream + '$'
        for i in stream:
            lexeme = Lexer(i)
            self.ahead(lexeme.type, lexeme.value)

    def get_action(self, state, literal):
        return self.syntax_table[state][all_symbols.index(literal)]

    def ahead(self, literal, value=None):
        action = self.get_action(self.state_stack[-1], literal)
        if action[0] == 's':  # shift action
            self.state_stack.append(int(action[1:]))
            # self.current_state = int(action[1:])
            if literal == 'a':
                self.arg_stack.append(value)
        elif action[0] == '$':
            machine_literal = self.arg_stack.pop()
            self.machin_lit = machine_literal
            # success
        elif action[0] == 'r':
            number = int(action[1:])
            production = grammar[number]
            head = production[0]
            body = production[1]
            for _ in body:
                self.state_stack.pop()
            state = self.get_action(self.state_stack[-1], head)
            self.state_stack.append(int(state))
            if number == 2 or number == 3:
                i2 = self.arg_stack.pop()
                i1 = self.arg_stack.pop()
                translation = semantic[number].format(i1, i2)
                self.arg_stack.append(translation)
            else:
                i = self.arg_stack.pop()
                translation = semantic[number].format(i)
                self.arg_stack.append(translation)
            self.ahead(literal, value)



if __name__ == "__main__":
    a = RegexCompiler()
    a.parse("abc*d(e|f)k")
    print(a.machin_lit)
    m = eval(a.machin_lit)
    m.sort_state_names()
    m.show()