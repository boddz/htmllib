"""
=======
HTMLLIB
=======

A module that turns a stream of HTML code into a python representation of it.
"""


from .lexer import Lexer, TokenTypes, pretty_print_tokens
from .parser import Parser
