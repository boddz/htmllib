#!/usr/bin/env python


"""
========================
HTMLLIB HTMLTree Testing
========================

Unit tests for the ``HTMLTree`` class in htmlib.htmltree module.
"""


from __future__ import annotations

from src import htmllib

from unittest import TestCase


class TestLexerMethods(TestCase):
    def setUp(self) -> None:
        self.htmltree_simple = htmllib.HTMLTree("""
            <!DOCTYPE html>

            <html lang="en">
                <head>
                    <meta lang="en" charset="UTF-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Document</title>
                <!-- A comment
                    Wow -->
                </head>
                <body>
                    <h1>Hello, World!</h1>
                    <img src="null" alt="null null"/>
                    <p>This is a simple HTML document to test HTMLTree methods</p>
                    <p id="2nd_p" class="second_best"> I am second best :( </p>
                </body>
                <>
            </html>
        """)

    def test_htmltree_simple_nodes(self) -> None:
        self.assertNotEqual(self.htmltree_simple.nodes_list, [])
        self.assertEqual(len(self.htmltree_simple.nodes_list), 22)
        self.assertEqual(len(self.htmltree_simple.doctype_or_comment_nodes), 2)
        self.assertEqual(len(self.htmltree_simple.opening_tag_nodes), 11)
        self.assertEqual(len(self.htmltree_simple.closing_tag_nodes), 7)
        self.assertEqual(len(self.htmltree_simple.self_closing_tag_nodes), 1)
        self.assertEqual(len(self.htmltree_simple.error_nodes), 1)

        for node in self.htmltree_simple.doctype_or_comment_nodes:
            self.assertIsInstance(node, htmllib.HTMLDoctypeOrCommNode)

        for node in self.htmltree_simple.opening_tag_nodes:
            self.assertIsInstance(node, htmllib.HTMLOpeningTagNode)

        for node in self.htmltree_simple.closing_tag_nodes:
            self.assertIsInstance(node, htmllib.HTMLClosingTagNode)

        for node in self.htmltree_simple.self_closing_tag_nodes:
            self.assertIsInstance(node, htmllib.HTMLSelfClosingTagNode)

        for node in self.htmltree_simple.error_nodes:
            self.assertIsInstance(node, htmllib.HTMLErrorNode)

    def test_htmltree_simple_search_tags_by_name(self) -> None:
        tags_h1 = self.htmltree_simple.search_tags_by_name("h1")
        tags_p = self.htmltree_simple.search_tags_by_name("p")
        tags_img_sc = self.htmltree_simple.search_tags_by_name("img", self_closing=True)
        self.assertIsInstance(tags_h1[0], htmllib.HTMLOpeningTagNode)
        self.assertIsInstance(tags_p[0], htmllib.HTMLOpeningTagNode)
        self.assertIsInstance(tags_p[1], htmllib.HTMLOpeningTagNode)
        self.assertIsInstance(tags_img_sc[0], htmllib.HTMLSelfClosingTagNode)
        self.assertEqual(tags_h1[0].inner_html, "Hello, World!")
        self.assertIsNone(tags_h1[0].attributes)
        self.assertEqual(tags_p[0].inner_html, "This is a simple HTML document to test HTMLTree methods")
        self.assertIsNone(tags_p[0].attributes)
        self.assertEqual(tags_p[1].inner_html, " I am second best :( ")
        self.assertEqual(tags_p[1].attributes, {"id": "2nd_p", "class": "second_best"})
        self.assertEqual(tags_img_sc[0].attributes, {"src": "null", "alt": "null null"})

    def test_htmltree_simple_search_tags_by_attrs(self) -> None:
        tags_meta = self.htmltree_simple.search_tags_by_attrs({
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0"
        })
        tags_p = self.htmltree_simple.search_tags_by_attrs({"class": "second_best", "id": "2nd_p"})
        tags_img_sc = self.htmltree_simple.search_tags_by_attrs({"src": "null", "alt": "null null"}, self_closing=True)
        self.assertIsInstance(tags_meta[0], htmllib.HTMLOpeningTagNode)
        self.assertIsInstance(tags_meta[1], htmllib.HTMLOpeningTagNode)
        self.assertIsInstance(tags_p[0], htmllib.HTMLOpeningTagNode)
        self.assertIsInstance(tags_img_sc[0], htmllib.HTMLSelfClosingTagNode)
        self.assertIsNone(tags_meta[0].inner_html)
        self.assertIsNone(tags_meta[1].inner_html)
        self.assertEqual(tags_p[0].inner_html, " I am second best :( ")

    def test_htmltree_simple_search_tags_by_exact_attrs(self) -> None:
        tags_meta1 = self.htmltree_simple.search_tags_by_exact_attrs({
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0"
        })
        tags_meta2 = self.htmltree_simple.search_tags_by_exact_attrs({"content": "IE=edge", "http-equiv": "X-UA-Compatible"})
        tags_p = self.htmltree_simple.search_tags_by_exact_attrs({"id": "2nd_p", "class": "second_best"})
        tags_img_sc = self.htmltree_simple.search_tags_by_exact_attrs({"src": "null", "alt": "null null"}, self_closing=True)
        self.assertIsInstance(tags_meta1[0], htmllib.HTMLOpeningTagNode)
        self.assertIsInstance(tags_meta1[1], htmllib.HTMLOpeningTagNode)
        self.assertEqual(tags_meta2, [])
        self.assertIsInstance(tags_p[0], htmllib.HTMLOpeningTagNode)
        self.assertIsInstance(tags_img_sc[0], htmllib.HTMLSelfClosingTagNode)
        self.assertIsNone(tags_meta1[0].inner_html)
        self.assertIsNone(tags_meta1[1].inner_html)
        self.assertEqual(tags_p[0].inner_html, " I am second best :( ")

    def test_htmltree_simple_search_tags_by_attr(self) -> None:
        tags_lang = self.htmltree_simple.search_tags_by_attr(("lang", "en"))
        tags_name = self.htmltree_simple.search_tags_by_attr(("name", "viewport"))
        tags_could_not_find = self.htmltree_simple.search_tags_by_attr(("None", "None"))
        tags_alt_sc = self.htmltree_simple.search_tags_by_attr(("alt", "null null"), self_closing=True)
        self.assertEqual(tags_could_not_find, [])
        self.assertIsInstance(tags_lang[0], htmllib.HTMLOpeningTagNode)
        self.assertIsInstance(tags_lang[1], htmllib.HTMLOpeningTagNode)
        self.assertIsInstance(tags_name[0], htmllib.HTMLOpeningTagNode)
        self.assertIsInstance(tags_name[1], htmllib.HTMLOpeningTagNode)
        self.assertIsInstance(tags_alt_sc[0], htmllib.HTMLSelfClosingTagNode)
        self.assertEqual(tags_lang[0].tag_name, "html")
        self.assertEqual(tags_lang[1].tag_name, "meta")
        self.assertEqual(tags_name[0].tag_name, "meta")
        self.assertEqual(tags_name[1].tag_name, "meta")
        self.assertEqual(tags_alt_sc[0].tag_name, "img")

    # This is just a shortcut function test, so it is not super important.
    def test_htmltree_simple_search_tags_by_id(self) -> None:
        tags_id = self.htmltree_simple.search_tags_by_id("2nd_p")
        self.assertEqual(tags_id[0].tag_name, "p")
        self.assertEqual(tags_id[0].inner_html, " I am second best :( ")

    # This is just a shortcut function test, so it is not super important.
    def test_htmltree_simple_search_tags_by_class(self) -> None:
        tags_id = self.htmltree_simple.search_tags_by_class("second_best")
        self.assertEqual(tags_id[0].tag_name, "p")
        self.assertEqual(tags_id[0].inner_html, " I am second best :( ")
