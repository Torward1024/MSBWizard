# wizard/super/wizard_project.py
from typing import Dict, Any, Optional, List
from common.super.project import Project
from wizard.base.wizard_block import WizardBlock
from wizard.base.code_template import CodeTemplate
from wizard.base.wizard_container import WizardContainer
from wizard.base.template_container import TemplateContainer
from common.utils.validation import check_non_empty_string
from common.utils.logging_setup import logger

class WizardProject(Project):
    """Project class for managing MSBWizard configurations.

    Attributes:
        name (str): Project name.
        blocks (WizardContainer): Container for visual blocks.
        templates (TemplateContainer): Container for code templates.
        connections (Dict[str, List[str]]): Mapping of block names to their connected blocks.
        _item_type (Type[BaseEntity]): Type of items (WizardBlock).
    """
    name: str
    blocks: WizardContainer
    templates: TemplateContainer
    connections: Dict[str, List[str]]
    _item_type = WizardBlock

    def __init__(self, name: str = "WIZARD_PROJECT", blocks: Dict[str, WizardBlock] = None,
                 templates: Dict[str, CodeTemplate] = None, connections: Dict[str, List[str]] = None):
        check_non_empty_string(name, "WizardProject name")
        super().__init__(name=name)
        self.blocks = WizardContainer(items=blocks, name=f"{name}_blocks")

        default_template = CodeTemplate(
            name="default_project_template",
            template="""# Generated MSB Project: {{project_name}}
from common.base.baseentity import BaseEntity
from common.base.basecontainer import BaseContainer

{% for name, block in blocks.items() %}
class {{block.type | capitalize}}(BaseEntity):
    name: str
    {% for attr_name, attr_value in block.attributes.items() %}
    {{attr_name}}: {{attr_value.__class__.__name__}}
    {% endfor %}
{% endfor %}
""",
            block_type="project"
        )
        templates = templates or {"default_project_template": default_template}
        self.templates = TemplateContainer(items=templates, name=f"{name}_templates")
        self.connections = connections or {}
        logger.info(f"Initialized WizardProject '{name}' with {len(self.blocks)} blocks and {len(self.templates)} templates")

    def create_item(self, item_code: str = "BLOCK_DEFAULT", isactive: bool = True) -> None:
        """Create and add a new WizardBlock to the project."""
        block = WizardBlock(name=item_code, block_type="entity", isactive=isactive)
        self.add_item(block)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WizardProject':
        """Create a WizardProject from a dictionary."""
        blocks = {k: WizardBlock.from_dict(v) for k, v in data.get("blocks", {}).items()}
        templates = {k: CodeTemplate.from_dict(v) for k, v in data.get("templates", {}).items()}
        return cls(
            name=data.get("name", "WIZARD_PROJECT"),
            blocks=blocks,
            templates=templates,
            connections=data.get("connections", {})
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the project to a dictionary."""
        return {
            "name": self.name,
            "blocks": self.blocks.to_dict(),
            "templates": self.templates.to_dict(),
            "connections": self.connections
        }