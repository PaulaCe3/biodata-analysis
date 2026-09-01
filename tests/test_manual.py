from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class ManualTests(unittest.TestCase):
    def test_spanish_manual_covers_workflow_metrics_and_privacy(self):
        content = (
            PROJECT_ROOT / "docs" / "MANUAL_DE_USO.md"
        ).read_text(encoding="utf-8")

        self.assertIn("## Recorrido rápido", content)
        self.assertIn("## 8. Cómo interpretar las métricas", content)
        self.assertIn("### Predecir una observación nueva", content)
        self.assertIn("## 12. Privacidad y límites", content)
        self.assertIn("## Glosario esencial", content)

    def test_english_manual_covers_workflow_metrics_and_privacy(self):
        content = (
            PROJECT_ROOT / "docs" / "USER_GUIDE.md"
        ).read_text(encoding="utf-8")

        self.assertIn("## Quick workflow", content)
        self.assertIn("## 8. Metrics", content)
        self.assertIn("### Predicting a new observation", content)
        self.assertIn("## 12. Privacy and limitations", content)
        self.assertIn("## Essential glossary", content)


if __name__ == "__main__":
    unittest.main()
