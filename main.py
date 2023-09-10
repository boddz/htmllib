#!/usr/bin/env python


from src import htmllib


if __name__ == "__main__":
    # Manual testing code goes here ::

    htmltree = htmllib.HTMLTree("""
        <!DOCTYPE html>
        <html lang="en" id="htmlid">
            <head>
                <title>HTMLLIB Test Page</title>
            </head>
            <body>
                <section class="main">
                    <h1>Hello, World!</h1>
                    <p id="find_me">You found me!</p>
                    <button type="button" id="pointless">Click Me!</button>
                    <button type="button2" id="pointless2">Click Me!2</button>
                </section>
                <br/>
                <img src="assets/parse_diagram.png" alt="A diagram of HTMLLib's parse process"/>
                <img src="assets/parse_diagram.png" alt="A diagram of HTMLLib's parse process">
            </body>
        </html>
    """)

    print(htmltree.doctype_raw)
    print(htmltree.search_tags_by_name("html")[0].attributes)
    print(htmltree.search_tags_by_attrs({"id": "htmlid", "lang": "en"}))
    print(htmltree.search_tags_by_exact_attrs({"type": "button", "id": "pointless"}))
    # print(htmltree.search_tags_by_exact_attrs({"id": "pointless", "type": "button"}))  # Nothing due to strict match.
    print(htmltree.search_tags_by_attr(("type", "button")))
    print(htmltree.search_tags_by_attrs_keys(["alt", "src"]))
    print(htmltree.search_tags_by_exact_attrs_keys(["src", "alt"]))
    # print(htmltree.search_tags_by_exact_attrs_keys(["alt", "src"]))  # Nothing due to strict match.
    print(htmltree.search_tags_by_attr_key("type"))
    print(htmltree.search_tags_by_name("br", self_closing=True))
    print(htmltree.search_tags_by_id("find_me")[0].inner_html)
    print(htmltree.search_tags_by_class("main")[0].tag_name)
