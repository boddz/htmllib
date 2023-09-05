#!/usr/bin/env python


"""
=====================
HTMLLIB Lexer Testing
=====================

Unit tests for the ``Lexer`` class in htmlib.lexer module.
"""


from __future__ import annotations

from src import htmllib

from unittest import TestCase


class TestLexerMethods(TestCase):
    def setUp(self) -> None:
        self.lexer_open_tag = htmllib.Lexer("<html>").lex()
        self.lexer_close_tag = htmllib.Lexer("</html>").lex()
        self.lexer_open_and_close_tag = htmllib.Lexer("<p> This content will be ignored </p>").lex()
        self.lexer_attrs_tag = htmllib.Lexer("<p id='123' class='abcdef'>").lex()
        self.lexer_attrs_self_closing = htmllib.Lexer('<img src="null" alt="There is no image"/>').lex()
        self.lexer_ignore_invalid_lexeme = htmllib.Lexer("<p @ id=\\'invalid'>").lex()  # Invalids are ignored.
        self.lexer_cursors_pos = htmllib.Lexer(
            """<!--
                Just some simple HTML code to in the lexer tests.
            -->

            <!DOCTYPE html>

            <html>
                <head>
                    <title> I am just content between tags and thus will be ignored by the lexer :( </title>
                <head>
                <body>
                    <h1 id="h1-id123">
                    <img src = "null"   alt="No image provided" >
                <body>
            <html>
            """  # This was cross-referenced using a file instead, to make sure values are accurate for tests.
        )
        self.lexed_cursors_pos = self.lexer_cursors_pos.lex()

    #region (token values)

    def test_lexer_open_tag(self) -> None:
        self.assertEqual(self.lexer_open_tag[0].value, "<")
        self.assertEqual(self.lexer_open_tag[1].value, "html")
        self.assertEqual(self.lexer_open_tag[2].value, ">")
        self.assertEqual(self.lexer_open_tag[3].value, "EOF")

    def test_lexer_close_tag(self) -> None:
        self.assertEqual(self.lexer_close_tag[0].value, "<")
        self.assertEqual(self.lexer_close_tag[1].value, "/")
        self.assertEqual(self.lexer_close_tag[2].value, "html")
        self.assertEqual(self.lexer_close_tag[3].value, ">")
        self.assertEqual(self.lexer_close_tag[4].value, "EOF")

    def test_lexer_open_and_close_tag(self) -> None:
        self.assertEqual(self.lexer_open_and_close_tag[0].value, "<")
        self.assertEqual(self.lexer_open_and_close_tag[1].value, "p")
        self.assertEqual(self.lexer_open_and_close_tag[2].value, ">")
        self.assertEqual(self.lexer_open_and_close_tag[3].value, "<")
        self.assertEqual(self.lexer_open_and_close_tag[4].value, "/")
        self.assertEqual(self.lexer_open_and_close_tag[5].value, "p")
        self.assertEqual(self.lexer_open_and_close_tag[6].value, ">")
        self.assertEqual(self.lexer_open_and_close_tag[7].value, "EOF")

    def test_lexer_attrs_tag(self) -> None:
        self.assertEqual(self.lexer_attrs_tag[0].value, "<")
        self.assertEqual(self.lexer_attrs_tag[1].value, "p")
        self.assertEqual(self.lexer_attrs_tag[2].value, "id")
        self.assertEqual(self.lexer_attrs_tag[3].value, "=")
        self.assertEqual(self.lexer_attrs_tag[4].value, "123")
        self.assertEqual(self.lexer_attrs_tag[5].value, "class")
        self.assertEqual(self.lexer_attrs_tag[6].value, "=")
        self.assertEqual(self.lexer_attrs_tag[7].value, "abcdef")
        self.assertEqual(self.lexer_attrs_tag[8].value, ">")
        self.assertEqual(self.lexer_attrs_tag[9].value, "EOF")

    def test_lexer_attrs_self_closing(self) -> None:
        self.assertEqual(self.lexer_attrs_self_closing[0].value, "<")
        self.assertEqual(self.lexer_attrs_self_closing[1].value, "img")
        self.assertEqual(self.lexer_attrs_self_closing[2].value, "src")
        self.assertEqual(self.lexer_attrs_self_closing[3].value, "=")
        self.assertEqual(self.lexer_attrs_self_closing[4].value, "null")
        self.assertEqual(self.lexer_attrs_self_closing[5].value, "alt")
        self.assertEqual(self.lexer_attrs_self_closing[6].value, "=")
        self.assertEqual(self.lexer_attrs_self_closing[7].value, "There is no image")
        self.assertEqual(self.lexer_attrs_self_closing[8].value, "/")
        self.assertEqual(self.lexer_attrs_self_closing[9].value, ">")
        self.assertEqual(self.lexer_attrs_self_closing[10].value, "EOF")

    def test_lexer_ignore_invalid_lexeme(self) -> None:
        self.assertEqual(self.lexer_ignore_invalid_lexeme[0].value, "<")
        self.assertEqual(self.lexer_ignore_invalid_lexeme[1].value, "p")
        self.assertEqual(self.lexer_ignore_invalid_lexeme[2].value, "id")
        self.assertEqual(self.lexer_ignore_invalid_lexeme[3].value, "=")
        self.assertEqual(self.lexer_ignore_invalid_lexeme[4].value, "invalid")
        self.assertEqual(self.lexer_ignore_invalid_lexeme[5].value, ">")
        self.assertEqual(self.lexer_ignore_invalid_lexeme[6].value, "EOF")

    #endregion (token values)

    #region (token types)

    def test_breifly_token_type_enums(self) -> None:
        """
        This is not as important, full coverage not needed here really.
        """
        self.assertEqual(self.lexer_attrs_self_closing[0].type, htmllib.TokenTypes.ANGLE_BRACKET_L)
        self.assertEqual(self.lexer_attrs_self_closing[1].type, htmllib.TokenTypes.ID)
        self.assertEqual(self.lexer_attrs_self_closing[2].type, htmllib.TokenTypes.ID)
        self.assertEqual(self.lexer_attrs_self_closing[3].type, htmllib.TokenTypes.ASSIGNMENT)
        self.assertEqual(self.lexer_attrs_self_closing[4].type, htmllib.TokenTypes.QUOTE)
        self.assertEqual(self.lexer_attrs_self_closing[5].type, htmllib.TokenTypes.ID)
        self.assertEqual(self.lexer_attrs_self_closing[6].type, htmllib.TokenTypes.ASSIGNMENT)
        self.assertEqual(self.lexer_attrs_self_closing[7].type, htmllib.TokenTypes.QUOTE)
        self.assertEqual(self.lexer_attrs_self_closing[8].type, htmllib.TokenTypes.CLOSING_SLASH)
        self.assertEqual(self.lexer_attrs_self_closing[9].type, htmllib.TokenTypes.ANGLE_BRACKET_R)

    #endregion (token types)

    #region (token cursror positions)

    def test_cursors_pos(self) -> None:
        """
        A few random checks to determine if cursor positioning is correct using cursor positions in a slice.
        """
        stream = self.lexer_cursors_pos.stream_raw
        first_slice = stream[self.lexed_cursors_pos[1].cursor.index + 1 : self.lexed_cursors_pos[2].cursor.index]
        second_slice = stream[self.lexed_cursors_pos[4].cursor.index + 1 : self.lexed_cursors_pos[5].cursor.index]
        third_slice = stream[self.lexed_cursors_pos[9].cursor.index + 1 : self.lexed_cursors_pos[11].cursor.index]
        fourth_slice = stream[self.lexed_cursors_pos[29].cursor.index : self.lexed_cursors_pos[30].cursor.index]
        fifth_slice = stream[self.lexed_cursors_pos[32].cursor.index : self.lexed_cursors_pos[39].cursor.index]
        sixth_slice = stream[self.lexed_cursors_pos[39].cursor.index : self.lexed_cursors_pos[40].cursor.index]

        self.assertEqual(first_slice, self.lexed_cursors_pos[1].extra)  # Comment slice.
        self.assertEqual(second_slice, self.lexed_cursors_pos[4].extra)  # Doctype slice.
        self.assertEqual(third_slice, self.lexed_cursors_pos[10].value)  # Head tag ID slice.
        self.assertEqual(fourth_slice, f'"{self.lexed_cursors_pos[29].value}"')
        self.assertEqual(fifth_slice, 'img src = "null"   alt="No image provided" ')
        self.assertEqual(sixth_slice.strip(), self.lexed_cursors_pos[39].value)

    def test_cursors_line_col(self) -> None:
        """
        A few random checks to determin if cursor line and columns are accurate.
        """
        stream = self.lexer_cursors_pos.stream_raw

        self.assertEqual((self.lexed_cursors_pos[7].cursor.line, self.lexed_cursors_pos[7].cursor.col), (7, 14))
        self.assertEqual((self.lexed_cursors_pos[26].cursor.line, self.lexed_cursors_pos[26].cursor.col), (12, 22))
        self.assertEqual((self.lexed_cursors_pos[29].cursor.line, self.lexed_cursors_pos[29].cursor.col), (12, 28))

        htmllib.pretty_print_tokens(self.lexed_cursors_pos)

    #endregion (token cursror positions)
