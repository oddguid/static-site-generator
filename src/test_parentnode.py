import unittest
from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    def test_ctor_none(self):
        node = ParentNode(None, None)

        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_ctor(self):
        tag = "p"
        children = [ ParentNode(None, None) ]
        props = { "id": "foo", "name": "bar" }

        node = ParentNode(tag, children, props)

        self.assertEqual(node.tag, tag)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_to_html_empty(self):
        node = ParentNode(None, None)

        self.assertRaises(ValueError, node.to_html)

    def test_to_html_tag_empty(self):
        node = ParentNode(None, [ ParentNode(None, None) ])

        self.assertRaises(ValueError, node.to_html)

    def test_to_html_children_empty(self):
        node = ParentNode("p", None)

        self.assertRaises(ValueError, node.to_html)

    def test_to_html_children_single(self):
        tag = "p"
        children = [ LeafNode("b", "bold text") ]

        node = ParentNode(tag, children)

        result = node.to_html()

        self.assertEqual(result, "<p><b>bold text</b></p>")

    def test_to_html_children_multiple(self):
        tag = "p"
        children = [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text")
            ]

        node = ParentNode(tag, children)

        result = node.to_html()

        self.assertEqual(result, "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_children_parent(self):
        tag = "p"
        children = [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text")
            ]
        props = { "id": "foo" }

        child_node = ParentNode(tag, children)

        node = ParentNode(tag, [child_node], props)

        result = node.to_html()

        self.assertEqual(result, "<p id=\"foo\"><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p>")


    def test_repr(self):
        tag = "p"
        children = [ LeafNode(None, None) ]
        props = { "id": "auto" }

        node = ParentNode(tag, children, props)

        result = node.__repr__()

        self.assertEqual(result,
                         "ParentNode(p, [LeafNode(None, None, None)], {'id': 'auto'})")

if __name__ == "__main__":
    unittest.main()

