# wizard/super/wizard_generator.py
from typing import Dict, Any, Optional
from common.super.super import Super
from common.super.manipulator import Manipulator
from wizard.super.wizard_project import WizardProject
from wizard.base.wizard_block import WizardBlock
from common.utils.logging_setup import logger
from jinja2 import Template

class CodeGenerator(Super):
    """Super-class for generating Python code from MSBWizard configurations using Jinja2."""
    _operation: str = "generate"

    def __init__(self, manipulator: Manipulator = None):
        super().__init__(manipulator=manipulator)
        logger.info("Initialized CodeGenerator")

    def _generate_wizardproject(self, obj: WizardProject, attributes: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate Python code for a WizardProject, creating custom classes for each block."""
        if attributes is None:
            attributes = {}
        template_name = attributes.get("template", "default_project_template")
        template = obj.templates.get(template_name)
        if not template:
            logger.error(f"Template '{template_name}' not found")
            return self._build_response(obj, False, "_generate_wizardproject", None, f"Template '{template_name}' not found")

        try:
            jinja_template = Template(template.template)
            code = jinja_template.render(
                project_name=obj.name,
                blocks=[{
                    "name": block.name,
                    "base_class": block.base_class,
                    "block_type": block.block_type,
                    "position": block.position,
                    "connections": block.connections,
                    "attributes": block.to_dict()  # Pass all block attributes
                } for block in obj.blocks.get_all().values()],
                connections=obj.connections
            )
            logger.info(f"Generated code for project '{obj.name}' with {len(obj.blocks.get_all())} classes")
            return self._build_response(obj, True, "_generate_wizardproject", code)
        except Exception as e:
            logger.error(f"Failed to render template '{template_name}': {str(e)}")
            return self._build_response(obj, False, "_generate_wizardproject", None, str(e))

    def _generate_wizardblock(self, obj: WizardBlock, attributes: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate Python code for a single WizardBlock as a custom class."""
        if attributes is None:
            attributes = {}
        template_name = attributes.get("template", f"{obj.block_type}_template")
        project = self._manipulator.get_managing_object()
        template = project.templates.get(template_name) if isinstance(project, WizardProject) else None
        if not template:
            logger.error(f"Template '{template_name}' not found")
            return self._build_response(obj, False, "_generate_wizardblock", None, f"Template '{template_name}' not found")

        try:
            jinja_template = Template(template.template)
            code = jinja_template.render(
                block_name=obj.name,
                base_class=obj.base_class,
                block_type=obj.block_type,
                position=obj.position,
                connections=obj.connections,
                attributes=obj.to_dict()
            )
            logger.info(f"Generated code for block '{obj.name}' as class '{obj.name}({obj.base_class})'")
            return self._build_response(obj, True, "_generate_wizardblock", code)
        except Exception as e:
            logger.error(f"Failed to render template '{template_name}': {str(e)}")
            return self._build_response(obj, False, "_generate_wizardblock", None, str(e))