# HBS Risk Calculator

## Hungry Bone Syndrome Prediction Tool

A comprehensive web application for predicting Hungry Bone Syndrome risk in patients undergoing total parathyroidectomy with autotransplantation for secondary hyperparathyroidism.

### Features

- **Interactive Risk Calculator**: Real-time HBS probability calculation
- **Beautiful UI**: Gradient backgrounds, animations, and modern design
- **Clinical Guidelines**: Evidence-based management recommendations
- **Model Information**: Detailed performance metrics and validation data
- **Research Background**: Comprehensive pathophysiology and study details

### Model Performance

- **AUC**: 0.742 (optimism-corrected)
- **Validation**: 500 bootstrap iterations
- **Study Population**: 227 patients
- **HBS Incidence**: 49.8%

### Predictors

1. **Age** (years)
2. **Phosphate at 1 month** (mmol/L)
3. **Alkaline Phosphatase at 1 month** (U/L)
4. **PTH at 3 months** (pmol/L)

### Risk Categories

- **Low Risk (<30%)**: Standard monitoring
- **Intermediate Risk (30-70%)**: Enhanced monitoring
- **High Risk (>70%)**: Intensive care

### Usage

```bash
streamlit run app.py
