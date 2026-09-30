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
from data_loaders import load_data
from data_processor import process_data, create_cleaning_report




logger = logging.getLogger(__name__)

def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    # Set up logging
    logging.basicConfig(
        level=logging.DEBUG if verbose == True else logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S")


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


def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    if Path(filepath).is_file() == True:
        logger.info(f"Input file validated: {filepath}")
        return True

    if Path(filepath).is_file() == False:
        logger.error(f"Input file not found: {filepath}")
        return False
    
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

    cleaned = process_data(data, config)

    report = create_cleaning_report(data, cleaned)

    logger.info(
        f"Processing complete: {report['rows_removed']} rows and "
        f"{report['columns_removed']} columns removed."
    )

    cleaned.to_csv(args.output, index=False)
    logger.info(f"Saved cleaned data to {args.output} ({len(cleaned)} rows).")

    print("Cleaning report:")
    for key, value in report.items():
        print(f"  {key}: {value}")



if __name__ == "__main__":
    main()