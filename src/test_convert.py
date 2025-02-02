import unittest
from convert import text_node_to_html_node, split_nodes_delimiter
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

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is **bolded** text", TextType.NORMAL)

        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertListEqual(result,
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("bolded", TextType.BOLD),
                TextNode(" text", TextType.NORMAL)
            ])

    def test_split_nodes_delimiter_bold_double(self):
        node = TextNode("Some **bolded** text with **another**", TextType.NORMAL)

        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertListEqual(result,
            [
                TextNode("Some ", TextType.NORMAL),
                TextNode("bolded", TextType.BOLD),
                TextNode(" text with ", TextType.NORMAL),
                TextNode("another", TextType.BOLD)
            ])

    def test_split_nodes_delimiter_bold_multiword(self):
        node = TextNode("Some text with **bolded words**", TextType.NORMAL)

        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertListEqual(result,
            [
                TextNode("Some text with ", TextType.NORMAL),
                TextNode("bolded words", TextType.BOLD)
            ])

    def test_split_nodes_delimiter_italic_multiword(self):
        node = TextNode("Some text with *italic words*", TextType.NORMAL)

        result = split_nodes_delimiter([node], "*", TextType.ITALIC)

        self.assertListEqual(result,
            [
                TextNode("Some text with ", TextType.NORMAL),
                TextNode("italic words", TextType.ITALIC)
            ])

    def test_split_nodes_delimiter_bold_and_italic(self):
        node = TextNode("Some text with **bolded words** and *italic* word", TextType.NORMAL)

        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        result = split_nodes_delimiter(result, "*", TextType.ITALIC)

        self.assertListEqual(result,
            [
                TextNode("Some text with ", TextType.NORMAL),
                TextNode("bolded words", TextType.BOLD),
                TextNode(" and ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.NORMAL)
            ])


    def test_split_nodes_delimiter_code(self):
        node = TextNode("Some text with `code block`", TextType.NORMAL)

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertListEqual(result,
            [
                TextNode("Some text with ", TextType.NORMAL),
                TextNode("code block", TextType.CODE)
            ])

if __name__ == "__main__":
    unittest.main()

