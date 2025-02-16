import os

# Define paths relative to this file.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
PARENT_FASTA_PATH = os.path.join(DATA_DIR, "parent.fasta")
VARIANTS_XLSX_PATH = os.path.join(DATA_DIR, "variants.xlsx")
