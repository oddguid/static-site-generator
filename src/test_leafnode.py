import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_ctor_none(self):
        node = LeafNode(None, None)

        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_ctor(self):
        tag = "<p>"
        value = "sample text"
        props = { "id": "foo", "name": "bar" }

        node = LeafNode(tag, value, props)

        self.assertEqual(node.tag, tag)
        self.assertEqual(node.value, value)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, props)

    def test_to_html_empty(self):
        node = LeafNode(None, None)

        self.assertRaises(ValueError, node.to_html)

    def test_to_html_raw(self):
        node = LeafNode(None, "simple text")

        result = node.to_html()

        self.assertEqual(result, "simple text")

    def test_to_html_paragraph(self):
        node = LeafNode("p", "This is a paragraph of text.")

        result = node.to_html()

        self.assertEqual(result, "<p>This is a paragraph of text.</p>")
    
    def test_to_html_link(self):
        node = LeafNode("a", "Click me!", { "href": "https://www.google.com"} )

        result = node.to_html()

        self.assertEqual(result, "<a href=\"https://www.google.com\">Click me!</a>")

    def test_repr(self):
        tag = "p"
        value = "sample text"
        props = { "id": "auto" }

        node = LeafNode(tag, value, props)

        result = node.__repr__()

        self.assertEqual(result,
                         "LeafNode(p, sample text, {'id': 'auto'})")

if __name__ == "__main__":
    unittest.main()

