# DriveGuard-X Battery AI

## Lithium-Ion Battery State of Health Estimation using Machine Learning

**Project:** DriveGuard-X  
**Module:** Battery AI  
**Primary Task:** Lithium-Ion Battery State of Health (SOH) Estimation  
**Dataset:** NASA Li-Ion Battery Aging Dataset  
**Base Research Paper:** Pandit and Ahlawat, *A standardized comparative framework for machine learning techniques in lithium-ion battery state of health estimation*  
**Final Model:** Random Forest Regressor  
**Implementation Environment:** Python / Kaggle Notebook  
**Intended Integration:** MATLAB/Simulink + ESP32-based DriveGuard-X prototype

---

# 1. Overview

The Battery AI module is one of the core intelligence components of **DriveGuard-X**, an adaptive battery protection system designed for an electric-vehicle-like platform.

The purpose of this module is to estimate the **State of Health (SOH)** of a lithium-ion battery from measurable electrical, thermal and discharge characteristics.

Battery degradation is an important factor in electric vehicle safety and performance. As a battery ages, its usable capacity decreases and its electrical and thermal behavior changes. A battery protection system therefore should not treat every battery as if it were in the same condition.

The Battery AI module provides an estimated SOH value that can subsequently be used by the higher-level DriveGuard-X decision system to adapt protection behavior.

The overall concept is:

```text
Battery Measurements
        │
        ▼
┌───────────────────────┐
│ Feature Extraction    │
│                       │
│ Voltage               │
│ Current               │
│ Temperature           │
│ Discharge Behavior    │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│      Battery AI       │
│                       │
│ Random Forest Model   │
└───────────┬───────────┘
            │
            ▼
       Estimated SOH
            │
            ▼
┌───────────────────────┐
│ DriveGuard-X Decision │
│ Layer                 │
└───────────┬───────────┘
            │
            ▼
   Adaptive Protection
```

The Battery AI model is **not intended to independently make safety-critical decisions**. It provides battery-health information to the larger DriveGuard-X protection architecture.

---

# 2. Project Motivation

A conventional battery protection system generally operates using fixed electrical thresholds such as:

- Overcurrent
- Overvoltage
- Undervoltage
- Overtemperature

However, battery behavior changes as the battery ages.

For example, the same current event may have different implications for:

- A healthy battery
- A moderately degraded battery
- A severely degraded battery

DriveGuard-X therefore introduces battery health as an additional input to the protection architecture.

The intended system is not simply:

```text
Current > Threshold
        ↓
Protection
```

Instead, it aims toward:

```text
Battery condition
        +
Driver behavior
        +
Road condition
        ↓
Causal interpretation
        ↓
Adaptive protection
```

The Battery AI module is responsible for the **battery-condition component** of this architecture.

---

# 3. Research Baseline

The Battery AI development was based on the following research paper:

> **Ravi Pandit and Nikhil Ahlawat**,  
> *A standardized comparative framework for machine learning techniques in lithium-ion battery state of health estimation*,  
> Future Batteries 7 (2025), 100099.

**DOI:** `10.1016/j.fub.2025.100099`

The paper was selected because it provides a standardized comparison of machine-learning algorithms for lithium-ion battery SOH estimation using the NASA battery aging dataset.

The paper evaluates:

- XGBoost
- Random Forest
- Support Vector Machine

and uses a battery-level training/testing methodology involving:

```text
Training:
B0005

Testing:
B0006
B0007
B0018
```

The DriveGuard-X Battery AI development initially reproduced this methodology before extending it into a more generalized battery-level evaluation.

---

# 4. Development Philosophy

The objective was **not to simply reproduce the paper**.

The development strategy was:

```text
Base Research Paper
        │
        ▼
Paper-Compatible Reproduction
        │
        ▼
Baseline Performance
        │
        ▼
Feature Engineering
        │
        ▼
Larger Battery Dataset
        │
        ▼
Generalization Investigation
        │
        ▼
Operating-Condition Analysis
        │
        ▼
Battery-Level Cross Validation
        │
        ▼
Robust Model Selection
        │
        ▼
Untouched-Battery Evaluation
        │
        ▼
Final Battery AI Model
```

