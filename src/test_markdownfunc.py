import unittest

from markdownfunc import *

class TestMarkdownBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        block = "#### 4 headings"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_not_heading(self):
        block = "####### 7 headings"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_heading_no_space(self):
        block = "######yes"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_heading_only_hashtag(self):
        block = "#"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)


    def test_code(self):
            block = "```\nit works```"
            block_type = block_to_block_type(block)
            self.assertEqual(block_type, BlockType.CODE)

    def test_code_multi_line(self):
            block = "```\nyes\nit works```"
            block_type = block_to_block_type(block)
            self.assertEqual(block_type, BlockType.CODE)

    def test_not_code(self):
            block = "``\ndoesn't work``"
            block_type = block_to_block_type(block)
            self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_code_empty(self):
            block = "``````"
            block_type = block_to_block_type(block)
            self.assertEqual(block_type, BlockType.PARAGRAPH)


    def test_quote_single_line(self):
            block = "> first quote"
            block_type = block_to_block_type(block)
            self.assertEqual(block_type, BlockType.QUOTE)

    def test_quote_multi_line(self):
            block = "> first quote\n>second quote"
            block_type = block_to_block_type(block)
            self.assertEqual(block_type, BlockType.QUOTE)

    def test_not_quote_multi_line(self):
            block = "> first quote\nsecond quote"
            block_type = block_to_block_type(block)
            self.assertEqual(block_type, BlockType.PARAGRAPH)


    def test_unordered_list_single_line(self):
        block = "- This is a list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
    
    def test_unordered_list_multi_line(self):
        block = "- This is a list\n- with items"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
    
    def test_not_unordered_list(self):
        block = "-This is a list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    def test_not_unordered_list_multi_lines(self):
        block = "-This is a list\n- with items\n- yes\n-no"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    

    def test_ordered_list(self):
        block = "1. This is a list\n2. with items"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_not_ordered_list(self):
        block = "1. This is a list\n3. with items"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_not_ordered_list_starting_with_2(self):
        block = "2. This is a list\n3. with items"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()