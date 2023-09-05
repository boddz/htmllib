#!/usr/bin/env python

"""
**FYI**
From now on, this is the main entery point that needs to be used structure wise for module to work as intended.
"""

from src import htmllib


if __name__ == "__main__":
    l = htmllib.Parser('<html lang="en">')
    print(l.parse_tokens_to_node_list())
