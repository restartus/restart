# Using YAML for inputs (and documentation too)

This is going to be a readable way to input small models. Larger ones will have
to be done programmatically because of the data size, but even models with 800
points are still manageable as a YAML file.

It also means that all the tables are in a single location for editing and it is
way more readable than JSON and descriptive than a CSV

[Zetcode](https://www.geeksforgeeks.org/is-python-call-by-reference-or-call-by-value/)
has a good tutorial on this.

# And documentation too (both API docs and generatl)

While we are at it might as well get documentation from code working

## Automatically from docstrings in the code

[Peter
Kong](https://medium.com/@peterkong/comparison-of-python-documentation-generators-660203ca3804)
has a good comparison between four of them and then there is mydocs as well, but
we want something that uses docstrings internally. And there is the official
list from [Python.org](https://wiki.python.org/moin/DocumentationTools). And a
list for the [Python
Guide](https://docs.python-guide.org/writing/documentation/) plus a tutorial at
[Real Python](https://realpython.com/documenting-python-code/)

- [pdoc3](https://pdoc3.github.io/pdoc/) for Python 3
- [pydoc](https://docs.python.org/3/library/pydoc.html) this comes standard with
    python

Then things mentioned
- [sphinx](http://www.sphinx-doc.org/en/master/index.html) The main problem is
- [pdoc](https://github.com/BurntSushi/pdoc) less complex than Sphinx and you
    should use
    that it is very heavy weight and uses RST files but it can use
- [doxygen](http://www.stack.nl/~dimitri/doxygen/index.html) powerful but ugly
- [pydoctor](https://github.com/twisted/pydoctor) Python 2 only so exclude it

## Then for general documentation website
- [Read the Docs](https://readthedocs.org/). You see many open source projects using it. And it includes free hosting of your documentation so great for open source projects
- [MkDocs](https://www.mkdocs.org) - This is a fast HTML centric thingy that works in Markdown with a YAML
    file but it does not read doc strings. it does seem like something Hugo is a
    better choice with the right template.
