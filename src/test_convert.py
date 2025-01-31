import unittest
from convert import text_node_to_html_node
from leafnode import LeafNode
from textnode import TextNode, TextType

class TestConvert(unittest.TestCase):
    def test_normal(self):
        text = "sample text"
        text_type = TextType.NORMAL

        node = TextNode(text, text_type)

        result = text_node_to_html_node(node)

        self.assertEqual(isinstance(result, LeafNode), True)
        self.assertEqual(result.to_html(),
                         "sample text")

    def test_bold(self):
        text = "sample text"
        text_type = TextType.BOLD

        node = TextNode(text, text_type)

        result = text_node_to_html_node(node)

        self.assertEqual(isinstance(result, LeafNode), True)
        self.assertEqual(result.to_html(),
                         "<b>sample text</b>")

    def test_italic(self):
        text = "sample text"
        text_type = TextType.ITALIC

        node = TextNode(text, text_type)

        result = text_node_to_html_node(node)

        self.assertEqual(isinstance(result, LeafNode), True)
        self.assertEqual(result.to_html(),
                         "<i>sample text</i>")

    def test_code(self):
        text = "sample text"
        text_type = TextType.CODE

        node = TextNode(text, text_type)

        result = text_node_to_html_node(node)

        self.assertEqual(isinstance(result, LeafNode), True)
        self.assertEqual(result.to_html(),
                         "<code>sample text</code>")

    def test_link(self):
        text = "link text"
        text_type = TextType.LINK
        url = "example.com"

        node = TextNode(text, text_type, url)

        result = text_node_to_html_node(node)

        self.assertEqual(isinstance(result, LeafNode), True)
        self.assertEqual(result.to_html(),
                         "<a href=\"example.com\">link text</a>")

    def test_image(self):
        text = "alt text"
        text_type = TextType.IMAGE
        url = "example.com/foo.png"

        node = TextNode(text, text_type, url)

        result = text_node_to_html_node(node)

        self.assertEqual(isinstance(result, LeafNode), True)
        self.assertEqual(result.to_html(),
                         "<img src=\"example.com/foo.png\" alt=\"alt text\"></img>")

if __name__ == "__main__":
    unittest.main()

