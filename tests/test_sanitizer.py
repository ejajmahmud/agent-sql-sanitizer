"""Unit tests for SQLSanitizer."""
import unittest
from agent_sql_sanitizer.sanitizer import SQLSanitizer

class TestSQLSanitizer(unittest.TestCase):
    def test_clean_select(self):
        ok, _ = SQLSanitizer.sanitize("SELECT id, email FROM customers WHERE active = 1")
        self.assertTrue(ok)

    def test_block_drop(self):
        ok, msg = SQLSanitizer.sanitize("DROP TABLE accounts")
        self.assertFalse(ok)
        self.assertIn("Forbidden SQL operation", msg)

    def test_block_chaining(self):
        ok, msg = SQLSanitizer.sanitize("SELECT * FROM items; DELETE FROM items;")
        self.assertFalse(ok)
        self.assertIn("Multiple SQL statements", msg)

    def test_block_metadata_table(self):
        ok, msg = SQLSanitizer.sanitize("SELECT * FROM information_schema.tables")
        self.assertFalse(ok)
        self.assertIn("metadata table", msg)

    def test_block_comments(self):
        ok, msg = SQLSanitizer.sanitize("SELECT * FROM users -- bypass auth")
        self.assertFalse(ok)
        self.assertIn("comments", msg)

if __name__ == "__main__":
    unittest.main()
