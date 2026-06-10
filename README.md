# DatabaseHIS

DatabaseHIS is an academic Hospital Information System (HIS) database created for research, education, and experimentation with relational database design.

The database models a broad healthcare environment, including hospitals, departments, patients, employees, medical records, hospitalizations, examinations, prescriptions, vehicles, dispatching, incidents, pharmacy stock, notifications, and supporting reference data.

## Purpose

This repository contains an academic database export intended for:

- relational database modeling and analysis
- SQL query development and optimization
- data integration and transformation exercises
- database import/export testing
- research-oriented experiments over a healthcare-style information system

The data is designed for academic use. It should be treated as a synthetic or educational dataset, not as a production medical system.

## Repository Contents

The repository includes:

- `DatabaseScript.ddl` - database schema definition script
- `README.md` - project documentation
- `*.csv` - table-level CSV exports
- `generate_scaled_his_datasets.py` - script for generating scaled dataset variants
- `scaled_output/` - generated baseline and scaled CSV subsets

Each CSV file represents one database table. CSV file names are written in English `snake_case` for repository readability. The schema script may still use the original database table names.

## Dataset Scope

The exported tables cover multiple functional areas of a hospital information system:

- Healthcare entities: patients, employees, hospitals, departments, rooms, beds, medical records, examinations, diagnoses, and hospitalizations
- Medication and pharmacy data: medicines, active substances, prescriptions, stock, orders, reservations, and expiration tracking
- Dispatch and emergency operations: vehicles, calls, incidents, dispatchers, routes, trips, vehicle equipment, service records, and failures
- Communication and notifications: user accounts, chat groups, chat messages, user messages, notifications, and notification types
- Geographic and reference data: regions, districts, cities, insurance companies, event types, employee types, diseases, disabilities, vaccines, and auxiliary lists
- Experiment and audit data: experiment plans, experiment runs, logs, error rates, and change tracking

## Time-Evolving Database

DatabaseHIS is designed as a database that evolves over time. The dataset includes entities and records that represent changing states, historical events, and operational updates.

Examples of time-dependent or evolving data include:

- hospitalizations and patient-bed assignments
- examinations and medical record entries
- prescriptions, medicine reservations, and stock movements
- vehicle trips, incidents, failures, service events, and route plans
- notifications, chat messages, calls, logs, and tracked changes
- experiment runs and generated outputs

This makes the dataset suitable for studying temporal behavior in relational databases, such as historical queries, event tracking, state transitions, and long-running operational workflows.

## File Format

The data is exported as CSV files.

General expectations:

- one CSV file corresponds to one database table
- the first row may contain column names, depending on the export source
- values are intended to be imported into the schema defined in `DatabaseScript.ddl`
- some tables may be empty if no records were generated for that part of the model

## Suggested Usage

Typical usage workflow:

1. Create a new database in the target database system.
2. Execute `DatabaseScript.ddl` to create the schema.
3. Import the CSV files into their matching tables.
4. Validate primary keys, foreign keys, and import order if constraints are enabled.
5. Run analytical, experimental, or educational SQL queries over the imported data.

When importing into a relational database, table dependencies may require importing reference tables before transactional tables.

## Scaled Dataset Variants

The repository also contains generated scaled subsets in `scaled_output/`.

Available variants:

- `baseline` - original selected source tables used by the generator
- `scale_100k` - scaled to 100,000 rows in `medical_records.csv`
- `scale_500k` - scaled to 500,000 rows in `medical_records.csv`
- `scale_1m` - scaled to 1,000,000 rows in `medical_records.csv`

The scaled variants include:

- `medical_cards.csv`
- `medical_records.csv`
- `hospitalizations.csv`
- `examinations.csv`

Large CSV files inside `scaled_output/` are tracked with Git LFS because some generated files exceed GitHub's regular 100 MB file limit.

To regenerate the scaled datasets:

```bash
py generate_scaled_his_datasets.py --input-dir . --output-dir scaled_output
```

## Notes

- This repository is maintained for academic and research purposes.
- The structure and dataset may change over time as the database model develops.
- New tables, updated exports, or revised schema definitions may be added in future versions.
- The dataset should not be interpreted as a real hospital production export.

## License

No explicit license has been defined yet. Until a license is added, reuse should be limited to academic review and repository-owner-approved purposes.
