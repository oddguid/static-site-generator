import unittest
from htmlnode import HTMLNode

class TestTextNode(unittest.TestCase):
    def test_ctor_none(self):
        node = HTMLNode()

        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_ctor(self):
        tag = "<p>"
        value = "sample text"
        children = [ HTMLNode(tag), HTMLNode(tag, value) ]
        props = { "id": "foo", "name": "bar" }

        node = HTMLNode(tag, value, children, props)

        self.assertEqual(node.tag, tag)
        self.assertEqual(node.value, value)
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_props_to_html_empty(self):
        node = HTMLNode()

        result = node.props_to_html()

        self.assertEqual(result, "")

    def test_props_to_html_single(self):
        props = { "id": "foo" }

        node = HTMLNode(props = props)

        result = node.props_to_html()

        self.assertEqual(result, " id=\"foo\"")

    def test_props_to_html_multiple(self):
        props = { "id": "foo", "name": "bar" }

        node = HTMLNode(props = props)

        result = node.props_to_html()

        self.assertEqual(result, " id=\"foo\" name=\"bar\"")

