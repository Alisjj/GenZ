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
