# wizard/super/wizard_manipulator.py
from typing import Optional
from common.super.manipulator import Manipulator
from wizard.base.wizard_block import WizardBlock
from wizard.base.wizard_container import WizardContainer
from wizard.base.template_container import TemplateContainer
from wizard.super.wizard_project import WizardProject
from wizard.super.wizard_generator import CodeGenerator
from wizard.super.wizard_manager import BlockManager
from wizard.super.wizard_ui_manager import UIManager
from common.utils.logging_setup import logger
from PySide6.QtWidgets import QGraphicsScene

class WizardManipulator(Manipulator):
    """Manipulator for managing MSBWizard operations.

    Attributes:
        _managing_object (WizardProject): The managed project.
        _base_classes (List[Type]): Supported types.
        _operations (Dict[str, Callable]): Registered operations.
    """
    def __init__(self, managing_object: Optional[WizardProject] = None, scene: Optional[QGraphicsScene] = None):
        """Initialize the WizardManipulator."""
        base_classes = [WizardBlock, WizardContainer, WizardProject, TemplateContainer]
        super().__init__(managing_object=managing_object, base_classes=base_classes)
        self.register_operation("manage", BlockManager(manipulator=self))
        self.register_operation("generate", CodeGenerator(manipulator=self))
        self.register_operation("render", UIManager(manipulator=self, scene=scene))
        logger.info("Initialized WizardManipulator")