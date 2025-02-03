import unittest
from convert import (
        text_node_to_html_node,
        split_nodes_delimiter,
        extract_markdown_images,
        extract_markdown_links,
        split_nodes_image,
        split_nodes_link,
        text_to_textnodes
    )
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

    def test_extract_markdown_images_none(self):
        text = "this is text without images"

        result = extract_markdown_images(text)

        self.assertEqual(len(result), 0)

    def test_extract_markdown_images_single(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"

        result = extract_markdown_images(text)

        self.assertListEqual(result,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif")
            ])

    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

        result = extract_markdown_images(text)

        self.assertListEqual(result,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ])

    def test_extract_markdown_images_not_image(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif)"

        result = extract_markdown_images(text)

        self.assertEqual(len(result), 0)

    def test_extract_markdown_links_none(self):
        text = "sample text, no link"

        result = extract_markdown_links(text)

        self.assertEqual(len(result), 0)

    def test_extract_markdown_links_single(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"

        result = extract_markdown_links(text)

        self.assertListEqual(result,
            [
                ("to boot dev", "https://www.boot.dev")
            ])

    def test_extract_markdown_links_multiple(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

        result = extract_markdown_links(text)

        self.assertListEqual(result,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ])

    def test_extract_markdown_links_not_link(self):
        text = "This is text with a link ![to boot dev](https://www.boot.dev)"

        result = extract_markdown_links(text)

        self.assertEqual(len(result), 0)

    def test_split_nodes_image_no_image(self):
        node = TextNode("sample text", TextType.NORMAL)

        result = split_nodes_image([node])

        self.assertListEqual(result,
            [
                TextNode("sample text", TextType.NORMAL)
            ])

    def test_split_nodes_image_single(self):
        node1 = TextNode("sample ![alt text](image.gif) image", TextType.NORMAL)
        node2 = TextNode("simple bold", TextType.BOLD)

        result = split_nodes_image([node1, node2])

        self.assertListEqual(result,
            [
                TextNode("sample ", TextType.NORMAL),
                TextNode("alt text", TextType.IMAGE, "image.gif"),
                TextNode(" image", TextType.NORMAL),
                TextNode("simple bold", TextType.BOLD)
            ])

    def test_split_nodes_image_single_start(self):
        node1 = TextNode("![alt text](image.gif) image", TextType.NORMAL)
        node2 = TextNode("simple bold", TextType.BOLD)

        result = split_nodes_image([node1, node2])

        self.assertListEqual(result,
            [
                TextNode("alt text", TextType.IMAGE, "image.gif"),
                TextNode(" image", TextType.NORMAL),
                TextNode("simple bold", TextType.BOLD)
            ])

    def test_split_nodes_image_single_end(self):
        node1 = TextNode("sample ![alt text](image.gif)", TextType.NORMAL)
        node2 = TextNode("simple bold", TextType.BOLD)

        result = split_nodes_image([node1, node2])

        self.assertListEqual(result,
            [
                TextNode("sample ", TextType.NORMAL),
                TextNode("alt text", TextType.IMAGE, "image.gif"),
                TextNode("simple bold", TextType.BOLD)
            ])

    def test_split_nodes_image_multiple(self):
        node1 = TextNode("sample ![alt text](image.gif) ![text alt](pic.png)", TextType.NORMAL)
        node2 = TextNode("simple bold", TextType.BOLD)

        result = split_nodes_image([node1, node2])

        self.assertListEqual(result,
            [
                TextNode("sample ", TextType.NORMAL),
                TextNode("alt text", TextType.IMAGE, "image.gif"),
                TextNode(" ", TextType.NORMAL),
                TextNode("text alt", TextType.IMAGE, "pic.png"),
                TextNode("simple bold", TextType.BOLD)
            ])

    def test_split_nodes_link_no_link(self):
        node = TextNode("sample text", TextType.NORMAL)

        result = split_nodes_link([node])

        self.assertListEqual(result,
            [
                TextNode("sample text", TextType.NORMAL)
            ])

    def test_split_nodes_link_single(self):
        node1 = TextNode("sample [link](example.com) image", TextType.NORMAL)
        node2 = TextNode("simple bold", TextType.BOLD)

        result = split_nodes_link([node1, node2])

        self.assertListEqual(result,
            [
                TextNode("sample ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "example.com"),
                TextNode(" image", TextType.NORMAL),
                TextNode("simple bold", TextType.BOLD)
            ])

    def test_split_nodes_link_single_start(self):
        node1 = TextNode("[link](example.com) image", TextType.NORMAL)
        node2 = TextNode("simple bold", TextType.BOLD)

        result = split_nodes_link([node1, node2])

        self.assertListEqual(result,
            [
                TextNode("link", TextType.LINK, "example.com"),
                TextNode(" image", TextType.NORMAL),
                TextNode("simple bold", TextType.BOLD)
            ])

    def test_split_nodes_link_single_end(self):
        node1 = TextNode("sample [link](example.com)", TextType.NORMAL)
        node2 = TextNode("simple bold", TextType.BOLD)

        result = split_nodes_link([node1, node2])

        self.assertListEqual(result,
            [
                TextNode("sample ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "example.com"),
                TextNode("simple bold", TextType.BOLD)
            ])

    def test_split_nodes_link_multiple(self):
        node1 = TextNode("sample [link](example.com) [zelda](w3.org)", TextType.NORMAL)
        node2 = TextNode("simple bold", TextType.BOLD)

        result = split_nodes_link([node1, node2])

        self.assertListEqual(result,
            [
                TextNode("sample ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "example.com"),
                TextNode(" ", TextType.NORMAL),
                TextNode("zelda", TextType.LINK, "w3.org"),
                TextNode("simple bold", TextType.BOLD)
            ])

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        result = text_to_textnodes(text)

        self.assertListEqual(result,
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ])


if __name__ == "__main__":
    unittest.main()

