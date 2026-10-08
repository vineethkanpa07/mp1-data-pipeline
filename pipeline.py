"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --output clean.csv
    python pipeline.py --input data.csv --output results.json --format json --verbose

"""

import argparse
import logging
import sys
from pathlib import Path
from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)


logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""

# Create an ArgumentParser
    parser = argparse.ArgumentParser(
        description="Analyze a data file"
    )

    # Add a named argument (required)
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to input file"
    )

    # Add named arguments (optional)
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Path to the output file")

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to the yaml configuration file"
    )

    args = parser.parse_args()

    return args
    
def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(verbose=args.verbose)
    logger.debug(
        f"Arguments parsed: input={args.input}, output={args.output}, config={args.config}"
    )

    if validate_input(args.input) == False:
        sys.exit(1)
    if validate_input(args.config) == False:
        sys.exit(1)

    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError as e:
        logger.error(f"Failed to load file: {e}")
        sys.exit(1)

    required_columns = config["validation"]["required_columns"]
    numeric_columns = config["validation"]["numeric_columns"]

    try:
        validated = validate_dataframe(data, required_columns, numeric_columns)
    except ValueError:
        sys.exit(1)

    logger.info(f"Validation complete: {len(data)} -> {len(validated)} rows")
    
    cleaned = process_data(validated, config)

    report = create_cleaning_report(validated, cleaned)

    logger.info(
        f"Processing complete: {report['rows_removed']} rows and "
        f"{report['columns_removed']} columns removed."
    )

    output_path = save_data(cleaned, args.output)
    logger.info(f"Saved cleaned data to {output_path} ({len(cleaned)} rows).")

    print("Cleaning report:")
    for key, value in report.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    main()