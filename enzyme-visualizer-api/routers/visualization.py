from fastapi import APIRouter, HTTPException
import logging

from models import Variant, ParentSequence, PropertiesList
from services.visualizer import load_variants_data, load_parent_sequence

# Create a new APIRouter instance with a prefix for all routes
router = APIRouter(
    prefix="/visualizer"
)

# Global variables for loaded data.
variants_data: list[Variant] = []
parent_sequence: str = ""

logger = logging.getLogger("uvicorn.error")

@router.on_event("startup")
def startup_event():
    """
    Load the parent sequence and variants data when the API starts.

    Raises:
        HTTPException: If there is an error during startup.
    """
    global parent_sequence, variants_data
    try:
        parent_sequence = load_parent_sequence()
        variants_data = load_variants_data()
        # Sort variants by mutation position.
        variants_data.sort(key=lambda v: v.position)
    except Exception as e:
        logger.error("Startup failed", exc_info=True)
        raise e

@router.get("/parent-sequence", response_model=ParentSequence)
def get_parent():
    """
    Return the parent enzyme sequence.

    Returns:
        ParentSequence: The parent sequence object.

    Raises:
        HTTPException: If the parent sequence is not loaded.
    """
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
    if not variants_data:
        raise HTTPException(status_code=500, detail="Variants data not loaded.")
    return variants_data

@router.get("/properties", response_model=PropertiesList)
def get_properties():
    """
    Return a list of available property names (from the Excel file).

    Returns:
        PropertiesList: An object containing a list of property names.
    """
    if not variants_data:
        return PropertiesList(properties=[])
    # Assumes all variants share the same property keys.
    properties = list(variants_data[0].properties.keys())
    return PropertiesList(properties=properties)