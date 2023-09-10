=======
HTMLLIB
=======

A Python3 Module that provides an API for gathering data from a stream/ string of HTML code.

There are no docs for this project yet as it is still in its early stages of development, although I have got some
cool things implemented, they will be in the ``main.py`` file either commented or uncommented. The ``main.py`` file is
the entry point for manual testing of the HTMLLIB module.

More information on how to use the module and examples to go along with it will be added soon, they are just not
priority as of this moment.


---------------------------
Parser Process Flow Diagram
---------------------------

.. image:: assets/parse_diagram.png
    :alt: A Diagram of HTMLLIB's Parse Process 


-----------
Quick Start
-----------

Not all of the features I want are implemented yet, but here are a few useful ones to get you started
(**use in main.py for imports to work**):

    .. code-block:: python

        from src import htmllib

        htmltree = htmllib.HTMLTree('''
            <html lang="en">
                <head>
                    <title>HTMLLIB Test Page</title>
                </head>
                <body>
                    <section class="main">
                        <h1>Hello, World!</h1>
                        <p id="find_me">You found me!</p>
                    </section>
                </body>
            </html>
        ''')

        print(htmltree.search_tags_by_name("html")[0].attributes)   # -> "{'lang': 'en'}"
        print(htmltree.search_tags_by_id("find_me")[0].inner_html)  # -> "You found me!"
        print(htmltree.search_tags_by_class("main")[0].tag_name)    # -> "section"


------------------
Testing the Module
------------------

This project has decent test coverage thus far using the `unittest <https://docs.python.org/3/library/unittest.html>`_
module from Python3's standard library.

Run all tests with:

    .. code-block:: bash

        python -m unittest discover tests/

Run a single test with:

    .. code-block:: bash

        python -m unittest tests/test_<which>.py
