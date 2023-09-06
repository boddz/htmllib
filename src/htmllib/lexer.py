#!/usr/bin/env python

"""
==============
The HTML Lexer
==============

Internal module used to generate a list of verbose tokens to be handed to the parser module at a later point.
"""

from __future__ import annotations

from enum import Enum, auto
from dataclasses import dataclass


class UnkownLexemeError(Exception): ...


class TokenTypes(Enum):
    ANGLE_BRACKET_L = auto()
    ANGLE_BRACKET_R = auto()
    EXCLAMATION = auto()
    CLOSING_SLASH = auto()
    ID = auto()
    CONTENT = auto()
    ASSIGNMENT = auto()
    QUOTE = auto()
    ERROR = auto()
    EOF = auto()


@dataclass
class Cursor:
    index: int
    line: int
    col: int

    def increment(self, chars: int=1) -> None:
        self.col += chars

    def new_line(self, lines :int=1) -> None:
        self.line += lines
        self.col = 1


@dataclass
class Token:
    """
    Represents a tokenized piece of code. To be only generated from the lex process.
    """
    type: TokenTypes
    value: str
    cursor: Cursor
    extra: str = None  # Extra content, e.g. doctype and comments.


class Lexer:
    """
    Represents the lex process/ states.

    Usage ::

        # Open a file and read contents, or just dump HTML data into a variable directly.
        with open("simple_tag.html", "r") as file_obj:
            code = file_obj.read()

        lexer = Lexer(code)
        tokens = lexer.lex()

        # Optional, this just prints out all of the generated tokens in a pretty looking way.
        pretty_print_tokens(tokens)

    ----
    Note
    ----

    * This class will only generate tokens with values and positions in the file/ stream. The generated tokens have no
    error checking and are intended to be passed to a seperate parser module for validation checks/ code and data
    generation.

    * Index may not appear accurate when compared to text editors, but it is for the sake of list indexing the HTML.

    """
    def __init__(self, stream: str) -> None:
        self.__stream_raw = stream
        self.__stream_proc = list(stream)
        self.__cursor = Cursor(None, 1, 1)  # For index, use the lexer's index at a later stage in lex.
        self.__index = 0
        self.__tokens = list()
        self.__inside_angle_bracket = False

    @property
    def stream_raw(self) -> str:
        return self.__stream_raw

    @property
    def stream(self) -> list:
        return self.__stream_proc

    @property
    def cursor(self) -> Cursor:
        return self.__cursor

    @property
    def index(self) -> int:
        return self.__index

    @property
    def tokens(self) -> list:
        """
        A list to store the tokens generated by :meth:`lex`.
        """
        return self.__tokens

    def __index_up(self) -> int:
        """
        **For internal use only**

        Return current index for the Lexer object & increment it's value.
        """
        current = self.__index
        self.__index += 1
        return current

    def __index_down(self) -> int:
        """
        **For internal use only**

        Return the current index for the Lexer object & decrement it's value.
        """
        current = self.__index
        self.__index -= 1
        return current

    def get_char(self, index: int) -> char:
        """
        Returns the character at the specified index.
        """
        return self.stream[index]

    def __eat_id(self, until: list=[" ", ">", "=", "<", "/"]) -> None:
        """
        **For internal use only**

        Eat chars and return them as a string whilst incrementing the lexers main index.

        :param until: The character to stop at
        :type until: str, optional

        :return: ``identifier``, the string that was produced from consuming the valid lexemes
        :rtype: str
        """
        identifier = str()
        char = self.get_char(self.index - 1)
        while char not in until and self.index < len(self.stream):  # Check index avoid out of range.
            identifier += char
            if char == "\n": self.cursor.new_line()
            else: self.cursor.increment()
            char = self.get_char(self.__index_up())
        if char in until: self.__index_down()
        if self.index == len(self.stream): identifier += char  # Avoid out of index but add char if it is at EOF.
        return identifier

    def __eat_quotes(self, *, which: str="\"") -> None:
        """        
        **For internal use only**

        Eats quoted strings.

        :return: ``quoted``, the string that was produced from eating the chars inside of quotes
        :rtype: str
        """
        quoted = str()
        char = self.get_char(self.__index_up())  # Char past the first `"`, the start of quoted str.
        while char not in [which, "\n"] and self.index < len(self.stream):
            quoted += char
            self.cursor.increment()
            char = self.get_char(self.__index_up())
        if char == which:
            self.cursor.increment()
        if self.index == len(self.stream): quoted += char  # Avoid out of index but add char if it is at EOF.
        return quoted

    def snapshot_cursor(self, cursor: Cursor) -> Cursor:
        """
        Snapshot a cursor at it's current position. Useful for the :meth:``self.lex``.
        """
        return Cursor(cursor.index, cursor.line, cursor.col)

    def lex(self, *, debug: bool=False) -> list(Token):
        """
        Generates tokens from :attr:``self.stream`` to be appended to :attr:``self.tokens``.

        :param debug: Do not raise, just print errors
        :type debug: bool, optional

        :raises UnkownLexemeError: whenever a non-supported lexeme is found

        :return: :attr:``self.tokens``
        :rtype: list
        """
        while self.index < len(self.stream):
            # Only increment the index when it is less than the stream len to avoid out of index error for stream list.
            char = self.get_char(self.__index_up()) if self.index < len(self.stream) else self.get_char(self.index)
            self.cursor.index = self.index - 1  # At every run of lex, set the lexer's cursor index to match the lexer.
            cursor = self.snapshot_cursor(self.cursor)

            # This first if is to avoid including content in a tag as the IDs inside the angled brackets of a tag for -
            # example: '<html lang="en">' would have ``html``, ``lang`` and ``en`` tokenized as IDs whereas
            # '<title>Document</title>' would only have ``title`` (in both the opening and closing tag interior) tokenized
            # as IDs and will ignore the text ``Document`` which is inside the body of the tag.
            #
            # This check works by making sure that the current lexeme is not in the tag body but the tag interior, but at
            # the same time still running cases for "<", ">" and "\n" to avoid breaking the lex process incase one is found
            # in the tag's body.
            # 
            # TL;DR: ignore content in tag body, only tokenize IDs in the tag's interior (tag params).
            if char not in ["<", ">", "\n"] and self.__inside_angle_bracket is False: self.cursor.increment()
            elif char == " ": self.cursor.increment()
            elif char == "\t": self.cursor.increment()
            elif char == "\n": self.cursor.new_line()
            elif char == "<":
                self.__inside_angle_bracket = True
                self.tokens.append(Token(TokenTypes.ANGLE_BRACKET_L, "<", cursor))
                self.cursor.increment()
            elif char == ">":
                self.__inside_angle_bracket = False
                self.tokens.append(Token(TokenTypes.ANGLE_BRACKET_R, ">", cursor))
                self.cursor.increment()
            elif char == "!":  # Catches doctype stuff and comments and stores them in token extra param for later.
                self.cursor.increment()
                self.__index_up()
                extra = self.__eat_id([">"])
                self.tokens.append(Token(TokenTypes.EXCLAMATION, "!", cursor, extra))
            elif char == "/":
                self.tokens.append(Token(TokenTypes.CLOSING_SLASH, "/", cursor))
                self.cursor.increment()
            elif char == "=":
                self.tokens.append(Token(TokenTypes.ASSIGNMENT, "=", cursor))
                self.cursor.increment()
            elif char == "\"":
                self.cursor.increment()
                quoted = self.__eat_quotes()
                self.tokens.append(Token(TokenTypes.QUOTE, quoted, cursor))
            elif char == "'":
                self.cursor.increment()
                quoted = self.__eat_quotes(which="'")
                self.tokens.append(Token(TokenTypes.QUOTE, quoted, cursor))
            elif ord(char) >= ord('A') and ord(char) <= ord('Z') or \
                ord(char) >= ord('a') and ord(char) <= ord('z') or \
                ord(char) >= ord("0") and ord(char) <= ord("9"):  # All identifiers [aA-zZ, 0-9].
                identifier = self.__eat_id()
                self.tokens.append(Token(TokenTypes.ID, identifier, cursor))
            else: self.cursor.increment()

        self.tokens.append(Token(TokenTypes.EOF, "EOF", None))
        return self.tokens


def pretty_print_tokens(tokens: list, *, index=None) -> None:
    """
    Pretty print a generated list of tokens.

    :param tokens: The list of tokens to pretty print
    :type tokens: list

    :param index: The index of a specific token to pretty print, defaults to None
    :type index: int, optional

    :raises TypeError: Raised if a list is not given as ``tokens`` param
    """
    if type(tokens) != list: raise TypeError("Param ``tokens`` must be of type ``list``")
    for i, token in enumerate(tokens):
        if index is not None: i = index
        print(
            f"({i}) --->\t------\n\t\t"                                                                               \
                         f"Type   = {token.type}\n\t\t"                                                               \
                         f"Value  = \"{token.value.strip(chr(10))}\"\n\t\t"                                           \
                         f"Cursor = {token.cursor}\n\t\t"                                                             \
                         f"Extra  = \"{token.extra}\"\n\t\t"                                                          \
                       "------"
        )
        if index is not None: break


if __name__ == "__main__":
    with open("tests/data/basic.html", "r") as file_obj:
        code = file_obj.read()

    lexer = Lexer(code)
    tokens = lexer.lex()

    pretty_print_tokens(tokens)
