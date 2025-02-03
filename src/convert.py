import re
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, { "href": text_node.url })
        case TextType.IMAGE:
            return LeafNode("img", "", { "src": text_node.url, "alt": text_node.text })
        case _:
            raise Exception("Invalid HTML: text type invalid")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue

        split_nodes = []
        parts = old_node.text.split(delimiter)

        if len(parts) % 2 == 0:
            # no closing delimiter
            raise Exception("Invalid Markdown: no closing delimiter found")

        for i in range(len(parts)):
            if parts[i] == "":
                # skip empty parts
                continue

            if i % 2 == 0:
                # normal text section
                split_nodes.append(TextNode(parts[i], TextType.NORMAL))
            else:
                split_nodes.append(TextNode(parts[i], text_type))

        new_nodes.extend(split_nodes)

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)

        if len(images) == 0:
            # no images
            new_nodes.append(old_node)
            continue

        original_text = old_node.text

        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)

            if len(sections) != 2:
                raise Exception("Invalid Markdown: image section no closed")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))

            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)

        if len(links) == 0:
            # no links
            new_nodes.append(old_node)
            continue

        original_text = old_node.text

        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)

            if len(sections) != 2:
                raise Exception("Invalid Markdown: link section not closed")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))

            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL))

    return new_nodes
