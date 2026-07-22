import unittest

from markdown_to_html import markdown_to_html_node

class MarkdownToHTMLNode(unittest.TestCase):
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_headings(self):
        md = """
# This is **bolded** heading text in a h1 tag here

## This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is <b>bolded</b> heading text in a h1 tag here</h1><h2>This is another paragraph with <i>italic</i> text and <code>code</code> here</h2></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second **item**
3. Third item

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second <b>item</b></li><li>Third item</li></ol></div>",
        )

    def test_unordered_list(self):
        md = """
- This is a list
- with items
- and _more_ items

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul></div>",
        )

    def test_code_block(self):
        md = """
```
def add(a, b):
    return a + b
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>def add(a, b):\n    return a + b\n</code></pre></div>",
        )
    def test_quote_block(self):
        md = """
> This is a quote
> with multiple lines
> and some _italic_ text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with multiple lines and some <i>italic</i> text</blockquote></div>",
        )
if __name__ == "__main__":
    unittest.main()