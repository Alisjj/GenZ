import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "<p>",
            "This is a paragraph text",
            props={"font-style": "bold", "font-size": "45px"},
        )
        node2 = HTMLNode(
            "<p>",
            "This is a paragraph text",
            props={"style": '{"color": red, "bg-color": green}'},
        )
        self.assertEqual(node.props_to_html(), ' font-style="bold" font-size="45px"')
        self.assertEqual(
            node2.props_to_html(), ' style="{"color": red, "bg-color": green}"'
        )

    def test_leaf_node_render(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(
            node2.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_lead_node_error(self):
        node = LeafNode(None, None, None)
        self.assertRaises(ValueError, node.to_html)

    def test_parent_node(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        node2 = ParentNode(
            "html",
            [
                ParentNode("head", [LeafNode("title", "Parent and child elements")]),
                ParentNode(
                    "body",
                    [
                        LeafNode("p", "This text is not inside a div"),
                        ParentNode("div", [LeafNode("p", "This text is within a div")]),
                        ParentNode(
                            "div",
                            [
                                LeafNode("p", "This text is within a div with a class"),
                                LeafNode(
                                    "p",
                                    "This text has a class and is within a div with a class",
                                    {"class": "mytext"},
                                ),
                            ],
                            {"class": "mydiv"},
                        ),
                    ],
                ),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )
        self.assertEqual(
            node2.to_html(),
            '<html><head><title>Parent and child elements</title></head><body><p>This text is not inside a div</p><div><p>This text is within a div</p></div><div class="mydiv"><p>This text is within a div with a class</p><p class="mytext">This text has a class and is within a div with a class</p></div></body></html>',
        )


if __name__ == "__main__":
    unittest.main()
