from fastapi import APIRouter, HTTPException
from models import Variant, ParentSequence
from utils.datahandler import load_variants_data, load_parent_sequence

# Create a new APIRouter instance with a prefix for all routes
router = APIRouter(
    prefix="/visualizer"
)

@router.get("/parent-sequence", response_model=ParentSequence)
def get_parent():
    """
    Return the parent enzyme sequence.

    Returns:
        ParentSequence: The parent sequence object.

    Raises:
        HTTPException: If the parent sequence is not loaded.
    """
    parent_sequence = load_parent_sequence()
    if not parent_sequence:
        raise HTTPException(status_code=500, detail="Parent sequence not loaded.")
    return ParentSequence(sequence=parent_sequence)

@router.get("/variants", response_model=list[Variant])
def get_variants():
    """
    Return a list of variants with parsed mutation information.

    Returns:
        list[Variant]: A list of Variant objects.

    Raises:
        HTTPException: If the variants data is not loaded.
    """
    variants_data = load_variants_data()
    # Sort variants by mutation position.
    variants_data.sort(key=lambda v: v.position)
    if not variants_data:
        raise HTTPException(status_code=500, detail="Variants data not loaded.")
    return variants_data