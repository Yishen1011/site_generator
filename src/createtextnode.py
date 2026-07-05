from textnode import TextNode, TextType
import re

'''
node = TextNode("This is text with a `code block` word", TextType.TEXT)

new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

new_nodes = 
[
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),
]
'''

def split_nodes_delimiter(
    old_nodes: list[TextNode], 
    delimiter: str, 
    text_type: TextType) -> list[TextNode]:

    new_nodes = []
    boolean = False
    match text_type:
        case TextType.BOLD:
            if delimiter != "**":
                boolean = True
        case TextType.CODE:
            if delimiter != "`":
                boolean = True
        case TextType.ITALIC:
            if delimiter != "_":
                boolean = True
    
    if boolean:
        raise Exception(f'Delimiter "{delimiter}" does not match with "{text_type}" text type')

    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:

    new_nodes = []
    for old_node in old_nodes:

        # if not text type
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        # [("image", "https://i.imgur.com/zjjcJKZ.png"),("second image", "https://i.imgur.com/3elNhQu.png")]
        lst_of_images = extract_markdown_images(old_node.text)
        # Can't find images
        if len(lst_of_images) == 0:
            new_nodes.append(old_node)
            continue
        
        current_text = old_node.text
        # Split for every images
        split_nodes = []
        for image in lst_of_images:
            image_alt, image_link = image[0], image[1]
            sections = current_text.split(f"![{image_alt}]({image_link})", 1)

            # will have maximum 2 sections
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

            current_text = sections[1]

        if current_text != '':
            split_nodes.append(TextNode(current_text, TextType.TEXT))
        new_nodes.extend(split_nodes)

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:

        # if not text type
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # [("link", "https://boot.dev"),("another link", "https://wikipedia.org")]
        lst_of_links = extract_markdown_links(old_node.text)
        if len(lst_of_links) == 0:
            new_nodes.append(old_node)
            continue
        
        current_text = old_node.text
        # Split for every links
        split_nodes = []
        for link in lst_of_links:
            link_alt, link_link = link[0], link[1]
            sections = current_text.split(f"[{link_alt}]({link_link})", 1)

            # will have maximum 2 sections
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(link_alt, TextType.LINK, link_link))

            current_text = sections[1]
            
        if current_text != '':
            split_nodes.append(TextNode(current_text, TextType.TEXT))
        new_nodes.extend(split_nodes)

    return new_nodes

# This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)
def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    bold_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    code_nodes = split_nodes_delimiter(bold_nodes, "`", TextType.CODE)
    italic_nodes = split_nodes_delimiter(code_nodes, "_", TextType.ITALIC)
    image_nodes = split_nodes_image(italic_nodes)
    return split_nodes_link(image_nodes)