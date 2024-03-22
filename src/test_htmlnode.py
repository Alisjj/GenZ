import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("<p>", "This is a paragraph text", props={"font-style": "bold", "font-size": "45px"})
        node2 = HTMLNode("<p>", "This is a paragraph text", props={"style": '{"color": red, "bg-color": green}'})
        self.assertEqual(node.props_to_html(), ' font-style="bold" font-size="45px"')
        self.assertEqual(node2.props_to_html(), ' style="{"color": red, "bg-color": green}"')

    def test_leaf_node_render(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
    def test_lead_node_error(self):
        node = LeafNode(None, None, None)
        self.assertRaises(ValueError, node.to_html)
    
    
if __name__ == "__main__":
    unittest.main()
