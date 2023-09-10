#!/usr/bin/env python

"""
**FYI**
From now on, this is the main entry point that needs to be used structure wise for module to work as intended.
"""


from urllib import request
from pprint import PrettyPrinter

from src import htmllib


if __name__ == "__main__":
    # HTMLCODE = "<html lang='en'><body><h1>Hello, World!</h1><p> This is a test </p> A good test. </p></body></html>"
    # HTMLCODE = "<html lang='en' id='123'> <div lang = 'en'    id ='123'/> <p id='123'>"
    HTMLCODE = "<html id='123' lang='en'> <div lang = 'en'    class ='123'> <p id='123'> </p></html><img id='123'/>"

    resp = request.urlopen("https://example.com")
    HTMLCODE = resp.read() if resp.status == 200 else ""

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

    print(htmltree.search_tags_by_name("title"))
    # print(htmltree.search_tags_by_attrs({"lang": "en", "id": "123"}))
    # print(htmltree.search_tags_by_exact_attrs({"id": "123", "lang": "en"}))
    # print(htmltree.search_tags_by_attr(("type", "text/css")))
    # print(htmltree.search_tags_by_id("123"))
    # print(htmltree.search_tags_by_class("123"))
    # print(htmltree.search_tags_by_name("img", self_closing=True))
    # print(htmltree.search_tags_by_attrs({"lang": "en", "id": "123"}, self_closing=True))
    # print(htmltree.search_tags_by_exact_attrs({"id": "123", "lang": "en"}, self_closing=True))
    # print(htmltree.search_tags_by_attr(("type", "text/css"), self_closing=True))
    # print(htmltree.search_tags_by_id("123", self_closing=True))
    # print(htmltree.search_tags_by_class("123", self_closing=True))
