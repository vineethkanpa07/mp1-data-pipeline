# MP1 Data Pipeline

This project is a data cleaning pipeline that first loads a CSV file, then validates and cleans it based on configuration settings specified in a YAML file, and finally saves the cleaned result as a new CSV. Data moves through the pipeline in a set order: the input and configuration files are checked and loaded, the data is validated, it is cleaned by removing duplicates, missing values, and outliers, and the final dataframe is saved along with a cleaning report. `pipeline.py` is the starting point, parsing command-line arguments and coordinating each step through the functions in the `src` package. `src/utils.py` handles shared setup tasks like checking that input files exist and configuring logging. `src/data_loaders.py` reads the CSV and YAML files, and `src/data_validator.py` confirms that required columns are present and removes rows with invalid numeric values. `src/data_processor.py` applies the cleaning steps enabled in `config/config.yaml` and builds the cleaning report, while `src/data_output.py` creates the output folder and saves the cleaned data. Because the cleaning rules are in the config file, the pipeline can be adjusted for different datasets without changing the code.

## Example Usage

Run the pipeline on the provided sample data:

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

Output:

```
DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, output=output/clean.csv, config=config/config.yaml
INFO     src.utils — Input file validated: fixtures/sample_data.csv
INFO     src.utils — Input file validated: config/config.yaml
INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
INFO     src.data_loaders — Loaded YAML file: config/config.yaml
WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
DEBUG    src.data_validator — Valid rows: 98, removed rows: 2
INFO     __main__ — Validation complete: 100 -> 98 rows
DEBUG    src.data_processor — 2 rows removed.
DEBUG    src.data_processor — 2 rows removed.
DEBUG    src.data_processor — Method used: iqr, Threshold: 1.5, 2 rows removed.
INFO     __main__ — Processing complete: 6 rows and 0 columns removed.
DEBUG    src.data_output — Saved 92 rows to output/clean.csv
INFO     __main__ — Saved cleaned data to output/clean.csv (92 rows).
Cleaning report:
  rows_before: 98
  rows_after: 92
  rows_removed: 6
  columns_before: 5
  columns_after: 5
  columns_removed: 0
'''

## Example Usage

Run the pipeline on the provided sample data:

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

Output:

```
DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, output=output/clean.csv, config=config/config.yaml
INFO     src.utils — Input file validated: fixtures/sample_data.csv
INFO     src.utils — Input file validated: config/config.yaml
INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
INFO     src.data_loaders — Loaded YAML file: config/config.yaml
WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
DEBUG    src.data_validator — Valid rows: 98, removed rows: 2
INFO     __main__ — Validation complete: 100 -> 98 rows
DEBUG    src.data_processor — 2 rows removed.
DEBUG    src.data_processor — 2 rows removed.
DEBUG    src.data_processor — Method used: iqr, Threshold: 1.5, 2 rows removed.
INFO     __main__ — Processing complete: 6 rows and 0 columns removed.
DEBUG    src.data_output — Saved 92 rows to output/clean.csv
INFO     __main__ — Saved cleaned data to output/clean.csv (92 rows).
Cleaning report:
  rows_before: 98
  rows_after: 92
  rows_removed: 6
  columns_before: 5
  columns_after: 5
  columns_removed: 0
```