#!/usr/bin/env python


"""
======================
HTMLLIB Parser Testing
======================

Unit tests for the ``Parser`` class in htmlib.parser module.
"""


from __future__ import annotations

from src import htmllib

from unittest import TestCase


class TestParserMethods(TestCase):
    def setUp(self) -> None:
        self.parser_opening_tag = htmllib.Parser("<html>")
        self.parser_opening_tag_attr = htmllib.Parser("<html lang = 'en' >")
        self.parser_opening_tag_attrs = htmllib.Parser("<html lang = 'en' id='123</p>sd' class= 'foo'>")
        self.parser_closing_tag = htmllib.Parser("</html>")
        self.parser_self_closing_tag = htmllib.Parser("<img/>")
        self.parser_self_closing_tag_attr = htmllib.Parser("<img src='null'/>")
        self.parser_self_closing_tag_attrs = htmllib.Parser("""<img src = "null" alt='123' id="img<img/>id"/>""")
        self.parser_no_valid_id_error = htmllib.Parser("<></>")
        self.parser_never_closed_error = htmllib.Parser("<div id='111' \n\n\nclass='zxc'")
        self.parser_never_closed_error_sc = htmllib.Parser("<img/")
        self.parser_open_tag_inner_content = htmllib.Parser("<div><div><div>test</div><p>a</p><p>456</p></p></div>")
        self.parser_nothing_to_parse = htmllib.Parser("html>html/>!='sds'")
        self.parser_not_all_valid = htmllib.Parser("html>html/>!='sds<body id='im_valid'> Yay, I'm valid </body>'")

    def test_parser_opening_tag(self) -> None:
        nodes = self.parser_opening_tag._parse_tokens_to_node_list()
        self.assertIsInstance(nodes[0], htmllib.HTMLOpeningTagNode)
        self.assertEqual(nodes[0].tag_name, "html")
        self.assertEqual(nodes[0].attributes, None)
        self.assertEqual(nodes[0].inner_html, None)
        self.assertEqual(nodes[0].cursor_start.index, 0)
        self.assertEqual(nodes[0].cursor_start.line, 1)
        self.assertEqual(nodes[0].cursor_start.col, 1)
        self.assertEqual(nodes[0].cursor_end.index, 5)
        self.assertEqual(nodes[0].cursor_end.line, 1)
        self.assertEqual(nodes[0].cursor_end.col, 6)

    def test_parser_opening_tag_attr(self) -> None:
        nodes = self.parser_opening_tag_attr._parse_tokens_to_node_list()
        self.assertIsInstance(nodes[0], htmllib.HTMLOpeningTagNode)
        self.assertEqual(nodes[0].tag_name, "html")
        self.assertEqual(nodes[0].attributes, {"lang": "en"})
        self.assertEqual(nodes[0].inner_html, None)
        self.assertEqual(nodes[0].cursor_start.index, 0)
        self.assertEqual(nodes[0].cursor_start.line, 1)
        self.assertEqual(nodes[0].cursor_start.col, 1)
        self.assertEqual(nodes[0].cursor_end.index, 18)
        self.assertEqual(nodes[0].cursor_end.line, 1)
        self.assertEqual(nodes[0].cursor_end.col, 19)

    def test_parser_opening_tag_attrs(self) -> None:
        nodes = self.parser_opening_tag_attrs._parse_tokens_to_node_list()
        self.assertIsInstance(nodes[0], htmllib.HTMLOpeningTagNode)
        self.assertEqual(nodes[0].tag_name, "html")
        self.assertEqual(nodes[0].attributes, {"lang": "en", "id": "123</p>sd", "class": "foo"})
        self.assertEqual(nodes[0].inner_html, None)
        self.assertEqual(nodes[0].cursor_start.index, 0)
        self.assertEqual(nodes[0].cursor_start.line, 1)
        self.assertEqual(nodes[0].cursor_start.col, 1)
        self.assertEqual(nodes[0].cursor_end.index, 45)
        self.assertEqual(nodes[0].cursor_end.line, 1)
        self.assertEqual(nodes[0].cursor_end.col, 46)

    def test_parser_closing_tag(self) -> None:
        nodes = self.parser_closing_tag._parse_tokens_to_node_list()
        self.assertIsInstance(nodes[0], htmllib.HTMLClosingTagNode)
        self.assertEqual(nodes[0].tag_name, "html")
        self.assertEqual(nodes[0].cursor_start.index, 0)
        self.assertEqual(nodes[0].cursor_start.line, 1)
        self.assertEqual(nodes[0].cursor_start.col, 1)
        self.assertEqual(nodes[0].cursor_end.index, 6)
        self.assertEqual(nodes[0].cursor_end.line, 1)
        self.assertEqual(nodes[0].cursor_end.col, 7)

    def test_parser_self_closing_tag(self) -> None:
        nodes = self.parser_self_closing_tag._parse_tokens_to_node_list()
        self.assertIsInstance(nodes[0], htmllib.HTMLSelfClosingTagNode)
        self.assertEqual(nodes[0].tag_name, "img")
        self.assertEqual(nodes[0].attributes, None)
        self.assertEqual(nodes[0].cursor_start.index, 0)
        self.assertEqual(nodes[0].cursor_start.line, 1)
        self.assertEqual(nodes[0].cursor_start.col, 1)
        self.assertEqual(nodes[0].cursor_end.index, 5)
        self.assertEqual(nodes[0].cursor_end.line, 1)
        self.assertEqual(nodes[0].cursor_end.col, 6)

    def test_parser_self_closing_tag_attr(self) -> None:
        nodes = self.parser_self_closing_tag_attr._parse_tokens_to_node_list()
        self.assertIsInstance(nodes[0], htmllib.HTMLSelfClosingTagNode)
        self.assertEqual(nodes[0].tag_name, "img")
        self.assertEqual(nodes[0].attributes, {"src": "null"})
        self.assertEqual(nodes[0].cursor_start.index, 0)
        self.assertEqual(nodes[0].cursor_start.line, 1)
        self.assertEqual(nodes[0].cursor_start.col, 1)
        self.assertEqual(nodes[0].cursor_end.index, 16)
        self.assertEqual(nodes[0].cursor_end.line, 1)
        self.assertEqual(nodes[0].cursor_end.col, 17)

    def test_parser_self_closing_tag_attrs(self) -> None:
        nodes = self.parser_self_closing_tag_attrs._parse_tokens_to_node_list()
        self.assertIsInstance(nodes[0], htmllib.HTMLSelfClosingTagNode)
        self.assertEqual(nodes[0].tag_name, "img")
        self.assertEqual(nodes[0].attributes, {"src": "null", "alt": "123", "id": "img<img/>id"})
        self.assertEqual(nodes[0].cursor_start.index, 0)
        self.assertEqual(nodes[0].cursor_start.line, 1)
        self.assertEqual(nodes[0].cursor_start.col, 1)
        self.assertEqual(nodes[0].cursor_end.index, 45)
        self.assertEqual(nodes[0].cursor_end.line, 1)
        self.assertEqual(nodes[0].cursor_end.col, 46)

    def test_parser_no_valid_id_error(self) -> None:
        nodes = self.parser_no_valid_id_error._parse_tokens_to_node_list()
        self.assertIsInstance(nodes[0], htmllib.HTMLErrorNode)
        self.assertIsInstance(nodes[0].message, str)
        self.assertIsInstance(nodes[0].exception, htmllib.NonValidTagIDError)
        self.assertEqual(nodes[0].cursor_start.index, 0)
        self.assertEqual(nodes[0].cursor_start.line, 1)
        self.assertEqual(nodes[0].cursor_start.col, 1)
        self.assertEqual(nodes[0].cursor_end.index, 1)
        self.assertEqual(nodes[0].cursor_end.line, 1)
        self.assertEqual(nodes[0].cursor_end.col, 2)
        self.assertIsInstance(nodes[1], htmllib.HTMLErrorNode)
        self.assertIsInstance(nodes[1].message, str)
        self.assertIsInstance(nodes[1].exception, htmllib.NonValidTagIDError)
        self.assertEqual(nodes[1].cursor_start.index, 2)
        self.assertEqual(nodes[1].cursor_start.line, 1)
        self.assertEqual(nodes[1].cursor_start.col, 3)
        self.assertEqual(nodes[1].cursor_end.index, 3)
        self.assertEqual(nodes[1].cursor_end.line, 1)
        self.assertEqual(nodes[1].cursor_end.col, 4)

    def test_parser_never_closed_error(self) -> None:
        nodes = self.parser_never_closed_error._parse_tokens_to_node_list()
        self.assertIsInstance(nodes[0], htmllib.HTMLErrorNode)
        self.assertIsInstance(nodes[0].message, str)
        self.assertIsInstance(nodes[0].exception, htmllib.NeverEndedTagError)
        self.assertEqual(nodes[0].cursor_start.index, 0)
        self.assertEqual(nodes[0].cursor_start.line, 1)
        self.assertEqual(nodes[0].cursor_start.col, 1)
        self.assertEqual(nodes[0].cursor_end.index, 28)
        self.assertEqual(nodes[0].cursor_end.line, 4)
        self.assertEqual(nodes[0].cursor_end.col, 12)

    def test_parser_never_closed_error_self_closing(self) -> None:
        nodes = self.parser_never_closed_error_sc._parse_tokens_to_node_list()
        self.assertIsInstance(nodes[0], htmllib.HTMLErrorNode)
        self.assertIsInstance(nodes[0].message, str)
        self.assertIsInstance(nodes[0].exception, htmllib.NeverEndedTagError)
        self.assertEqual(nodes[0].cursor_start.index, 0)
        self.assertEqual(nodes[0].cursor_start.line, 1)
        self.assertEqual(nodes[0].cursor_start.col, 1)
        self.assertEqual(nodes[0].cursor_end.index, 5)
        self.assertEqual(nodes[0].cursor_end.line, 1)
        self.assertEqual(nodes[0].cursor_end.col, 6)

    def test_parser_open_tag_inner_content(self) -> None:
        nodes = self.parser_open_tag_inner_content._parse_tokens_to_node_list()
        self.assertIsInstance(nodes[0], htmllib.HTMLOpeningTagNode)
        self.assertEqual(nodes[1].inner_html, "<div>test</div><p>a</p><p>456</p></p>")
        self.assertEqual(nodes[2].inner_html, "test")
        self.assertEqual(nodes[4].inner_html, "a")
        self.assertEqual(nodes[6].inner_html, "456")

    def test_parser_not_all_valid(self) -> None:
        nodes = self.parser_not_all_valid._parse_tokens_to_node_list()
        self.assertIsInstance(nodes[0], htmllib.HTMLOpeningTagNode)

    def test_parser_nothing_to_parse(self) -> None:
        nodes = self.parser_nothing_to_parse._parse_tokens_to_node_list()
        self.assertEqual(nodes, [])
