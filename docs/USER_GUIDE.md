# Biodata user guide

Biodata is a web application for exploring tabular data, reviewing data quality and comparing predictive regression models. It supports the analysis by organizing the workflow, explaining results and making limitations visible. It does not replace domain expertise or human judgment.

## Quick workflow

1. Choose a language and appearance under **Preferences**.
2. Upload a CSV, DATA or TXT file from the sidebar.
3. Confirm whether the first row contains column names.
4. Review **Overview** and **Explore** before modeling.
5. Under **Models**, choose a numeric target variable.
6. Keep only predictors that would be available when making a real prediction.
7. Select **Analyze and compare models**.
8. Review metrics, diagnostics and limitations.
9. To study a new case, complete **Predict a new observation**.
10. Download the report to preserve the result.

## 1. Supported data

Biodata works with tabular data: each row represents one observation and each column represents one variable.

| species | bill_length | body_mass | sex | year |
|---|---:|---:|---|---:|
| Adelie | 39.1 | 3750 | male | 2007 |
| Gentoo | 46.1 | 4500 | female | 2008 |

Files may contain numeric variables, categorical variables and missing values. The public demonstration accepts files up to 25 MB.

The current version requires a **numeric target variable** because it solves regression problems, such as predicting weight, length, concentration, yield or time.

## 2. Before uploading a file

Check that:

- Every column has one clear meaning.
- Column names are not duplicated.
- Numbers are stored as numbers rather than values mixed with units such as `25 kg`.
- Categories use consistent labels.
- The intended target has enough known values and more than one distinct value.
- The file contains no personal, clinical, confidential or regulated data.

If the file has no headers, turn off **The file has column names**. Biodata will let you name the columns before continuing.

## 3. Language and appearance

Open **Preferences** in the sidebar.

- **Idioma / Language:** switches the interface, charts and report between Spanish and English.
- **Automatic:** follows the device appearance.
- **Dark:** keeps the dark interface.
- **Light:** keeps the light interface.

Changing these preferences should preserve the uploaded file and results stored in the session.

## 4. Overview tab

This section explains what the dataset contains before any modeling decision is made.

- **Observations:** number of rows.
- **Variables:** number of columns.
- **Missing values:** cells without information.
- **Duplicate rows:** fully repeated rows.

The preview shows the first observations so you can verify the structure, names and value types. It is not necessarily representative of the full dataset.

Biodata reports missing values, infinite numeric values and duplicate rows. It does not silently delete duplicates or overwrite the original file. These findings remain visible so the responsible person can decide how to correct the source data.

## 5. Explore tab

Use exploration to understand distributions, scales and possible issues before training a model.

- **Numeric summary:** includes the mean, standard deviation, minimum, maximum and quartiles.
- **Categorical summary:** shows the most common categories and their frequency.
- **Numeric distribution:** reveals concentration, asymmetry, gaps and possible extreme values.
- **Categorical distribution:** compares group sizes and labels missing values as **Missing**.
- **Correlation:** summarizes linear relationships among numeric variables.

A correlation close to `1` means two variables tend to increase together; a value close to `-1` means one tends to decrease as the other increases; a value near `0` means there is little linear association. Correlation does not establish causation.

## 6. Models tab

### Target variable

The target is the numeric value you want to estimate. Choose it from a specific question, such as “Can body mass be estimated from the available measurements?”.

Do not use an identifier, record number or code as the target even if it is numeric.

### Predictors

Predictors are the variables used to estimate the target. Include only information that would be available at prediction time and that has a reasonable connection to the problem.

Exclude unique identifiers, future information and variables derived from the target. Otherwise, **data leakage** can make a model look accurate during testing while causing it to fail in real use.

### Use context

This optional section records the intended use, an acceptable error and any groups that deserve special attention. Biodata uses the context to make the report more practical.

### Analysis process

Biodata:

1. Reserves 20% of the observations for final testing.
2. Uses the remaining 80% for training and model comparison.
3. Fills missing numeric predictors with the training median.
4. Fills missing categorical predictors with the most frequent training category.
5. Encodes categories for model use.
6. Compares four alternatives through cross-validation.
7. Selects the model with the lowest average MAE.
8. Evaluates the winner once on the reserved data.

Rows with a missing or infinite target are excluded from modeling because no valid outcome exists for training or evaluation.

## 7. Models compared

- **Dummy:** predicts using a simple rule such as the mean and provides a minimum baseline.
- **Linear regression:** represents linear relationships between predictors and the target.
- **Random Forest:** combines many trees and can learn nonlinear relationships.
- **Gradient Boosting:** builds successive trees that try to correct previous errors.

A more complex model is not automatically better. Biodata selects the model based on measured performance.

## 8. Metrics

### MAE

Mean absolute error is the average distance between predictions and actual values. It uses the same unit as the target. Lower is better, but the value must be compared with a predefined acceptable error.

### RMSE

Root mean squared error penalizes large errors more strongly. When it is much higher than MAE, some cases may be failing by considerably more than the average.

### R²

R² describes the proportion of observed variation represented by the model.

- Close to `1`: much of the observed variation is represented.
- Close to `0`: little improvement over predicting a mean.
- Below `0`: worse than that simple baseline on the test data.

A high R² does not prove causation and does not guarantee that every individual prediction is accurate.

### P90 error

Ninety percent of cases have an absolute error at or below this value. It helps interpret performance beyond the average.

### Residual