This allowed the project to answer two different questions:

### Question 1

Can our implementation achieve comparable or better performance than the selected research paper under a similar evaluation setup?

### Question 2

Does the resulting model generalize to batteries that operate under different conditions?

The first question produced a strong paper-compatible result.

The second question revealed significant domain-shift challenges and led to the selection of Random Forest as the final generalized model.

---

# 5. Dataset

The model uses the **NASA Li-Ion Battery Aging Dataset**.

The dataset contains measurements collected during battery aging experiments, including:

- Voltage
- Current
- Temperature
- Load current
- Load voltage
- Time
- Discharge capacity

The raw dataset contains thousands of individual experiment CSV files.

The metadata file contains information such as:

```text
type
start_time
ambient_temperature
battery_id
test_id
uid
filename
Capacity
Re
Rct
```

The experiments are categorized into:

- Charge
- Discharge
- Impedance

For SOH estimation, the project focuses on **discharge experiments**.

---

# 6. Dataset Structure

A representative discharge experiment contains measurements such as:

```text
Voltage_measured
Current_measured
Temperature_measured
Current_load
Voltage_load
Time
```

The raw measurements are converted into a single cycle-level feature vector.

```text
Raw CSV
   │
   ├── Voltage measurements
   ├── Current measurements
   ├── Temperature measurements
   ├── Load current
   ├── Load voltage
   └── Time
          │
          ▼
   Feature Extraction
          │
          ▼
   One feature vector
   for one discharge cycle
```

---

# 7. SOH Definition

Battery State of Health is represented using discharge capacity relative to a reference capacity.

The basic definition used in the paper-compatible experiment is:

\[
SOH = \frac{C_i}{C_0}
\]

or, when expressed as a percentage:

\[
SOH(\%) = \frac{C_i}{C_0}\times100
\]

where:

- \(C_i\) = measured capacity at cycle \(i\)
- \(C_0\) = reference/initial battery capacity

For the paper batteries B0005, B0006, B0007 and B0018, the paper-compatible implementation uses the first recorded capacity as the initial reference.

For the generalized dataset, battery-specific reference capacities were investigated because several batteries contained anomalous early capacity values.

The generalized implementation uses the maximum capacity observed within the first five valid observations for the additional batteries.

This avoids producing physically unrealistic SOH values above 100% caused by clearly anomalous initial capacity records.

---

# 8. Data Quality Investigation

An important part of the project was determining whether abnormal SOH values were caused by model behavior or by the dataset itself.

An initial generalized SOH calculation produced physically unrealistic values such as:

```text
SOH > 100%
```

and in some cases extremely large values.

For example, some batteries contained early capacity measurements that were far below the later measurements.

This made a simple:

```text
first capacity = C0
```

rule inappropriate for every battery in the dataset.

The dataset was therefore investigated battery by battery.

The investigation considered:

- Capacity trajectories
- SOH trajectories
- Cycle ordering
- Capacity jumps
- Temperature
- Current
- Discharge duration
- Voltage behavior
- Battery operating conditions

This analysis showed that the dataset contains multiple experimental regimes and several batteries with unusual early measurements.

---

# 9. Feature Engineering

Each discharge experiment is converted into a cycle-level feature vector.

The final feature set contains **21 features**.

## Electrical Features

### Voltage

```text
voltage_initial
voltage_final
voltage_min
voltage_max
voltage_mean
voltage_std
voltage_drop
```

These describe the voltage behavior during discharge.

### Current

```text
current_mean
current_min
current_max
current_std
```

These describe the measured discharge current behavior.

---

# 10. Thermal Features

Temperature behavior is represented using:

```text
temperature_initial
temperature_final
temperature_max
temperature_mean
temperature_rise
```

These features capture thermal behavior during the discharge process.

---

# 11. Load and Discharge Features

The model also uses:

```text
load_current_abs_mean
load_current_abs_max
load_voltage_mean
load_voltage_min
discharge_duration
```

