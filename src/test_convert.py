import unittest
from convert import (
        text_node_to_html_node,
        split_nodes_delimiter,
        extract_markdown_images,
        extract_markdown_links,
        split_nodes_image,
        split_nodes_link,
        text_to_textnodes,
        markdown_to_blocks,
        block_to_block_type,
        text_to_children,
        quote_block_to_html_node,
        unordered_list_to_html_node,
        ordered_list_to_html_node,
        code_to_html_node,
        heading_to_html_node,
        paragraph_to_html_node,
        markdown_to_html_node
    )
from leafnode import LeafNode
from parentnode import ParentNode
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

    def test_markdown_to_blocks(self):
        text = """
  # This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.




* This is the first list item in a list block
* This is a list item
* This is another list item
        """

        result = markdown_to_blocks(text)

        self.assertListEqual(result,
            [
                '# This is a heading',
                'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
                '* This is the first list item in a list block\n* This is a list item\n* This is another list item\n'
            ])

    def test_block_to_block_type_empty(self):
        text = ""

        result = block_to_block_type(text)

        self.assertEqual(result, "paragraph")

    def test_block_to_block_type_paragraph(self):
        text = "sample text"

        result = block_to_block_type(text)

        self.assertEqual(result, "paragraph")

    def test_block_to_block_type_heading(self):
        text1 = "# heading 1"
        text2 = "## heading 2"
        text3 = "### heading 3"
        text4 = "#### heading 4"
        text5 = "##### heading 5"
        text6 = "###### heading 6"

        result = block_to_block_type(text1)

        self.assertEqual(result, "heading")

        result = block_to_block_type(text2)

        self.assertEqual(result, "heading")

        result = block_to_block_type(text3)

        self.assertEqual(result, "heading")

        result = block_to_block_type(text4)

        self.assertEqual(result, "heading")

        result = block_to_block_type(text5)

        self.assertEqual(result, "heading")

        result = block_to_block_type(text6)

        self.assertEqual(result, "heading")

    def test_block_to_block_type_heading_too_long(self):
        text = "####### heading 7"

        result = block_to_block_type(text)

        self.assertEqual(result, "paragraph")

    def test_block_to_block_type_code(self):
        text = """```
int main() {
  return 0;
}
```"""

        result = block_to_block_type(text)

        self.assertEqual(result, "code")

    def test_block_to_block_type_almost_code(self):
        text = """```
int main() {
  return 0;
}`"""

        result = block_to_block_type(text)

        self.assertEqual(result, "paragraph")

    def test_block_to_block_type_quote(self):
        text = """>quote
>quote
>quote"""

        result = block_to_block_type(text)

        self.assertEqual(result, "quote")

    def test_block_to_block_type_almost_quote(self):
        text = """>quote
>quote
quote"""

        result = block_to_block_type(text)

        self.assertEqual(result, "paragraph")

    def test_block_to_block_type_unordered_list(self):
        text = """* item
- foo
* bar"""

        result = block_to_block_type(text)

        self.assertEqual(result, "unordered_list")


    def test_block_to_block_type_almost_unordered_list(self):
        text = """* item
foo
* bar"""

        result = block_to_block_type(text)

        self.assertEqual(result, "paragraph")

    def test_block_to_block_type_ordered_list(self):
        text = """1. item
2. foo
3. bar
4. fizz
5. buzz
6. fizzbuzz
7. oof
8. rab
9. zzif
10. zzub"""

        result = block_to_block_type(text)

        self.assertEqual(result, "ordered_list")

    def test_block_to_block_type_almost_ordered_list(self):
        text = """1. item
2. foo
3. bar
4. fizz
5. buzz
6. fizzbuzz
oof
rab
7. zzif
8. zzub"""

        result = block_to_block_type(text)

        self.assertEqual(result, "paragraph")

    def test_block_to_block_type_ordered_list_count_wrong(self):
        text = """1. item
2. foo
3. bar
4. fizz
5. buzz
6. fizzbuzz
10. oof
11. rab
12. zzif
13. zzub"""

        result = block_to_block_type(text)

        self.assertEqual(result, "paragraph")

    def test_text_to_children_normal(self):
        text = "sample text"

        result = text_to_children(text)

        self.assertEqual(len(result), 1)

        self.assertEqual(isinstance(result[0], LeafNode), True)
        self.assertEqual(result[0].to_html(),
            "sample text")

    def test_text_to_children_mix(self):
        text = """sample **bold** text
with a bit *italic*, some `code`, an
image ![alt img](foo.gif) and a
[link](example.com)"""

        result = text_to_children(text)

        self.assertEqual(len(result), 10)

        # normal
        self.assertEqual(isinstance(result[0], LeafNode), True)
        self.assertEqual(result[0].to_html(), "sample ")

        # bold
        self.assertEqual(isinstance(result[1], LeafNode), True)
        self.assertEqual(result[1].to_html(), "<b>bold</b>")

        # normal
        self.assertEqual(isinstance(result[2], LeafNode), True)
        self.assertEqual(result[2].to_html(), " text\nwith a bit ")

        # italic
        self.assertEqual(isinstance(result[3], LeafNode), True)
        self.assertEqual(result[3].to_html(), "<i>italic</i>")

        # normal
        self.assertEqual(isinstance(result[4], LeafNode), True)
        self.assertEqual(result[4].to_html(), ", some ")

        # code
        self.assertEqual(isinstance(result[5], LeafNode), True)
        self.assertEqual(result[5].to_html(), "<code>code</code>")

        # normal
        self.assertEqual(isinstance(result[6], LeafNode), True)
        self.assertEqual(result[6].to_html(), ", an\nimage ")

        # image
        self.assertEqual(isinstance(result[7], LeafNode), True)
        self.assertEqual(result[7].to_html(),
            "<img src=\"foo.gif\" alt=\"alt img\"></img>")

        # normal
        self.assertEqual(isinstance(result[8], LeafNode), True)
        self.assertEqual(result[8].to_html(), " and a\n")

        # link
        self.assertEqual(isinstance(result[9], LeafNode), True)
        self.assertEqual(result[9].to_html(),
            "<a href=\"example.com\">link</a>")

    def test_quote_block_to_html_node(self):
        text = """>quote
>foo
>bar"""

        result = quote_block_to_html_node(text)

        self.assertEqual(isinstance(result, ParentNode), True)
        self.assertEqual(result.to_html(),
            "<blockquote>quote\nfoo\nbar</blockquote>")

    def test_unordered_list_to_html_node(self):
        text = """* item
- foo
* bar"""

        result = unordered_list_to_html_node(text)

        self.assertEqual(isinstance(result, ParentNode), True)
        self.assertEqual(result.to_html(),
            "<ul><li>item</li><li>foo</li><li>bar</li></ul>")

    def test_unordered_list_to_html_node(self):
        text = """1. item
2. foo
3. bar
4. fizz
5. buzz
6. fizzbuzz
7. oof
8. rab
9. zzif
10. zzub"""

        result = ordered_list_to_html_node(text)

        self.assertEqual(isinstance(result, ParentNode), True)
        self.assertEqual(result.to_html(),
            "<ol><li>item</li><li>foo</li><li>bar</li>\
<li>fizz</li><li>buzz</li><li>fizzbuzz</li><li>oof</li>\
<li>rab</li><li>zzif</li><li>zzub</li></ol>")

    def test_code_to_html_node(self):
        text = """```
int main() {
  return 0;
}
```"""
        result = code_to_html_node(text)

        self.assertEqual(isinstance(result, ParentNode), True)
        self.assertEqual(result.to_html(),
            "<pre><code>\nint main() {\n  return 0;\n}\n</code></pre>")

    def test_heading_to_html_node(self):
        text = "### heading"

        result = heading_to_html_node(text)

        self.assertEqual(isinstance(result, ParentNode), True)
        self.assertEqual(result.to_html(),
            "<h3>heading</h3>")

    def test_paragraph_to_html_node(self):
        text = "sample text with **bold**"

        result = paragraph_to_html_node(text)

        self.assertEqual(isinstance(result, ParentNode), True)
        self.assertEqual(result.to_html(),
            "<p>sample text with <b>bold</b></p>")

    def test_markdown_to_html_node(self):
        text = """### heading

Sample text with **bold** and *italic* and `code`
and an image ![alt](foo.png) and a [link](example.com)

>quote
>...
>end

```
int main() {
  return 0;
}
```

* foo
* bar

1. fizz
2. buzz
3. fizzbuzz"""

        result = markdown_to_html_node(text)

        self.assertEqual(isinstance(result, ParentNode), True)
        self.assertEqual(result.to_html(),
            "<div>\
<h3>heading</h3>\
<p>Sample text with <b>bold</b> and <i>italic</i> and <code>code</code> \
and an image <img src=\"foo.png\" alt=\"alt\"></img>\
 and a <a href=\"example.com\">link</a></p>\
<blockquote>quote\n...\nend</blockquote>\
<pre><code>\nint main() {\nreturn 0;\n}\n</code></pre>\
<ul><li>foo</li><li>bar</li></ul>\
<ol><li>fizz</li><li>buzz</li><li>fizzbuzz</li></ol>\
</div>")

if __name__ == "__main__":
    unittest.main()

