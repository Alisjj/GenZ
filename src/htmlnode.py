import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"tag: {self.tag},\n value: {self.value},\n children:{self.children},\n props: {self.props} "

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        result = ""
        if self.props is None:
            return result
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        return result


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Error: No Value given for the leaf Node")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Error: No tag was given for a parent Node")

        if self.children is None:
            raise ValueError("Error: no children are given for the parent Node")

        result = f"<{self.tag}{self.props_to_html()}>"

        for node in self.children:
            result += node.to_html()

        return result + f"</{self.tag}>"

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
        if len(qoute) == block.count("\n"):
            return block_type_quote
    if unordered_list:
        if len(unordered_list) == block.count("\n"):
            return block_type_unordered_list
    if ordered_list:
        if len(ordered_list) == block.count("\n"):
            return block_type_ordered_list
    
    return block_type_paragraph

def block_to_p_tag(block):
        return LeafNode("p", value=block)

def block_to_code(block):
    text = block.strip("``` ")
    value = LeafNode("pre", value=text)
    return ParentNode("code", [value])

def block_to_heading(block):
    return LeafNode(f"h{block.count("#")}", block)

def block_to_unordered_list(block):
    children = []
    lines = block.split("\n")
    for line in lines:
        children.append(LeafNode("li", line.lstrip("-* ")))
    return ParentNode("ul", [children])

def block_to_ordered_list(block):
    children = []
    lines = block.split("\n")
    pattern = r'^[a-zA-Z\d]+\.\s'
    for line in lines:
        stripped = re.sub(pattern, '', line)
        children.append(LeafNode("li", stripped))
    return ParentNode("ol", [children])

def block_to_qoute(block):
    children = []
    lines = block.split("\n")
    for line in lines:
        children.append(LeafNode("p", line.strip("> ")))
    return ParentNode("blockquote", [children])


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
        elif block_type == block_type_quote(block):
            result.append(block_to_qoute(block_to_code))

    return ParentNode("div", [result])

