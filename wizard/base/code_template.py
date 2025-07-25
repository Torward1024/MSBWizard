# wizard/base/code_template.py
from typing import Dict, Any
from common.base.baseentity import BaseEntity
from common.utils.logging_setup import logger

class CodeTemplate(BaseEntity):
    """Base entity representing a code template for Python code generation in MSBWizard.

    Attributes:
        name (str): Unique identifier for the template.
        template (str): The template content (e.g., Jinja2 template string).
        block_type (str): Type of block the template applies to ("entity", "container", "operation", "project").
        isactive (bool): Activation status of the template.
    """
    name: str
    template: str
    block_type: str
    isactive: bool

    def __init__(self, name: str, template: str, block_type: str, isactive: bool = True, use_cache: bool = False):
        """Initialize a CodeTemplate with specified attributes.

        Args:
            name (str): Template name.
            template (str): Template content.
            block_type (str): Type of block the template applies to.
            isactive (bool): Activation status. Defaults to True.
            use_cache (bool): Enable caching for serialization. Defaults to False.

        Raises:
            ValueError: If block_type is invalid or template is empty.
        """
        if block_type not in ("entity", "container", "operation", "project"):
            raise ValueError(f"Invalid block_type: {block_type}")
        if not template:
            raise ValueError(f"Template content cannot be empty")
        super().__init__(
            name=name,
            template=template,
            block_type=block_type,
            isactive=isactive,
            use_cache=use_cache
        )
        logger.info(f"Initialized CodeTemplate '{name}' for block_type '{block_type}'")