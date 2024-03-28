import unittest

from textnode import (
    TextNode,
    split_nodes_delimiter,
    split_nodes_image,
    extract_markdown_images,
    extract_markdown_links,
    text_type_bold,
    text_type_code,
    text_type_text,
    text_type_image,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", "italic", "https")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_default_url(self):
        node = TextNode("This is a text node", "italic")
        node2 = TextNode("This is a text node", "bold", "")
        self.assertEqual(node.url, None)
        self.assertNotEqual(node2.url, None)

    def test_split_nodes_delimeter(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        node2 = TextNode("This is text with a *bold text* in it", text_type_text)
        node3 = TextNode("This is *text with* a *bold text* in it", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        new_nodes2 = split_nodes_delimiter([node2], "*", text_type_bold)
        new_nodes3 = split_nodes_delimiter([node3], "*", text_type_bold)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
        )

        self.assertEqual(
            new_nodes2,
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bold text", text_type_bold),
                TextNode(" in it", text_type_text),
            ],
        )

        self.assertEqual(
            new_nodes3,
            [
                TextNode("This is ", text_type_text),
                TextNode("text with", text_type_bold),
                TextNode(" a ", text_type_text),
                TextNode("bold text", text_type_bold),
                TextNode(" in it", text_type_text),
            ],
        )

    def test_markdown_extraction(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        text2 = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"

        self.assertEqual(
            extract_markdown_images(text),
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("another", "https://i.imgur.com/dfsdkjfd.png"),
            ],
        )

        self.assertEqual(
            extract_markdown_links(text2),
            [
                ("link", "https://www.example.com"),
                ("another", "https://www.example.com/another"),
            ],
        )

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        node2 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) that is it",
            text_type_text,
        )
        node3 = TextNode(
            "This is text no image",
            text_type_text,
        )
        new_nodes = split_nodes_image([node, node2, node3])

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" that is it", text_type_text),
                TextNode( "This is text no image", text_type_text)
            ],
        )


if __name__ == "__main__":
    unittest.main()
