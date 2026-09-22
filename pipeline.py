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


logger = logging.getLogger(__name__)

def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    # Set up logging
    logging.basicConfig(
        level=logging.DEBUG if verbose == True else logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
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
        "--format",
        help="Output format: csv or json; default is csv",
        choices=["csv", "json"], 
        default="csv"
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
    setup_logging(verbose = args.verbose)
    logger.debug(f"Arguments parsed: input={args.input}, output={args.output}")
    if validate_input(args.input) == False:
        sys.exit(1)
    try:
        data = load_data(args.input)
    except ValueError:
        sys.exit(1)




if __name__ == "__main__":
    main()