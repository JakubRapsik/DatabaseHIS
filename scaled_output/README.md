# Scaled HIS Dataset Variants

This directory contains scaled variants of the synthetic academic HIS dataset.

The target size refers to the number of rows in `medical_records.csv`. Related tables were scaled proportionally to preserve the structure of the original HIS dataset.

| Variant | medical_cards | medical_records | hospitalizations | examinations |
|---|---:|---:|---:|---:|
| scale_100k | 17347 | 100000 | 100069 | 102759 |
| scale_500k | 86735 | 500000 | 500346 | 513793 |
| scale_1m | 173469 | 1000000 | 1000692 | 1027586 |

## Generation Notes

- Primary identifiers were regenerated sequentially.
- Foreign-key-like references were remapped to valid generated identifiers.
- Dates were deterministically shifted across generation cycles.
- Domain values and statistical patterns were preserved by controlled scaling of the baseline dataset.
