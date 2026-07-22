import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p_props(self):
        node = LeafNode("p", "Hello, world!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<p href="https://www.google.com">Hello, world!</p>')
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_error_to_html(self):
        node = LeafNode("h1", None)
        with self.assertRaises(ValueError):
            node.to_html()

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_error_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_error_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

if __name__ == "__main__":
    unittest.main()