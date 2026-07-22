from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    first = block[0]
    if first == "#":
        if re.search(r"^[#]{1,6} (.*)", block):
            return BlockType.HEADING
    elif first == "`":
        if re.search(r"^```(\n+)([\s\S]*)(\n*?)```$", block):
        # if re.search(r"^[`]{3,3}(\n*)(.*)(\n*?)[`]{3,3}$", block):
            return BlockType.CODE
    elif first == ">":
        lines = block.split("\n")
        if check_each_lines(lines, r"^[>]( ?).*"):
            return BlockType.QUOTE
    elif first == "-":
        lines = block.split("\n")
        if check_each_lines(lines, r"^[-]( )(.*)"):
            return BlockType.UNORDERED_LIST
    elif first == "1":
        lines = block.split("\n")
        if check_each_lines(lines, r"^(\d+)\.\ (.*)", True):
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def check_each_lines(lines, regex, ordered=False):
    count = 1
    boolean = True
    for line in lines:
        if ordered:
            match = re.match(r'^\d+', line)
            if match:
                if match.group() != str(count):
                    boolean = False
                    break
            else:
                boolean = False
                break 
            count += 1
        if not re.search(regex, line):
            boolean = False

    return boolean