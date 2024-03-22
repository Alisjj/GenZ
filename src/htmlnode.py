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
        for key, value in self.props.items():
            result += f' {key}="{value}"'

        return result
    

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("No Value is given.")
        if self.tag and self.props:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        elif self.tag:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return self.value
    