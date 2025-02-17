from fastapi import APIRouter, HTTPException, Request
from models import Variant, ParentSequence, PropertiesList
from utils.datahandler import load_variants_data, load_parent_sequence

# Create a new APIRouter instance with a prefix for all routes
router = APIRouter(
    prefix="/visualizer"
)

@router.get("/parent-sequence", response_model=ParentSequence)
def get_parent(request: Request):
    """
    Return the parent enzyme sequence.

    Returns:
        ParentSequence: The parent sequence object.

    Raises:
        HTTPException: If the parent sequence is not loaded.
    """
    if not request.app.state.parent_sequence:
        raise HTTPException(status_code=500, detail="Parent sequence not loaded.")
    return ParentSequence(sequence=request.app.state.parent_sequence)

@router.get("/variants", response_model=list[Variant])
def get_variants(request: Request):
    """
    Return a list of variants with parsed mutation information.

    Returns:
        list[Variant]: A list of Variant objects.

    Raises:
        HTTPException: If the variants data is not loaded.
    """
    if not request.app.state.variants_data:
        raise HTTPException(status_code=500, detail="Variants data not loaded.")
    return request.app.state.variants_data