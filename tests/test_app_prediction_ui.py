from pathlib import Path
import logging
import unittest

from streamlit.testing.v1 import AppTest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
logging.getLogger("streamlit").setLevel(logging.ERROR)


class PredictionInterfaceTests(unittest.TestCase):
    def test_complete_interface_can_predict_a_new_observation(self):
        rows = ["measurement,size,group,target"]

        for index in range(60):
            measurement = 10 + index * 0.25
            size = 20 + index
            group = "A" if index % 2 == 0 else "B"
            target = 1.5 * measurement + 0.2 * size + (2 if group == "B" else 0)
            rows.append(
                f"{measurement:.2f},{size},{group},{target:.3f}"
            )

        content = ("\n".join(rows) + "\n").encode("utf-8")
        app = AppTest.from_file(
            PROJECT_ROOT / "app.py",
            default_timeout=60
        ).run(timeout=60)

        app.file_uploader[0].upload(
            "biological_sample.csv",
            content,
            "text/csv"
        ).run(timeout=60)

        analyze_button = next(
            button
            for button in app.button
            if button.label == "Analizar y comparar modelos"
        )
        analyze_button.click().run(timeout=120)

        self.assertFalse(app.exception)
        self.assertTrue(any(
            "Predecir una observación nueva" in markdown.value
            for markdown in app.markdown
        ))
        self.assertTrue(any(
            "¿Qué podés hacer en esta sección?" in markdown.value
            for markdown in app.markdown
        ))
        self.assertTrue(any(
            "Paso 1 de 2" in markdown.value
            for markdown in app.markdown
        ))

        next(
            widget
            for widget in app.number_input
            if widget.label == "Measurement"
        ).set_value(16.5)
        next(
            widget
            for widget in app.number_input
            if widget.label == "Size"
        ).set_value(46)
        next(
            widget
            for widget in app.selectbox
            if widget.label == "Group"
        ).select("A")
        next(
            button
            for button in app.button
            if button.label == "Calcular estimación"
        ).click().run(timeout=60)

        self.assertFalse(app.exception)
        self.assertTrue(any(
            '<div class="biodata-single-prediction" role="status"'
            in markdown.value
            for markdown in app.markdown
        ))

        self.assertTrue(any(
            "¿Cómo leer este resultado?" in markdown.value
            for markdown in app.markdown
        ))

        next(
            button
            for button in app.button
            if button.label == "Cargar otro caso"
        ).click().run(timeout=60)

        self.assertFalse(app.exception)
        self.assertFalse(any(
            '<div class="biodata-single-prediction" role="status"'
            in markdown.value
            for markdown in app.markdown
        ))
        self.assertIsNone(next(
            widget
            for widget in app.number_input
            if widget.label == "Measurement"
        ).value)

        next(
            widget
            for widget in app.number_input
            if widget.label == "Measurement"
        ).set_value(16.5)
        next(
            widget
            for widget in app.number_input
            if widget.label == "Size"
        ).set_value(46)
        next(
            widget
            for widget in app.selectbox
            if widget.label == "Group"
        ).select("A")
        next(
            button
            for button in app.button
            if button.label == "Calcular estimación"
        ).click().run(timeout=60)

        next(
            control
            for control in app.segmented_control
            if control.key == "biodata_language"
        ).set_value("en").run(timeout=60)

        self.assertFalse(app.exception)
        self.assertTrue(any(
            "Predict a new observation" in markdown.value
            for markdown in app.markdown
        ))
        self.assertTrue(any(
            "How should you read this result?" in markdown.value
            for markdown in app.markdown
        ))
        self.assertTrue(any(
            '<div class="biodata-single-prediction" role="status"'
            in markdown.value
            for markdown in app.markdown
        ))


if __name__ == "__main__":
    unittest.main()
