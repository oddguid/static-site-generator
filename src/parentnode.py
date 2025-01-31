from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")

        if self.children is None:
            raise ValueError("Invalid HTML: no children")

        props = self.props_to_html();

        result = f"<{self.tag}{props}>"

        for child in self.children:
            result += child.to_html()

        result += f"</{self.tag}>"

        return result

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
