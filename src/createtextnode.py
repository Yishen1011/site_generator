from textnode import TextNode, TextType


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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
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
        print(sections)
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
        
        
