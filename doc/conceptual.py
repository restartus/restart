"""Create README.md images."""
# https://docs.python.org/3/library/pathlib.html
from pathlib import Path

from graphviz import Digraph


def main():
    """Run all the graphs for README.md."""
    conceptual()


def conceptual():
    """Show the conceptual diagram.

    Describe with graphviz how it all works
    """
    # https://graphviz.readthedocs.io/en/stable/api.html#graph
    # name = graph name
    # print(__file__)
    # print(Path(__file__).stem)
    name = Path(__file__).stem
    format_type = "jpg"
    # https://graphviz.readthedocs.io/en/stable/api.html#graphviz.Graph
    dot = Digraph(
        name=name,
        # This will give you a .dot file and the jpg
        # is names .dot.jpg
        filename=Path(name).with_suffix(".dot"),
        # dot is the default neato is a minimum energy model
        # which looks horrible
        # engine="neato",
        format=format_type,
        node_attr={"shape": "box"},
    )
    # neato = Graph(engine="neato")

    # Population superclass using cluster as a special name
    # Note that name must be a named parameter
    # https://graphviz.readthedocs.io/en/stable/examples.html#cluster-py
    with dot.subgraph(name="Pop_class") as c:
        c.attr(style="filled")
        c.node("P", "Population")

    dot.node("C", "Consumption")
    dot.edge("P", "C", "Counts")

    dot.node("A", "Activity")
    dot.edge("P", "A", "Counts")
    dot.edge("A", "P", "%Normal")

    dot.node("D", "Disease (Epidemiological)")
    dot.edge("D", "P", "Recovered")
    dot.edge("P", "D", "Cases")

    dot.node("E", "Economics")
    dot.edge("E", "P", "GDP, Employment")
    dot.edge("P", "E", "Cost")

    dot.node("B", "Behavior")
    dot.edge("P", "B", "Motivation, Ability, Prompt")
    dot.edge("B", "P", "Activity")

    with dot.subgraph(name="Res") as c:
        c.node("R", "Resource")
        c.edge("R", "P", "Supply")
        c.edge("C", "R", "Burn Rates")
        c.node("I", "Inventory")
        c.edge("R", "I", "Fill")
        c.edge("I", "R", "Use")
        c.node("S", "Supply")
        c.edge("R", "S", "Sales Order")
        c.edge("S", "R", "Fulfillment")

    # https://graphviz.readthedocs.io/en/stable/manual.html#basic-usage
    # do not add another format
    # dot.format = "jpg"
    # https://graphviz.readthedocs.io/en/stable/manual.html#engines
    # this creates a directory called conceptual
    # then renders a file named the first argument
    # if you do this, you render the first file and then the
    # format you ask for above
    # dot.render('conceptual')
    # https://graphviz.readthedocs.io/en/stable/api.html#graphviz.render

    dot.render()


if __name__ == "__main__":
    main()
