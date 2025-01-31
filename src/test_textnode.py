import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_ctor_no_url(self):
        text = "This is a text node"
        text_type = TextType.CODE

        node = TextNode(text, text_type)

        self.assertEqual(node.text, text)
        self.assertEqual(node.text_type, text_type)
        self.assertEqual(node.url, None)

    def test_ctor_url(self):
        text = "This is a text node"
        text_type = TextType.CODE
        url = "https://example.com"

        node = TextNode(text, text_type, url)

        self.assertEqual(node.text, text)
        self.assertEqual(node.text_type, text_type)
        self.assertEqual(node.url, url)

    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        
        self.assertEqual(node1, node2)

    def test_eq_text_diff(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("__DIFF__", TextType.BOLD)
        
        self.assertNotEqual(node1, node2)

    def test_eq_texttype_diff(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.NORMAL)
        
        self.assertNotEqual(node1, node2)

    def test_eq_url_diff(self):
        node1 = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.CODE, "example.com")
        node3 = TextNode("This is a text node", TextType.CODE, "foo.com")
        
        self.assertNotEqual(node1, node2)
        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node2, node3)

    def test_repr(self):
        text = "sample text"
        text_type = TextType.ITALIC
        url = "http://example.com"

        node = TextNode(text, text_type, url)

        result = node.__repr__()

        self.assertEqual(result,
                         "TextNode(sample text, italic, http://example.com)")

if __name__ == "__main__":
    unittest.main()
