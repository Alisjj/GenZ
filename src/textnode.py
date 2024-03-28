import re

from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        return False

    def __repr__(self) -> str:
        return repr(f"TextNode({self.text}, {self.text_type}, {self.url})")


def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Invalid text type: {text_node.text_type}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            result.append(node)
            continue

        text: str = node.text
        start_index = text.find(delimiter)
        while start_index != -1:
            closing = text.find(delimiter, start_index + len(delimiter))
            if closing == -1:
                raise ValueError(
                    "Invalid Markdown syntax: Missing closing delimiter for code block."
                )

            result.append(TextNode(text[:start_index], text_type_text))
            result.append(
                TextNode(text[start_index + len(delimiter) : closing], text_type)
            )

            text = text[closing + len(delimiter) :]
            start_index = text.find(delimiter)

        result.append(TextNode(text, node.text_type))

    return result


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            result.append(node)
            continue
        original_text = node.text
        if not original_text:
            continue
        images = extract_markdown_images(original_text)
        if not images:
            result.append(node)
            continue

        while images:
            image = images.pop(0)
            text = original_text.split(f"![{image[0]}]({image[1]})", 1)[0]
            original_text = original_text.split(f"![{image[0]}]({image[1]})", 1)[1]
            if text:
                result.append(TextNode(text, text_type_text))
            result.append(TextNode(image[0], text_type_image, image[1]))

        if original_text:
            result.append(TextNode(original_text, text_type_text))

    return result


def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            result.append(node)
            continue
        original_text = node.text
        if not original_text:
            continue
        links = extract_markdown_links(original_text)
        if not links:
            result.append(node)
            continue

        while links:
            link = links.pop(0)
            text = original_text.split(f"[{link[0]}]({link[1]})", 1)[0]
            original_text = original_text.split(f"[{link[0]}]({link[1]})", 1)[1]
            if text:
                result.append(TextNode(text, text_type_text))
            result.append(TextNode(link[0], text_type_link, link[1]))

        if original_text:
            result.append(TextNode(original_text, text_type_text))

    return result


def text_to_textnodes(text):
    text = [TextNode(text, text_type_text)]
    bold = split_nodes_delimiter(text, "**", text_type_bold)
    italic = split_nodes_delimiter(bold, "*", text_type_italic)
    code_block = split_nodes_delimiter(italic, "`", text_type_code)
    image = split_nodes_image(code_block)
    return split_nodes_link(image)