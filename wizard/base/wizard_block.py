# wizard/base/wizard_block.py
from typing import Dict, Any, List, Tuple
from common.base.baseentity import BaseEntity
from common.utils.logging_setup import logger

class WizardBlock(BaseEntity):
    """Base entity representing a visual block in MSBWizard.

    Attributes:
        name (str): Unique identifier for the block.
        block_type (str): Type of block ("entity", "container", "operation", "project").
        attributes (Dict[str, Any]): Block attributes (e.g., fields for entities or operation parameters).
        position (Tuple[int, int]): Position of the block on the canvas (x, y).
        connections (List[str]): List of names of connected blocks.
        isactive (bool): Activation status of the block.
    """
    name: str
    block_type: str
    attributes: Dict[str, Any]
    position: Tuple[int, int]
    connections: List[str]
    isactive: bool

    def __init__(self, name: str, block_type: str, attributes: Dict[str, Any] = None,
                 position: Tuple[int, int] = (0, 0), connections: List[str] = None,
                 isactive: bool = True, use_cache: bool = False):
        """Initialize a WizardBlock with specified attributes."""
        if block_type not in ("entity", "container", "operation", "project"):
            raise ValueError(f"Invalid block_type: {block_type}")
        super().__init__(
            name=name,
            isactive=isactive,
            block_type=block_type,
            attributes=attributes or {},
            position=position,
            connections=connections or [],
            use_cache=use_cache
        )
        logger.info(f"Initialized WizardBlock '{name}' of type '{block_type}'")