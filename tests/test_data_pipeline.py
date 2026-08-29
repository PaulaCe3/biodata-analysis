from io import StringIO
import unittest

import numpy as np
import pandas as pd
from sklearn.datasets import load_diabetes
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import GradientBoostingRegressor

from src.data_loader import load_dataset, validate_column_names
from src.data_profiler import get_dataset_fingerprint, get_dataset_profile
from src.data_quality import get_quality_report
from src.diagnostics import (
    build_diagnostic_warnings,
    build_prediction_table,
    calculate_permutation_feature_importance,
    summarize_diagnostics
)
from src.eda import (
    get_categorical_summary,
    get_numeric_summary,
    plot_categorical_distribution,
    plot_correlation_heatmap,
    plot_numeric_distribution
)
from src.evaluation import (
    evaluate_regression_model,
    summarize_regression_evaluation
)
from src.modeling import (
    compare_regression_models,
    cross_validate_regression_mae,
    select_best_regression_model,
    train_regression_model
)
from src.preprocessing import (
    build_preprocessor,
    detect_feature_types,
    get_valid_regression_targets,
    prepare_regression_dataset,
    split_train_test
)
from src.report import build_full_report


class DataPipelineTests(unittest.TestCase):
    def test_loader_detects_semicolon_separator(self):
        dataset = load_dataset(StringIO("a;b\n1;2\n3;4\n"))

        self.assertEqual(dataset.columns.tolist(), ["a", "b"])
        self.assertEqual(dataset.shape, (2, 2))

    def test_column_names_are_normalized_and_must_be_unique(self):
        self.assertEqual(
            validate_column_names([" largo ", "peso"]),
            ["largo", "peso"]
        )

        with self.assertRaises(ValueError):
            validate_column_names(["peso", " peso "])

    def test_summaries_handle_no_numeric_data_and_limit_categories(self):
        dataset = pd.DataFrame({"grupo": [f"g{i}" for i in range(60)]})

        self.assertTrue(get_numeric_summary(dataset).empty)
        self.assertEqual(
            len(get_categorical_summary(dataset, max_categories=10)["grupo"]),
            10
        )

    def test_categorical_plot_handles_missing_values(self):
        dataset = pd.DataFrame({
            "sexo": ["female", "male", np.nan, "female"]
        })

        figure = plot_categorical_distribution(dataset, "sexo")
        labels = [
            tick.get_text()
            for tick in figure.axes[0].get_xticklabels()
        ]

        self.assertIn("Sin dato", labels)
        figure.clear()

    def test_exploration_plots_accept_english_language(self):
        dataset = pd.DataFrame({
            "length": [39.1, 39.5, 40.3, np.nan],
            "mass": [3750, 3800, 3250, 3450]
        })

        figures = [
            plot_numeric_distribution(dataset, "length", language="en"),
            plot_correlation_heatmap(dataset, language="en")
        ]

        self.assertTrue(all(figure.axes for figure in figures))

        for figure in figures:
            figure.clear()

    def test_fingerprint_changes_when_values_change(self):
        original = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
        modified = original.copy()
        modified.loc[1, "y"] = 99

        self.assertNotEqual(
            get_dataset_fingerprint(original),
            get_dataset_fingerprint(modified)
        )

    def test_quality_report_counts_infinite_values(self):
        quality = get_quality_report(
            pd.DataFrame({"medida": [1.0, np.inf, -np.inf, np.nan]})
        )

        self.assertEqual(quality["missing_values"]["medida"], 1)
        self.assertEqual(quality["infinite_values"]["medida"], 2)

    def test_regression_preparation_drops_invalid_target_rows(self):
        dataset = pd.DataFrame({
            "medida": range(12),
            "grupo": ["A", None] * 6,
            "objetivo": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, np.nan, np.inf]
        })

        X, y, dropped_rows = prepare_regression_dataset(dataset, "objetivo")
        feature_types = detect_feature_types(X)
        preprocessor = build_preprocessor(
            feature_types["numeric_features"],
            feature_types["categorical_features"]
        )

        transformed = preprocessor.fit_transform(X, y)

        self.assertEqual(dropped_rows, 2)
        self.assertEqual(len(y), 10)
        self.assertEqual(transformed.shape[0], 10)

    def test_only_suitable_targets_are_offered(self):
        dataset = pd.DataFrame({
            "válido": range(10),
            "constante": [1] * 10,
            "insuficiente": [1, 2] + [np.nan] * 8
        })

        self.assertEqual(get_valid_regression_targets(dataset), ["válido"])

    def test_cross_validation_rejects_more_folds_than_rows(self):
        with self.assertRaises(ValueError):
            cross_validate_regression_mae(
                pipeline=None,
                X_train=pd.DataFrame({"x": [1]}),
                y_train=pd.Series([1]),
                n_splits=2
            )

    def test_complete_regression_flow_generates_a_report(self):
        dataset = load_diabetes(as_frame=True).frame.iloc[:180]
        X, y, _ = prepare_regression_dataset(dataset, "target")
        feature_types = detect_feature_types(X)
        X_train, X_test, y_train, y_test = split_train_test(X, y)
        preprocessor = build_preprocessor(
            feature_types["numeric_features"],
            feature_types["categorical_features"]
        )
        models = {
            "Dummy": DummyRegressor(strategy="mean"),
            "Gradient Boosting": GradientBoostingRegressor(random_state=42)
        }

        comparison = compare_regression_models(
            preprocessor,
            models,
            X_train,
            y_train,
            n_splits=3
        )
        best_name = select_best_regression_model(comparison)
        trained_model = train_regression_model(
            preprocessor,
            models[best_name],
            X_train,
            y_train
        )
        evaluation = evaluate_regression_model(
            trained_model,
            X_test,
            y_test
        )
        evaluation_summary = summarize_regression_evaluation(evaluation)
        prediction_table = build_prediction_table(
            X_test,
            y_test,
            evaluation["predictions"]
        )
        importance = calculate_permutation_feature_importance(
            trained_model,
            X_test,
            y_test,
            n_repeats=2
        )
        warnings = build_diagnostic_warnings(
            evaluation_summary,
            prediction_table
        )
        diagnostics = summarize_diagnostics(
            prediction_table,
            importance,
            warnings
        )
        report = build_full_report(
            dataset_profile=get_dataset_profile(dataset),
            quality_report=get_quality_report(dataset),
            model_comparison=comparison,
            evaluation_summary=evaluation_summary,
            target_column="target",
            diagnostics_summary=diagnostics
        )

        self.assertIn(best_name, comparison)
        self.assertIn("INTERPRETACIÓN EN LENGUAJE CLARO", report)
        self.assertIn("DIAGNÓSTICO DEL MODELO", report)


if __name__ == "__main__":
    unittest.main()
