import unittest

from src.report import build_full_report


class ReportTests(unittest.TestCase):
    def build_report(self, language="es"):
        return build_full_report(
            dataset_profile={
                "n_rows": 100,
                "n_columns": 3,
                "columns": ["x", "group", "target"]
            },
            quality_report={
                "missing_values": {"x": 0, "group": 0, "target": 0},
                "duplicate_rows": 0
            },
            model_comparison={
                "Dummy": {"mean_mae": 2.0},
                "Gradient Boosting": {"mean_mae": 1.0}
            },
            evaluation_summary={
                "mae": 1.1,
                "rmse": 1.5,
                "r2": 0.6,
                "n_predictions": 20,
                "mean_residual": 0.0,
                "min_residual": -2.0,
                "max_residual": 2.0
            },
            target_column="target",
            diagnostics_summary={
                "median_absolute_error": 0.9,
                "p90_absolute_error": 2.1,
                "max_absolute_error": 3.0,
                "top_features": [
                    {"variable": "x", "importancia": 0.8}
                ],
                "warnings": []
            },
            user_context={
                "goal": "priorizar casos",
                "audience": "Público general",
                "decision": "revisar casos",
                "acceptable_error": 1.2,
                "impact": "Medio"
            },
            language=language
        )

    def test_full_report_contains_context_and_diagnostics(self):
        report = self.build_report()

        self.assertIn("CONTEXTO DEL ANÁLISIS", report)
        self.assertIn("DIAGNÓSTICO DEL MODELO", report)
        self.assertIn("priorizar casos", report)

    def test_full_report_can_be_generated_in_english(self):
        report = self.build_report(language="en")

        self.assertIn("ANALYSIS CONTEXT", report)
        self.assertIn("MODEL DIAGNOSTICS", report)
        self.assertIn("PLAIN-LANGUAGE INTERPRETATION", report)
        self.assertIn("Gradient Boosting", report)


if __name__ == "__main__":
    unittest.main()
