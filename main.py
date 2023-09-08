#!/usr/bin/env python

"""
**FYI**
From now on, this is the main entry point that needs to be used structure wise for module to work as intended.
"""

from pprint import PrettyPrinter

from src import htmllib


if __name__ == "__main__":
    HTMLCODE = "<html lang='en'><body><h1>Hello, World!</h1><p> This is a test </p> A good test. </p></body></html>"
    HTMLCODE = "<html lang='en' id='123'> <div lang = 'en'    id ='123'/> <p id='123'>"
    HTMLCODE = "<html id='13' lang='en'> <div lang = 'en'    class ='123'> <p id='123'> </p></html>"

    # parser = htmllib.Parser(HTMLCODE)
    # nodes = parser._parse_tokens_to_node_list()

    # pretty = PrettyPrinter(indent=4)
    # pretty.pprint(nodes)

    htmltree = htmllib.HTMLTree(HTMLCODE)

    # print(htmltree.nodes_list)
    # print(htmltree.doctype_or_comment_nodes)
    # print(htmltree.opening_tag_nodes)
    # print(htmltree.closing_tag_nodes)
    # print(htmltree.self_closing_tag_nodes)
    # print(htmltree.error_nodes)

    # print(htmltree.search_tags_using_attrs({"id": "123", "lang": "en"})[0].inner_html)
    # print(htmltree.search_tags_using_exact_attrs({"lang": "en", "id": "123"}))
    # print(htmltree.search_tags_by_attr(("id", "123")))
    # print(htmltree.search_tags_by_id("123"))
    print(htmltree.search_tags_by_class("123"))
