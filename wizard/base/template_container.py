# wizard/base/template_container.py
from typing import Dict, Optional
from common.base.basecontainer import BaseContainer
from wizard.base.code_template import CodeTemplate
from common.utils.logging_setup import logger

class TemplateContainer(BaseContainer[CodeTemplate]):
    """Container for storing CodeTemplate instances in MSBWizard.

    Manages a collection of code templates used for generating Python code, ensuring type safety and validation.

    Attributes:
        name (str): Container name.
        _items (Dict[str, CodeTemplate]): Dictionary of templates indexed by name.
        isactive (bool): Activation status of the container.
        _use_cache (bool): Cache flag for serialization.
    """
    name: str
    _items: Dict[str, CodeTemplate]
    isactive: bool
    _use_cache: bool

    def __init__(self, items: Dict[str, CodeTemplate] = None, name: str = None,
                 isactive: bool = True, use_cache: bool = False):
        """Initialize the TemplateContainer with optional items and name.

        Args:
            items (Dict[str, CodeTemplate], optional): Initial dictionary of templates.
            name (str, optional): Container name. Defaults to None.
            isactive (bool): Activation status. Defaults to True.
            use_cache (bool): Enable caching for serialization. Defaults to False.

        Raises:
            TypeError: If items or their values do not match CodeTemplate type.
            ValueError: If template names do not match dictionary keys.
        """
        super().__init__(items=items, name=name, isactive=isactive, use_cache=use_cache)
        logger.info(f"Initialized TemplateContainer '{name}' with {len(self._items)} templates")

    def _validate_item(self, item: CodeTemplate) -> None:
        """Validate a CodeTemplate item.

        Args:
            item (CodeTemplate): The template to validate.

        Raises:
            TypeError: If the item is not a CodeTemplate.
            ValueError: If the template content is invalid (e.g., empty).
        """
        if not isinstance(item, CodeTemplate):
            raise TypeError(f"Item must be CodeTemplate, got {type(item).__name__}")
        if not item.template:
            raise ValueError(f"Template '{item.name}' has empty content")
        logger.debug(f"Validated CodeTemplate '{item.name}'")