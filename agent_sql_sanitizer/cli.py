"""Command-line interface for Agent SQL Sanitizer."""
import argparse
from .sanitizer import SQLSanitizer

def main():
    parser = argparse.ArgumentParser(description="Agent SQL Sanitizer CLI")
    parser.add_argument("--demo", action="store_true", help="Demonstrate SQL query sanitization")
    args = parser.parse_args()

    safe_q = "SELECT id, name FROM users WHERE active = 1"
    ok1, msg1 = SQLSanitizer.sanitize(safe_q)
    print(f"Query: '{safe_q}' -> Safe: {ok1} ({msg1})")

    dangerous_q = "SELECT * FROM users; DROP TABLE orders;"
    ok2, msg2 = SQLSanitizer.sanitize(dangerous_q)
    print(f"Query: '{dangerous_q}' -> Safe: {ok2} ({msg2})")

if __name__ == "__main__":
    main()
