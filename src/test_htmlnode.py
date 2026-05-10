import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq_without_children(self):
        eq_string = ' class="greeting" href="https://boot.dev"'
        node = HTMLNode("p", 
                        "This is a paragraph", 
                        None, 
                        {"class": "greeting", "href": "https://boot.dev"})
        self.assertEqual(node.props_to_html(), eq_string)

    def test_eq_with_children(self):
        eq_string = "HTMLNode(p, This is a paragraph, children: [HTMLNode(a, I am a child, children: None, None)], None)"
        child = HTMLNode("a", "I am a child")
        node = HTMLNode("p", "This is a paragraph", [child], None)
        self.assertEqual(str(node), eq_string)

    def test_eq_val(self):
        node = HTMLNode("p", "This is a paragraph")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "This is a paragraph")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
    
    def test_error_to_html(self):
        node = HTMLNode("h1", "This is a header")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html_empty(self):
        node = HTMLNode("h1", "This is a header")
        self.assertEqual(node.props_to_html(), "")

if __name__ == "__main__":
    unittest.main()