Absolute load-current features were introduced because the raw load-current measurements can contain different sign conventions.

Using the absolute magnitude makes these features less dependent on measurement sign convention.

---

# 12. Complete Feature Set

The final 21-feature input vector is:

```text
1.  voltage_initial
2.  voltage_final
3.  voltage_min
4.  voltage_max
5.  voltage_mean
6.  voltage_std
7.  voltage_drop
8.  current_mean
9.  current_min
10. current_max
11. current_std
12. temperature_initial
13. temperature_final
14. temperature_max
15. temperature_mean
16. temperature_rise
17. load_current_abs_mean
18. load_current_abs_max
19. load_voltage_mean
20. load_voltage_min
21. discharge_duration
```

---

# 13. Discharge Detection

The active discharge region is identified from the measured current.

The implementation uses:

```python
Current_measured < -0.1
```

as the active-discharge condition.

This removes portions of the measurement sequence that do not represent the actual discharge process.

The extracted active region is then used for feature calculation.

---

# 14. Paper-Compatible Baseline Experiment

The first major experiment intentionally followed the battery split used by the base paper.

```text
                 NASA Dataset
                      │
                      ▼
                  B0005
                      │
                      │ Training
                      ▼
               XGBoost Model
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
        B0006       B0007       B0018
          │           │           │
          └───────────┼───────────┘
                      │
                   Testing
```

This experiment was important because it allowed the DriveGuard-X implementation to be compared against the paper using the same basic battery-level evaluation structure.

---

# 15. Paper-Compatible Results

The DriveGuard-X XGBoost implementation produced:

| Battery | Paper MAE | DriveGuard-X MAE |
|---|---:|---:|
| B0006 | 0.070787 | **0.063250** |
| B0007 | 0.023080 | **0.019573** |
| B0018 | 0.016356 | **0.005879** |

MSE:

| Battery | Paper MSE | DriveGuard-X MSE |
|---|---:|---:|
| B0006 | 0.006306 | **0.004440** |
| B0007 | 0.000773 | **0.000471** |
| B0018 | 0.000347 | **0.000065** |

Therefore, under the paper-compatible experiment, DriveGuard-X achieved lower MAE and MSE for all three batteries.

The improvements were:

```text
B0006:
MAE improvement = 10.65%
MSE improvement = 29.59%

B0007:
MAE improvement = 15.19%
MSE improvement = 39.07%

B0018:
MAE improvement = 64.06%
MSE improvement = 81.27%
```

These results establish the first quantitative comparison between DriveGuard-X and the selected base paper.

---

# 16. Why the Paper-Compatible Experiment Was Not Enough

Although the paper-compatible experiment produced strong results, further investigation showed that it does not fully represent the generalization problem faced by DriveGuard-X.

The NASA dataset contains batteries operated under substantially different conditions.

Observed operating regimes include approximately:

```text
24°C / 2A
24°C / 4A
43°C / 4A
4°C / 1A
4°C / 2A
```

Temperature and current affect the observed battery behavior.

Therefore:

```text
Good performance on similar batteries
                ≠
Good performance on all unseen batteries
```

This motivated the generalized Battery AI experiment.

---

# 17. Generalized Dataset

The generalized dataset expanded the evaluation beyond the four batteries used in the paper-compatible experiment.

The final generalized development/test setup used **19 batteries** after excluding two highly problematic experimental groups during the robustness investigation.

The final generalized dataset contained:

```text
1518 cycle-level samples
19 batteries
21 engineered features
```

The battery groups represented multiple operating conditions.

---

# 18. Battery-Level Data Splitting

A critical design decision was to split data at the **battery level**, rather than randomly splitting individual cycles.

Random cycle-level splitting can produce:

```text
Battery A Cycle 1 ─── Training
Battery A Cycle 2 ─── Training
Battery A Cycle 3 ─── Validation
```

This allows the model to see data from the same battery during both training and validation.

Such a setup can overestimate generalization performance.

DriveGuard-X instead uses:

```text
Battery A ───── Training

Battery B ───── Validation

Battery C ───── Testing
```

