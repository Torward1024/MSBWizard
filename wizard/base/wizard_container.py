# wizard/base/wizard_container.py
from typing import Dict, Optional
from common.base.basecontainer import BaseContainer
from wizard.base.wizard_block import WizardBlock
from common.utils.logging_setup import logger

class WizardContainer(BaseContainer[WizardBlock]):
    """Container for storing WizardBlock instances in MSBWizard.

    Attributes:
        name (str): Container name.
        _items (Dict[str, WizardBlock]): Dictionary of blocks indexed by name.
        isactive (bool): Activation status.
        _use_cache (bool): Cache flag for serialization.
    """
    name: str
    _items: Dict[str, WizardBlock]
    isactive: bool
    _use_cache: bool

    def __init__(self, items: Dict[str, WizardBlock] = None, name: str = None,
                 isactive: bool = True, use_cache: bool = False):
        """Initialize the WizardBlockContainer."""
        super().__init__(items=items, name=name, isactive=isactive, use_cache=use_cache)

    def _validate_item(self, item: WizardBlock) -> None:
        """Validate a WizardBlock item."""
        if not isinstance(item, WizardBlock):
            raise TypeError(f"Item must be WizardBlock, got {type(item).__name__}")
        logger.debug(f"Validated WizardBlock '{item.name}'")