import os
import re

from htmlnode import LeafNode, ParentNode
from textnode import TextNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

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

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks]
    return blocks

def block_to_block_type(block: str):
    heading = re.findall(r"#{1,6}?\s.", block)
    qoute = re.findall(r"^>\s.*$", block, re.M)
    unordered_list = re.findall(r"^[-*]\s.*$", block, re.M)
    ordered_list = re.findall(r"^\d+\.\s.*$", block, re.M)
    if heading:
        return block_type_heading
    if block.startswith("```") and block.endswith("```"):
        return block_type_code 
    if qoute:
        if len(qoute) == block.count(">"):
            return block_type_quote
    if unordered_list:
        # if len(unordered_list) == block.count("\n"):
        return block_type_unordered_list
    if ordered_list:
        # if len(ordered_list) == block.count("\n"):
        return block_type_ordered_list
    
    return block_type_paragraph

def block_to_p_tag(block):
    val = text_to_textnodes(block)
    children = []
    for v in val:
        children.append(text_node_to_html_node(v))
    return ParentNode("p", children)

def block_to_code(block):
    text = block.lstrip("``` ")
    val = text_to_textnodes(text.rstrip(" ```"))
    children = []
    for v in val:
        children.append(text_node_to_html_node(v))
    value = ParentNode("pre", children)
    return ParentNode("code", [value])

def block_to_heading(block):
    val = text_to_textnodes(block.lstrip("# "))
    children = []
    for v in val:
        children.append(text_node_to_html_node(v))
    return ParentNode(f"h{block.count("#")}", children)

def block_to_unordered_list(block):
    children = []
    lines = block.split("\n")
    for line in lines:
        sub_child = []
        val = text_to_textnodes(line.lstrip("-*"))
        for v in val:
            sub_child.append(text_node_to_html_node(v))
        children.append(ParentNode("li", sub_child))
    return ParentNode("ul", children)

def block_to_ordered_list(block):
    children = []
    lines = block.split("\n")
    pattern = r'^[a-zA-Z\d]+\.\s'
    for line in lines:
        sub_child = []
        stripped = re.sub(pattern, '', line)
        val = text_to_textnodes(stripped)
        for v in val:
            sub_child.append(text_node_to_html_node(v))
        children.append(ParentNode("li", sub_child))
    return ParentNode("ol", children)

def block_to_qoute(block):
    children = []
    lines = block.split("> ")
    for line in lines:
        if line:
            sub_child = []
            val = text_to_textnodes(line.lstrip("> "))
            for v in val:
                sub_child.append(text_node_to_html_node(v))
            children.append(ParentNode("span", sub_child))
    return ParentNode("blockquote", children)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    result = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == block_type_code:
            result.append(block_to_code(block))
        elif block_type == block_type_heading:
            result.append(block_to_heading(block))
        elif block_type == block_type_paragraph:
            result.append(block_to_p_tag(block))
        elif block_type == block_type_unordered_list:
            result.append(block_to_unordered_list(block))
        elif block_type == block_type_ordered_list:
            result.append(block_to_ordered_list(block))
        elif block_type == block_type_quote:
            result.append(block_to_qoute(block))
    return ParentNode("div", result)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.count("#") == 1:
            return block.lstrip("# ")
    
    raise Exception("Error: Document has no header.")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        markdown = file.read()

    with open(template_path, "r") as template:
        temp = template.read()

    md_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    new = temp.replace("{{ Title }}", title)
    new = new.replace("{{ Content }}", md_html)

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    
    with open(dest_path, "w") as dest:
        dest.write(new)