This better represents the intended deployment scenario.

---

# 19. Operating-Condition Analysis

The generalized dataset was analyzed according to operating conditions.

| Condition | Batteries | Approx. Samples |
|---|---|---:|
| 24°C / 2A | B0005, B0006, B0007, B0018, B0028 | 664 |
| 24°C / 4A | B0025, B0027 | 56 |
| 43°C / 4A | B0029–B0032 | 160 |
| 4°C / 1A | B0045–B0048 | 277 |
| 4°C / 2A | B0053–B0056 | 361 |

The analysis showed significant differences between operating regimes in:

- Voltage
- Current
- Temperature
- Discharge duration
- Voltage drop
- Load behavior

This confirmed that **domain shift** is a major challenge for generalized SOH estimation.

---

# 20. Model Candidates

Three regression models were evaluated:

```text
XGBoost
Random Forest
Support Vector Regression
```

The reason for evaluating multiple models was to determine whether the best paper-compatible model was also the most robust model when generalization was considered.

---

# 21. Hyperparameter Optimization

Hyperparameter tuning was performed for the candidate models.

However, an important observation emerged during tuning.

A model can achieve excellent cross-validation performance when the validation samples come from batteries similar to the training battery while still performing poorly on genuinely unseen batteries.

Therefore, hyperparameter optimization alone was not considered sufficient for final model selection.

The final selection was based primarily on **battery-level robustness**.

---

# 22. Battery-Level GroupKFold

The generalized development dataset was divided using GroupKFold, with:

```text
Group = battery_id
```

This means that all cycles belonging to a battery remain together within a fold.

The development dataset contained:

```text
14 batteries
1018 cycle-level samples
```

Five additional batteries were reserved as a completely untouched final test set.

---

# 23. GroupKFold Results

The mean MAE across battery-level folds was:

| Model | Mean MAE | Standard Deviation |
|---|---:|---:|
| **Random Forest** | **0.042115** | **0.012953** |
| XGBoost | 0.051078 | 0.004175 |
| SVR | 0.127594 | 0.120856 |

Random Forest also achieved the best result on **9 of the 14 development batteries**.

Therefore, Random Forest was selected as the final generalized Battery AI model.

---

# 24. Final Model Architecture

The final Battery AI architecture is:

```text
                 Raw Battery Data
                        │
                        ▼
             ┌─────────────────────┐
             │ Discharge Detection │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │ Feature Extraction  │
             │                     │
             │ Voltage             │
             │ Current             │
             │ Temperature         │
             │ Load                │
             │ Discharge Duration  │
             └──────────┬──────────┘
                        │
                        ▼
              21-Dimensional Vector
                        │
                        ▼
             ┌─────────────────────┐
             │   Random Forest     │
             │     Regressor       │
             └──────────┬──────────┘
                        │
                        ▼
                 Estimated SOH
                        │
                        ▼
             DriveGuard-X Decision
                    Layer
```

---

# 25. Final Training and Testing Strategy

The final model uses:

### Development Set

```text
14 batteries
1018 cycle-level samples
```

These batteries are used for:

- Training
- Battery-level GroupKFold
- Model selection

### Untouched Test Set

```text
B0005
B0006
B0030
B0047
B0053
```

These batteries are not used for model selection.

The final Random Forest is retrained on all 14 development batteries and evaluated once on the five untouched batteries.

---

# 26. Final Model Performance

The final Random Forest achieved:

| Metric | Result |
|---|---:|
| **MAE** | **0.074921** |
| **MSE** | **0.008602** |
| **RMSE** | **0.092745** |
| **R²** | **0.367663** |

Per-battery results:

| Battery | MAE | RMSE | R² |
|---|---:|---:|---:|
| B0005 | 0.076112 | 0.097263 | 0.095355 |
| B0006 | 0.098159 | 0.112799 | 0.165279 |
| B0030 | 0.029732 | 0.032345 | 0.082935 |
| B0047 | 0.069388 | 0.077596 | -0.147188 |
| B0053 | 0.040104 | 0.046052 | -0.720507 |

