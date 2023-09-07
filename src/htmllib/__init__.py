"""
=======
HTMLLIB
=======

A module that turns a stream of HTML code into a python representation of it.
"""


from sys import version_info


assert (version_info.major, version_info.minor) >= (3, 8), f"To import ``{__package__}``, use Python 3.8 or above."


__author__ = "boddz"
__version__ = "1.0.0"
__license__ = "GNU GPLv3"


from .lexer import (
    Lexer,
    TokenTypes,
    pretty_print_tokens
)

from .parser import (
    Parser,
    HTMLDoctypeOrCommNode,
    HTMLOpeningTagNode,
    HTMLClosingTagNode,
    HTMLSelfClosingTagNode,
    HTMLErrorNode,
    NonValidTagIDError,
    NeverEndedTagError
)
