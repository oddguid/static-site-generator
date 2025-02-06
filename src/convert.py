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

def text_to_textnodes(text):
    nodes = [ TextNode(text, TextType.NORMAL) ]

    # bold before italic!
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def markdown_to_blocks(markdown):
    blocks = []
    current_block = []

    lines = markdown.split("\n")

    for line in lines:
        if len(line) == 0:
            if len(current_block) > 0:
                blocks.append("\n".join(current_block))
                current_block = []
        else:
            current_block.append(line.strip())

    if len(current_block) > 0:
        blocks.append("\n".join(current_block))

    return blocks

def block_to_block_type(block_text):
    # heading
    if re.match(r'^[#]{1,6} .*', block_text):
        return "heading"

    # code
    if block_text.startswith("```") and block_text.endswith("```"):
        return "code"

    # lists or quote
    lines = block_text.split("\n")
    quote_count = 0
    unordered_list_count = 0
    ordered_list_count = 1

    for line in lines:
        if line.startswith(">"):
            quote_count += 1

        if re.match(r'^[*-] .*', line):
            unordered_list_count +=1

        if line.startswith(f"{ordered_list_count}. "):
            ordered_list_count += 1

    if len(lines) == quote_count:
        return "quote"

    if len(lines) == unordered_list_count:
        return "unordered_list"

    if len(lines) == ordered_list_count - 1:
        return "ordered_list"

    return "paragraph"

def markdown_to_html_node(markdown):
    # split text into blocks
    markdown_blocks = markdown_to_blocks(markdown)

    children = []

    for markdown_block in markdown_blocks:
        block_type = block_to_block_type(markdown_block)

        match (block_type):
            case "heading":
                children.append(heading_to_html_node(markdown_block))
            case "code":
                children.append(code_to_html_node(markdown_block))
            case "quote":
                children.append(quote_block_to_html_node(markdown_block))
            case "unordered_list":
                children.append(unordered_list_to_html_node(markdown_block))
            case "ordered_list":
                children.append(ordered_list_to_html_node(markdown_block))
            case "paragraph":
                children.append(paragraph_to_html_node(markdown_block))
            case _:
                raise Exception("Invalid HTML: text type invalid")

    return ParentNode("div", children)

def text_to_children(text):
    # convert to text nodes
    text_nodes = text_to_textnodes(text)

    # convert to html nodes
    html_nodes = []

    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)

    return html_nodes

def quote_block_to_html_node(block):
    # split into lines
    lines = block.split("\n")

    # remove > from lines
    content = []

    for line in lines:
        content.append(line[1:].strip())

    children = text_to_children("\n".join(content))

    return ParentNode("blockquote", children)

def unordered_list_to_html_node(block):
    # split into lines
    lines = block.split("\n")

    # replace */- with <li>
    item_list = []

    for line in lines:
        children = text_to_children(line[2:])
        item_list.append(ParentNode("li", children))

    return ParentNode("ul", item_list)

def ordered_list_to_html_node(block):
    # split into lines
    lines = block.split("\n")

    # replace number with <li>
    item_list = []

    for line in lines:
        children = text_to_children(line[line.index(". ") + 2:])
        item_list.append(ParentNode("li", children))

    return ParentNode("ol", item_list)

def code_to_html_node(block):
    # strip ````
    content = block.replace("```", "")

    children = text_to_children(content)
    code = ParentNode("code", children)

    return ParentNode("pre", [code])

def heading_to_html_node(block):
    # index of first space is equal to number of #
    index = block.index(" ")

    text = block[index + 1:]
    children = text_to_children(text)

    return ParentNode(f"h{index}", children)

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)

    return ParentNode("p", children)