The final result demonstrates moderate generalized performance under an intentionally difficult unseen-battery evaluation.

---

# 27. Final Random Forest Feature Importance

The final model identified the following as its most influential features:

| Rank | Feature | Importance |
|---:|---|---:|
| 1 | load_current_abs_mean | 0.198499 |
| 2 | discharge_duration | 0.190903 |
| 3 | voltage_std | 0.150883 |
| 4 | current_mean | 0.150567 |
| 5 | temperature_initial | 0.081750 |
| 6 | voltage_mean | 0.051304 |
| 7 | load_voltage_min | 0.044612 |
| 8 | load_voltage_mean | 0.032828 |
| 9 | voltage_drop | 0.020108 |
| 10 | voltage_max | 0.017275 |

This indicates that the model relies strongly on current behavior, discharge duration, voltage variation and initial thermal conditions.

Feature importance should be interpreted as model behavior and **not as proof of causal relationships**.

---

# 28. Final Actual vs Predicted Evaluation

The final model was evaluated on five untouched batteries.

The actual and predicted SOH trajectories are generated in the notebook and saved under:

```text
FINAL_BATTERY_MODEL/REPORT_GRAPHS/
```

The graphs include:

```text
B0005
B0006
B0030
B0047
B0053
```

These plots provide a cycle-by-cycle view of how the final Random Forest follows the degradation trajectory of each unseen battery.

Aggregate metrics alone cannot show whether the model follows the temporal degradation trend, so these plots are an important part of the evaluation.

---

# 29. Research Findings

The development process produced several important findings.

### Finding 1: XGBoost performs strongly in the paper-compatible experiment

The DriveGuard-X XGBoost implementation achieved lower MAE and MSE than the reported paper results for B0006, B0007 and B0018.

### Finding 2: Paper-compatible performance does not guarantee generalized performance

When additional batteries and operating conditions were introduced, model performance changed significantly.

### Finding 3: Operating-condition variation is a major source of domain shift

Temperature and discharge-current conditions significantly change battery measurements.

### Finding 4: Battery-level validation is more appropriate for generalization

GroupKFold prevents cycles from the same battery from being distributed across training and validation folds.

### Finding 5: Random Forest provided the best robustness

Although SVR performed strongly in some individual test configurations, its GroupKFold performance was highly unstable.

Random Forest provided the strongest overall development-battery robustness.

### Finding 6: The final model is suitable as a prototype component, not a safety-certified BMS model

The final model is appropriate for demonstrating the Battery AI concept within DriveGuard-X.

However, the current offline cycle-level model should not be interpreted as a production-ready safety-critical battery management algorithm.

---

# 30. Deployment Considerations

The current model is a **cycle-level research model**.

It uses features such as:

```text
discharge_duration
voltage_mean
voltage_std
current_mean
temperature_mean
...
```

Some of these features require substantial portions of a discharge cycle.

Therefore, directly deploying the current model into a real-time vehicle would not be ideal.

The next deployment adaptation is to create a **rolling-window Battery AI model**.

Conceptually:

```text
ESP32
 │
 ├── Voltage
 ├── Current
 └── Temperature
        │
        ▼
   Rolling Window
        │
        ▼
 Feature Extraction
        │
        ▼
  Random Forest
        │
        ▼
 Estimated SOH
```

This model can be developed separately while keeping the current cycle-level model as the research baseline.

---

# 31. Integration with DriveGuard-X

The Battery AI model is not intended to operate independently.

The complete DriveGuard-X system contains multiple sensing and intelligence modules.

```text
                         DRIVEGUARD-X
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
   Battery Sensors       IMU Sensors        Microphone
          │                   │                   │
          ▼                   ▼                   ▼
    Battery AI          Driving Behavior      Road Condition
          │                   │                   │
          ▼                   ▼                   ▼
        SOH             Driver Event         Road Event
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │
                              ▼
                 ┌────────────────────────┐
                 │ Causal Attribution      │
                 │ Engine                  │
                 │                        │
                 │ Battery?              │
                 │ Driver?               │
                 │ Road?                 │
                 └───────────┬────────────┘
                             │
                             ▼
                  Adaptive Protection Logic
                             │
                             ▼
                    Motor / PWM Control
                             │
                             ▼
                       EV Prototype
```

