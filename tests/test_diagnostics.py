import unittest

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor

from src.diagnostics import (
    build_diagnostic_warnings,
    build_prediction_table,
    calculate_permutation_feature_importance,
    calculate_subgroup_errors,
    get_largest_errors,
    plot_actual_vs_predicted,
    plot_feature_importance,
    plot_residual_distribution,
    plot_residuals,
    summarize_diagnostics
)
from src.modeling import train_regression_model
from src.preprocessing import build_preprocessor


class DiagnosticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rng = np.random.default_rng(42)
        cls.X = pd.DataFrame(
            {
                "signal": rng.normal(size=120),
                "noise": rng.normal(size=120),
                "group": np.where(np.arange(120) % 2 == 0, "A", "B")
            }
        )
        cls.y = 4 * cls.X["signal"] + rng.normal(scale=0.2, size=120)

        preprocessor = build_preprocessor(
            ["signal", "noise"],
            ["group"]
        )
        cls.model = train_regression_model(
            preprocessor,
            GradientBoostingRegressor(random_state=42),
            cls.X,
            cls.y
        )
        cls.predictions = cls.model.predict(cls.X)
        cls.table = build_prediction_table(
            cls.X,
            cls.y,
            cls.predictions
        )

    def test_prediction_table_and_largest_errors(self):
        self.assertEqual(len(self.table), len(self.X))
        self.assertIn("error_absoluto", self.table.columns)

        largest = get_largest_errors(self.table, n=5)

        self.assertEqual(len(largest), 5)
        self.assertTrue(
            largest["error_absoluto"].is_monotonic_decreasing
        )

    def test_feature_importance_uses_original_features(self):
        importance = calculate_permutation_feature_importance(
            self.model,
            self.X,
            self.y,
            n_repeats=3
        )

        self.assertEqual(set(importance["variable"]), set(self.X.columns))
        self.assertEqual(importance.iloc[0]["variable"], "signal")

    def test_subgroups_warnings_and_summary(self):
        subgroups = calculate_subgroup_errors(
            self.table,
            ["group"],
            min_group_size=10
        )
        evaluation_summary = {
            "mae": float(self.table["error_absoluto"].mean()),
            "mean_residual": float(self.table["residuo"].mean())
        }
        importance = calculate_permutation_feature_importance(
            self.model,
            self.X,
            self.y,
            n_repeats=2
        )
        warnings = build_diagnostic_warnings(
            evaluation_summary,
            self.table,
            subgroups
        )
        summary = summarize_diagnostics(
            self.table,
            importance,
            warnings
        )

        self.assertEqual(set(subgroups["grupo"]), {"A", "B"})
        self.assertIn("p90_absolute_error", summary)
        self.assertTrue(summary["top_features"])

    def test_plots_are_created(self):
        importance = calculate_permutation_feature_importance(
            self.model,
            self.X,
            self.y,
            n_repeats=2
        )
        figures = [
            plot_actual_vs_predicted(self.table, "target"),
            plot_residuals(self.table),
            plot_residual_distribution(self.table),
            plot_feature_importance(importance)
        ]

        self.assertTrue(all(figure.axes for figure in figures))

        for figure in figures:
            plt.close(figure)


if __name__ == "__main__":
    unittest.main()
