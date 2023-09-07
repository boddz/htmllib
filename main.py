#!/usr/bin/env python

"""
**FYI**
From now on, this is the main entry point that needs to be used structure wise for module to work as intended.
"""

from pprint import PrettyPrinter

from src import htmllib


if __name__ == "__main__":
    HTMLCODE = "<html lang='en'><body><h1>Hello, World!</h1><p> This is a test </p><p> A good test. </p></body></html>"

    parser = htmllib.Parser(HTMLCODE)
    nodes = parser._parse_tokens_to_node_list()

    pretty = PrettyPrinter(indent=4)
    pretty.pprint(nodes)