The Battery AI therefore contributes:

```text
Battery condition
       ↓
Estimated SOH
       ↓
Protection decision context
```

The final system can combine this information with:

```text
Driver behavior
+
Road condition
+
Battery health
```

to determine the appropriate response to abnormal electrical events.

---

# 32. Example DriveGuard-X Decision Logic

The Battery AI output can be interpreted by the higher-level protection system.

Conceptually:

```text
                 Abnormal Event
                       │
                       ▼
              Causal Attribution
                       │
       ┌───────────────┼───────────────┐
       │               │               │
       ▼               ▼               ▼
    Battery          Driver           Road
    Related         Related         Related
       │               │               │
       ▼               ▼               ▼
  Conservative     Evaluate        Avoid false
  protection       driving         intervention
       │           behavior            │
       └───────────────┼───────────────┘
                       ▼
                Adaptive Response
```

The Battery AI should therefore be treated as a **decision-support component**, rather than as a standalone protection controller.

---

# 33. MATLAB/Simulink Integration Plan

The final Battery AI model will eventually be integrated into the MATLAB/Simulink portion of DriveGuard-X.

The intended simulation architecture is:

```text
             Battery Model
                  │
        ┌─────────┼─────────┐
        │         │         │
     Voltage    Current   Temperature
        │         │         │
        └─────────┼─────────┘
                  │
                  ▼
          Feature Extraction
                  │
                  ▼
           Battery AI Model
                  │
                  ▼
             Estimated SOH
                  │
                  ▼
        Protection Decision
                  │
                  ▼
          Motor / Load Model
```

The simulation will allow different battery-health conditions to be tested before connecting the model to the physical ESP32 system.

---

# 34. Hardware Deployment Concept

The physical DriveGuard-X prototype is expected to use an ESP32-based architecture.

Battery-related sensing can include:

```text
Battery
   │
   ├── Voltage Sensor
   │
   ├── Current Sensor
   │
   └── Temperature Sensor
           │
           ▼
          ESP32
           │
           ▼
     Battery AI Input
```

The predicted SOH can then be transmitted to the main DriveGuard-X controller or software layer.

The hardware prototype is intended primarily to demonstrate the integrated system concept rather than to serve as a certified automotive BMS.

---

# 35. Repository Structure

A recommended repository structure is:

```text
DriveGuard-X-Battery-AI/
│
├── README.md
│
├── notebooks/
│   ├── 01_dataset_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_paper_baseline.ipynb
│   ├── 04_generalized_experiments.ipynb
│   ├── 05_final_model.ipynb
│   └── ...
│
├── models/
│   └── final/
│       ├── driveguard_x_final_battery_rf.joblib
│       ├── final_model_metadata.json
│       ├── final_feature_importance.csv
│       └── feature_schema.json
│
├── results/
│   ├── final_test_predictions.csv
│   ├── final_per_battery_metrics.csv
│   └── comparison_results.csv
│
├── figures/
│   ├── 01_paper_vs_driveguard_xgb_mae.png
│   ├── 02_paper_vs_driveguard_xgb_mse.png
│   ├── 03_B0005_actual_vs_predicted_soh.png
│   ├── 04_B0006_actual_vs_predicted_soh.png
│   ├── 05_B0030_actual_vs_predicted_soh.png
│   ├── 06_B0047_actual_vs_predicted_soh.png
│   ├── 07_B0053_actual_vs_predicted_soh.png
│   └── 08_final_random_forest_feature_importance.png
│
├── docs/
│   └── battery_model_comparison.md
│
└── requirements.txt
```

The large NASA dataset should **not** be committed to the repository.

Instead, provide instructions for obtaining the dataset from NASA/Kaggle.

---

# 36. Reproducibility

The complete development process is contained in the primary Jupyter notebooks.

The workflow covers:

