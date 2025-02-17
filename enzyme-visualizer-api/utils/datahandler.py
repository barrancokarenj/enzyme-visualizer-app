import logging
import pandas
import re

from common import PARENT_FASTA_PATH, VARIANTS_XLSX_PATH, logger
from models import Variant

def load_parent_sequence() -> str:
    """Load the parent enzyme sequence from a FASTA file."""
    logger.error(f"Failed to load parent sequence: {PARENT_FASTA_PATH}")
    try:
        with open(PARENT_FASTA_PATH, "r") as file:
            lines = file.readlines()
        # Ignore FASTA header lines (starting with ">")
        sequence = "".join(line.strip() for line in lines if not line.startswith(">"))
        if not sequence:
            raise ValueError("Parent sequence is empty.")
        return sequence
    except Exception as e:
        logger.error(f"Failed to load parent sequence: {e}")
        raise e

def parse_mutation(mutation_str: str) -> dict:
    """
    Parse a mutation string.

    The expected format is for example:
        A123C+D234E
    For this task (one mutation per variant) if a plus sign is found,
    only the first mutation (e.g. 'A123C') is used.
    """
    parts = mutation_str.split("+")
    if len(parts) > 1:
        logger.warning(f"Multiple mutations found in '{mutation_str}'. Using the first mutation only.")
    mutation_part = parts[0].strip()
    pattern = r"^([A-Z])(\d+)([A-Z])$"
    match = re.match(pattern, mutation_part)
    if match:
        wild_type, pos, mutant = match.groups()
        return {"wild_type": wild_type, "position": int(pos), "mutant": mutant}
    else:
        raise ValueError(f"Invalid mutation format: {mutation_str}")

def load_variants_data() -> list[Variant]:
    """Load variants from an Excel file, parse mutations, and handle missing property values."""
    try:
        df = pandas.read_excel(VARIANTS_XLSX_PATH, engine="openpyxl")
    except Exception as e:
        logger.error(f"Failed to read Excel file: {e}")
        raise e

    required_columns = {"ID", "Mutation"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in variants file: {missing}")

    # The remaining columns are treated as property columns.
    property_columns = [col for col in df.columns if col not in ["ID", "Mutation"]]
    variants_list = []

    for _, row in df.iterrows():
        mutation_value = row.get("Mutation")
        if pandas.isna(mutation_value):
            logger.warning(f"Skipping variant with missing mutation. Identifier: {row.get('ID')}")
            continue

        mutation_str = str(mutation_value).strip()
        try:
            mutation_info = parse_mutation(mutation_str)
        except ValueError as e:
            logger.warning(f"Skipping variant due to mutation parsing error: {e}")
            continue

        variant = Variant(
            id=row["ID"],
            mutation=mutation_str,
            position=mutation_info["position"],
            wild_type=mutation_info["wild_type"],
            mutant=mutation_info["mutant"],
            properties={prop: (row[prop] if not pandas.isna(row[prop]) else None) for prop in property_columns},
        )
        variants_list.append(variant)
    return variants_list
