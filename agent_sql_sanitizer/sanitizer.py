"""Strict AST and lexical validator for agent-generated SQL queries."""
import re
from typing import Tuple, List

BLOCKED_KEYWORDS = {"DROP", "TRUNCATE", "ALTER", "DELETE", "UPDATE", "INSERT", "GRANT", "REVOKE", "EXEC", "EXECUTE"}
BLOCKED_TABLES = {"INFORMATION_SCHEMA", "PG_SHADOW", "PG_AUTHID", "SQLITE_MASTER", "MYSQL.USER", "SYS.TABLES"}


class SQLSanitizer:
    @staticmethod
    def sanitize(query: str, allowed_verbs: List[str] = None) -> Tuple[bool, str]:
        if allowed_verbs is None:
            allowed_verbs = ["SELECT"]

        cleaned = query.strip()
        # Check for comment injections
        if "--" in cleaned or "/*" in cleaned or "*/" in cleaned:
            return False, "SQL comments ('--' or '/*') are forbidden"

        # Check for statement chaining
        statements = [s.strip() for s in cleaned.split(";") if s.strip()]
        if len(statements) > 1:
            return False, "Multiple SQL statements chained with ';' are forbidden"
        if not statements:
            return False, "Empty query"

        single_query = statements[0]
        tokens = re.findall(r"[a-zA-Z0-9_]+", single_query)
        if not tokens:
            return False, "No valid SQL tokens found"

        first_verb = tokens[0].upper()
        if first_verb not in [v.upper() for v in allowed_verbs]:
            return False, f"Forbidden SQL operation '{first_verb}'. Allowed: {allowed_verbs}"

        # Check forbidden keywords anywhere in query
        upper_tokens = [t.upper() for t in tokens]
        for kw in BLOCKED_KEYWORDS:
            if kw in upper_tokens and kw not in allowed_verbs:
                return False, f"Forbidden keyword detected in query: '{kw}'"

        # Check blocked system tables
        for table in BLOCKED_TABLES:
            if table in upper_tokens:
                return False, f"Access to administrative metadata table '{table}' is blocked"

        return True, "Safe"