```text
Dataset discovery
       ↓
Metadata analysis
       ↓
Discharge filtering
       ↓
Data quality investigation
       ↓
SOH calculation
       ↓
Feature engineering
       ↓
Paper-compatible baseline
       ↓
Paper comparison
       ↓
Generalized dataset
       ↓
Battery trajectory audit
       ↓
Operating-condition analysis
       ↓
Model training
       ↓
Hyperparameter experiments
       ↓
GroupKFold robustness analysis
       ↓
Final Random Forest selection
       ↓
Untouched-battery evaluation
       ↓
Final graphs
       ↓
Saved model artifacts
```

---

# 37. Requirements

The core Python environment uses libraries including:

```text
numpy
pandas
scikit-learn
xgboost
joblib
matplotlib
```

A `requirements.txt` file can contain:

```text
numpy
pandas
scikit-learn
xgboost
joblib
matplotlib
```

---

# 38. Running the Notebooks

The recommended environment is **Kaggle Notebook** because the NASA dataset contains thousands of individual CSV files and can be accessed directly through the Kaggle dataset input system.

After attaching the dataset:

```text
Run notebooks
      ↓
Dataset discovery
      ↓
Feature extraction
      ↓
Model development
      ↓
Final evaluation
```

The final model artifacts are saved under:

```text
/kaggle/working/driveguard_x_battery_models/
```

The final model is located under:

```text
/kaggle/working/driveguard_x_battery_models/FINAL_BATTERY_MODEL/
```

---

# 39. Important Limitations

The current implementation has several limitations.

## 39.1 Cycle-Level Model

The current model operates on cycle-level features rather than a continuously updated real-time feature window.

A rolling-window deployment version is therefore required for real-time operation.

## 39.2 Dataset Domain

The model is trained and evaluated using the NASA battery aging dataset.

Real-world EV batteries can have different:

- Chemistry
- Pack configurations
- Thermal behavior
- Current profiles
- Aging mechanisms
- Environmental conditions

Therefore, performance on NASA data does not guarantee equivalent performance on a commercial EV battery pack.

## 39.3 Generalization Performance

The final generalized test R² is approximately:

```text
0.368
```

This demonstrates that cross-battery generalization remains challenging.

The model should therefore not be presented as a perfect SOH predictor.

## 39.4 Safety-Critical Usage

The model is a research prototype.

It should not independently control a real vehicle or safety-critical BMS without extensive additional validation, uncertainty analysis, fault handling and automotive-grade verification.

---

# 40. What This Model Successfully Demonstrates

The Battery AI component demonstrates:

- Machine-learning-based SOH estimation
- Cycle-level battery feature engineering
- NASA battery dataset processing
- Research-paper baseline reproduction
- Quantitative comparison with a published methodology
- Battery-level cross-validation
- Operating-condition analysis
- Domain-shift investigation
- Robust model selection
- Unseen-battery evaluation
- Explainable feature-importance analysis
- Preparation for MATLAB/Simulink integration

The primary achievement is therefore not simply the final MAE value.

It is the **complete experimental methodology used to arrive at and evaluate the final model**.

---

# 41. Final Result

The Battery AI development resulted in the following final model:

```text
Model:
Random Forest Regressor

Development:
14 batteries

Final Test:
5 completely unseen batteries

Features:
21 engineered cycle-level features

Final MAE:
0.074921

Final RMSE:
0.092745

Final R²:
0.367663
```

The model is considered suitable for integration into the **DriveGuard-X research prototype** as a battery-health estimation component.

---

# 42. Development Summary

The complete Battery AI development can be summarized as:

```text
                    BASE PAPER
                        │
                        ▼
              Paper-Compatible
                  Experiment
                        │
                        ▼
                XGBoost Baseline
                        │
                        ▼
            Better MAE/MSE than
             reported baseline
                        │
                        ▼
             Dataset Expansion
                        │
                        ▼
             Data Quality Audit
                        │
                        ▼
          Operating-Condition Study
                        │
                        ▼
                Domain Shift
                  Identified
                        │
                        ▼
            Battery-Level GroupKFold
                        │
                        ▼
              Model Robustness
                  Evaluation
                        │
                        ▼
             Random Forest Selected
                        │
                        ▼
             14-Battery Training
                        │
                        ▼
          5 Completely Unseen Batteries
                        │
                        ▼
             Final Model Evaluation
                        │
                        ▼
            DriveGuard-X Battery AI
```

