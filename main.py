#!/usr/bin/env python

"""
**FYI**
From now on, this is the main entery point that needs to be used structure wise for module to work as intended.
"""

from src import htmllib


if __name__ == "__main__":
    parser = htmllib.Parser('<html><div id="1"><div id="2">qwerty</div></div></html>')
    parser._parse_tokens_to_node_list()

    parser._generate_nodes_content(reverse_pair=True)

    for node_html in parser.tag_nodes_list:
        print(node_html)
