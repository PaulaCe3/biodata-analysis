import unittest

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from src.inference import (
    assess_observation,
    build_feature_profiles,
    build_observation,
    predict_observation
)
from src.modeling import train_regression_model
from src.preprocessing import build_preprocessor


class InferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.X = pd.DataFrame({
            "length": [10.0, 11.0, 12.5, 13.0, 14.0, 15.5, 16.0, 17.0],
            "weight": [20, 22, 25, 26, 29, 31, 33, 35],
            "group": ["A", "A", "B", "B", "A", "B", "A", None]
        })
        cls.y = pd.Series([1.0, 1.2, 1.7, 1.8, 2.1, 2.5, 2.7, 3.0])
        cls.numeric_features = ["length", "weight"]
        cls.categorical_features = ["group"]
        cls.profiles = build_feature_profiles(
            cls.X,
            cls.numeric_features,
            cls.categorical_features
        )
        cls.model = train_regression_model(
            build_preprocessor(
                cls.numeric_features,
                cls.categorical_features
            ),
            LinearRegression(),
            cls.X,
            cls.y
        )

    def test_feature_profiles_keep_ranges_categories_and_input_steps(self):
        length_profile = self.profiles["length"]
        group_profile = self.profiles["group"]

        self.assertEqual(length_profile["kind"], "numeric")
        self.assertEqual(length_profile["minimum"], 10.0)
        self.assertEqual(length_profile["maximum"], 17.0)
        self.assertGreater(length_profile["step"], 0)
        self.assertEqual(group_profile["categories"], ["A", "B"])

    def test_new_observation_uses_the_training_pipeline(self):
        observation = build_observation(
            ["length", "weight", "group"],
            {"length": 13.5, "weight": 28, "group": "A"}
        )

        prediction = predict_observation(self.model, observation)
        assessment = assess_observation(observation, self.profiles)

        self.assertTrue(np.isfinite(prediction))
        self.assertEqual(assessment["provided_count"], 3)
        self.assertFalse(assessment["missing_features"])
        self.assertFalse(assessment["out_of_range_features"])
        self.assertFalse(assessment["unseen_categories"])

    def test_assessment_flags_missing_unseen_and_out_of_range_values(self):
        observation = build_observation(
            ["length", "weight", "group"],
            {"length": 30.0, "weight": None, "group": "C"}
        )

        assessment = assess_observation(observation, self.profiles)
        prediction = predict_observation(self.model, observation)

        self.assertEqual(assessment["provided_count"], 2)
        self.assertEqual(assessment["missing_features"], ["weight"])
        self.assertEqual(assessment["out_of_range_features"], ["length"])
        self.assertEqual(assessment["unseen_categories"], ["group"])
        self.assertTrue(np.isfinite(prediction))


if __name__ == "__main__":
    unittest.main()