---

# 43. Future Work

The next stage of development will focus on transforming the offline research model into a form suitable for the complete DriveGuard-X system.

Planned work includes:

### 1. Real-Time Battery AI

Convert cycle-level features into rolling-window features that can be calculated from ESP32 sensor data.

### 2. MATLAB/Simulink Integration

Implement the battery model within the DriveGuard-X simulation environment.

### 3. Battery Degradation Simulation

Create simulated battery degradation conditions and evaluate how SOH estimation changes as the simulated battery ages.

### 4. Hardware Integration

Connect:

```text
Voltage
Current
Temperature
       ↓
ESP32
       ↓
Battery AI
       ↓
Estimated SOH
```

### 5. Multi-Model Integration

Combine Battery AI with:

```text
IMU Driving Behavior Model
+
Road Condition Model
+
Battery AI
```

### 6. Causal Attribution

Use the three model outputs to determine whether abnormal events are primarily:

```text
Battery-caused
Driver-caused
Road-caused
```

### 7. Adaptive Protection

Use the causal attribution result and battery condition to determine the appropriate protection response.

---

# 44. Complete DriveGuard-X Vision

The Battery AI is ultimately one part of the larger DriveGuard-X architecture.

```text
                         ┌───────────────────────┐
                         │      DRIVEGUARD-X     │
                         │ Adaptive EV Protection│
                         └───────────┬───────────┘
                                     │
                 ┌───────────────────┼───────────────────┐
                 │                   │                   │
                 ▼                   ▼                   ▼
          ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
          │   Battery   │     │     IMU     │     │ Microphone  │
          │   Sensors   │     │   Sensors   │     │   Sensor    │
          └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
                 │                   │                   │
                 ▼                   ▼                   ▼
          ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
          │  Battery AI │     │ Driving AI  │     │ Road AI     │
          │             │     │             │     │             │
          │ SOH         │     │ Driver      │     │ Surface /   │
          │ estimation  │     │ behavior    │     │ Road event  │
          └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
                 │                   │                   │
                 │                   │                   │
                 └───────────────────┼───────────────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │ Causal Attribution    │
                         │ Engine                │
                         │                       │
                         │ Battery?              │
                         │ Driver?               │
                         │ Road?                 │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │ Adaptive Protection   │
                         │ Logic                 │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │ Motor / PWM Control   │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │ DriveGuard-X Hardware │
                         │ Prototype             │
                         └───────────────────────┘
```

---

# 45. Conclusion

The DriveGuard-X Battery AI module began with a published machine-learning framework for lithium-ion battery SOH estimation and progressively extended it into a more rigorous battery-level generalization study.

The initial paper-compatible experiment demonstrated that the DriveGuard-X XGBoost implementation achieved lower MAE and MSE than the reported XGBoost results for B0006, B0007 and B0018.

The subsequent generalized analysis showed that battery SOH estimation becomes considerably more difficult when batteries operating under different temperature and current conditions are introduced. This led to the adoption of battery-level GroupKFold validation and a more rigorous untouched-battery evaluation strategy.

Random Forest was selected as the final model based on its robustness across the development batteries. The final model achieved an MAE of **0.074921**, RMSE of **0.092745** and R² of **0.367663** on five completely unseen test batteries.

The resulting model is suitable as a **research-grade Battery AI component for the DriveGuard-X prototype**. Its limitations, particularly regarding real-time operation and cross-domain generalization, are explicitly recognized and form part of the future development roadmap.

The next stage is to convert this offline Battery AI model into a deployment-oriented component and integrate it with the IMU-based driving behavior model, road-condition model and causal attribution engine to form the complete DriveGuard-X adaptive protection system.
