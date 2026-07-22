from blocktype import BlockType, block_to_block_type, markdown_to_blocks
from htmlnode import ParentNode
from delimiter import text_to_textnodes
from textnode import TextType, TextNode, text_node_to_html_node

def markdown_to_html_node(markdown):
    '''
    converts full markdown document into a single parent HTMLNode
    One parent HTMLNode should have multiple child HTMLNode
    '''
    children_of_div = []
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            number_of_hashtag = count_hashtags(block)
            hashtags = "#" * number_of_hashtag
            removed_hashtags = block.lstrip(hashtags + " ")
            children = text_to_children(removed_hashtags)
            children_of_div.append(ParentNode("h"+str(number_of_hashtag), children))
        elif block_type == BlockType.CODE:
            code = block.lstrip("```\n").rstrip("```")
            textnode = TextNode(code, TextType.CODE)
            leafnode = text_node_to_html_node(textnode)
            children_of_div.append(ParentNode("pre", [leafnode]))
        elif block_type == BlockType.QUOTE:
            block_quote = block.replace("\n", " ").replace("> ", "")
            children = text_to_children(block_quote)
            children_of_div.append(ParentNode("blockquote", children))
        elif block_type == BlockType.UNORDERED_LIST:
            children = unordered_html_list(block)
            children_of_div.append(ParentNode("ul", children))
        elif block_type == BlockType.ORDERED_LIST:
            children = ordered_html_list(block)
            children_of_div.append(ParentNode("ol", children))
        else: # BlockType.PARAGRAPH
           block_space = block.replace("\n", " ")
           children = text_to_children(block_space)
           children_of_div.append(ParentNode("p", children))
    
    parent_div = ParentNode("div", children_of_div)
    return parent_div


# Helper functions
def text_to_children(text):
    list_text_nodes = text_to_textnodes(text)
    list_html_nodes = []

    for text_nodes in list_text_nodes:
        html_node = text_node_to_html_node(text_nodes)
        list_html_nodes.append(html_node)

    return list_html_nodes

def count_hashtags(text):
    count = 0
    boolean = True
    iter = 0
    while boolean:
        if text[iter] == '#' and iter < 6:
            count += 1
            iter += 1
        else:
            boolean = False
    
    return count

def unordered_html_list(text):
    children_of_list = []
    lsts = text.replace("\n", "").split("- ")

    for lst in lsts:
        if lst == "":
            continue
        children = text_to_children(lst)
        children_of_list.append(ParentNode("li", children))
    return children_of_list

def ordered_html_list(text):
    children_of_list = []
    lsts = text.split("\n")

    for string in lsts:
        if string == "":
            continue
        # Split out the number
        _, second = string.split(". ", 1)
        children = text_to_children(second)
        children_of_list.append(ParentNode("li", children))
    return children_of_list
    