A residual is the difference between an actual value and its prediction. Patterns in residuals may reveal bias, missing structure or difficult cases.

## 9. Diagnostics and feature importance

- Points closer to the diagonal in the actual-versus-predicted chart indicate closer predictions.
- Residual patterns may reveal systematic overestimation or underestimation.
- Permutation importance measures how much performance drops when a variable is disrupted.
- Group error comparisons can reveal uneven performance among categories with enough observations.

Predictive importance does not establish causation and does not explain an individual prediction by itself.

## 10. Using results responsibly

Before using a model:

1. Define an acceptable error for the real task.
2. Compare it with MAE, RMSE and P90.
3. Review the largest errors.
4. Check whether relevant groups receive worse predictions.
5. Validate with new data from another time, place or population.
6. Keep human review for high-impact decisions.

The model can support ordering, prioritization or case review. It should not make important decisions by itself.

### Predicting a new observation

This section is for studying **one case collected after the analysis**. A new observation may be an animal measured in the field, a sampled plant, a laboratory sample or any other record with the same variables as the dataset.

For example, after training a model with measurements from many plants, you can enter measurements from a newly observed plant to estimate the target. You do not need to add that row to the file or run the whole analysis again.

#### How to use it

1. Find **Predict a new observation** under **Models**.
2. Read the introductory box. It explains what a new case is and which target will be estimated.
3. In **Step 1**, enter the measurements and categories you know. Each field shows its data type and, when applicable, the range observed in the dataset.
4. Use the same units and definitions as the original file.
5. If a value is genuinely unknown, leave the field empty. Biodata can still calculate using a typical training value, but it will warn that the result may be less representative.
6. Select **Calculate estimate**.
7. In **Step 2**, read the estimated value first and then the explanation of the error observed during testing.
8. Review every warning before using the result.

#### How to interpret the result

- **Estimated value:** the result calculated by the model for the entered case. It is not a confirmed measurement.
- **Average error:** how far predictions differed from actual values on average when Biodata tested the model with reserved data.
- **9-out-of-10 reference:** an error threshold that was not exceeded in 90% of test cases. It does not guarantee the error for this particular observation.
- **Warnings:** explain whether data is missing, a measurement is outside the known range or a category is new to the model. Each warning also explains what to review.

Biodata warns when a measurement falls outside the observed range, a category was absent from training, predictors are missing or the estimate falls outside the known target range. In these situations, the model has less relevant reference information and its error may increase.

Select **Enter another case** to clear the form and study a different observation. The estimate remains in session memory and disappears when the application is closed or restarted.

After evaluating the winning model on the held-out test set, Biodata fits it again using all valid cases. This final model remains available during the session. The new case does not modify the original dataset or previous results.

## 11. Downloadable report

The report includes the dataset profile, quality findings, analysis context, model comparison, final evaluation, diagnostics, predictive importance, practical interpretation and limitations.

Store it together with the dataset version and analysis date to maintain traceability.

## 12. Privacy and limitations

In the public demonstration, the file is transferred to Streamlit Community Cloud and processed temporarily in memory. Biodata does not store a permanent copy or send its contents to other services.

Use public, synthetic or test data only. Do not upload personal, clinical, confidential or regulated information.

Current limitations:

- Only numeric regression targets are supported.
- Internal validation does not replace external validation.
- Individual prediction intervals are not calculated.
- The model for new cases remains available only during the current session.
- Predictive results do not establish causation.
- Domain-expert review is still required.

## 13. Common problems

### A variable is not available as a target

It must be numeric, contain at least ten valid values and have more than one distinct value.

### A numeric column is treated as categorical

Check for units, symbols or text mixed with the numbers.

### The model looks unrealistically accurate

Look for identifiers, future information or variables derived from the target. Data leakage may be present.

### Performance changes on another dataset

The population, period, measurement method or data quality may have changed. Validate again and update the model when appropriate.

### The application displays an error

Refresh the page, remove the file and upload it again. If the error continues, record the action, file type and displayed message without sharing sensitive data.

## Essential glossary

- **Dataset:** an organized collection of data.
- **Observation:** one row in the dataset.
- **Variable:** a characteristic stored in a column.
- **Target:** the value to be predicted.
- **Predictor:** a variable used to estimate the target.
- **Missing value:** absent or unknown information.
- **Imputation:** controlled replacement of missing predictor values for modeling.
- **Training:** the stage in which a model learns patterns.
- **Test set:** reserved data used for final evaluation.
- **Cross-validation:** repeated model comparison using different parts of the training data.
- **Overfitting:** strong performance on known data and poor performance on new data.
- **Data leakage:** accidental use of information that would not exist at prediction time.
- **Regression:** modeling a continuous numeric target.
- **Inference:** using a trained model to estimate the target for a new observation.
- **Causation:** a relationship in which one change produces another; prediction alone does not prove it.

## Final checklist

- [ ] I understand what each row and variable represents.
- [ ] I reviewed missing, infinite, duplicate and extreme values.
- [ ] I chose a target that matches the question.
- [ ] I excluded identifiers and future information.
- [ ] I defined an acceptable error before reviewing results.
- [ ] I reviewed MAE, RMSE, R² and P90.
- [ ] I reviewed large errors and relevant groups.
- [ ] New cases use the same variables, definitions and units as training.
- [ ] I understand that predictive importance is not causation.
- [ ] I will validate with new data.
- [ ] Important decisions will retain human oversight.
