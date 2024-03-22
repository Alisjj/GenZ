import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("<p>", "This is a paragraph text", props={"font-style": "bold", "font-size": "45px"})
        node2 = HTMLNode("<p>", "This is a paragraph text", props={"style": '{"color": red, "bg-color": green}'})
        self.assertEqual(node.props_to_html(), ' font-style="bold" font-size="45px"')
        self.assertEqual(node2.props_to_html(), ' style="{"color": red, "bg-color": green}"')
    
    
if __name__ == "__main__":
    unittest.main()
