import unittest

from main import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = "# This is a heading h1"
        text = extract_title(md)
        self.assertEqual(text, "This is a heading h1")

    def test_extract_title_2(self):
        markdown = "# Mountain Journal"
        title = extract_title(markdown)
        assert title == "Mountain Journal"

    def test_h1_appear_after_lines(self):
        markdown = """yes this is true
# Mountain Journal"""
        title = extract_title(markdown)
        assert title == "Mountain Journal"

    def test_h1_appear_after_h2(self):
        markdown = """## yes this is true 
# Mountain Journal"""
        title = extract_title(markdown)
        assert title == "Mountain Journal"

    def test_no_h1_exists(self):
        markdown = "yes this is true Mountain Journal"

        with self.assertRaises(Exception):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()