import ast
from pathlib import Path
import unittest

from src.i18n import ENGLISH


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class TranslationTests(unittest.TestCase):
    def test_literal_interface_texts_have_an_english_translation(self):
        tree = ast.parse(
            (PROJECT_ROOT / "app.py").read_text(encoding="utf-8")
        )
        literal_keys = {
            node.args[0].value
            for node in ast.walk(tree)
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "tr"
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)
            )
        }

        missing = sorted(literal_keys.difference(ENGLISH))
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
