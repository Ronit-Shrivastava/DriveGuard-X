# Battery Model Artifacts

Copy the following artifacts from the Kaggle notebook output into this folder:

- `driveguard_x_final_battery_rf.joblib`
- `final_model_metadata.json`
- `feature_schema.json`

The model was trained as a cycle-level Random Forest regressor.

The current final feature schema contains 21 engineered features:

1. voltage_initial
2. voltage_final
3. voltage_min
4. voltage_max
5. voltage_mean
6. voltage_std
7. voltage_drop
8. current_mean
9. current_min
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

Do not commit large raw NASA datasets to the repository.
