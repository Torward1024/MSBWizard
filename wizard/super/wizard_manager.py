# wizard/super/wizard_manager.py
from typing import Dict, Any
from common.super.super import Super
from common.super.manipulator import Manipulator
from wizard.base.wizard_block import WizardBlock
from wizard.super.wizard_project import WizardProject
from common.utils.logging_setup import logger

class BlockManager(Super):
    """Super-class for managing WizardBlock instances in MSBWizard.

    Handles operations such as creating, updating, deleting, and connecting blocks within a project.

    Attributes:
        _manipulator (Manipulator): Associated Manipulator instance.
        _methods (Dict[Type, Dict[str, Callable]]): Method registry for block operations.
        _operation (str): Operation name ("manage").
    """
    _operation: str = "manage"

    def __init__(self, manipulator: Manipulator = None):
        """Initialize the BlockManager.

        Args:
            manipulator (Manipulator, optional): The Manipulator instance. Defaults to None.
        """
        super().__init__(manipulator=manipulator)
        logger.info("Initialized BlockManager")

    def _manage_wizardblock(self, obj: WizardBlock, attributes: Dict[str, Any] = None) -> Dict[str, Any]:
        """Manage a WizardBlock (create, update, or delete).

        Args:
            obj (WizardBlock): The block to manage.
            attributes (Dict[str, Any], optional): Management attributes (e.g., "action": "create", "update", "delete").

        Returns:
            Dict[str, Any]: Standardized response with status, object, method, result, and error (if any).

        Raises:
            ValueError: If the action is invalid or required attributes are missing.
        """
        if attributes is None:
            attributes = {}
        action = attributes.get("action")
        project = self._manipulator.get_managing_object()

        if not isinstance(project, WizardProject):
            logger.error("Managing object must be a WizardProject")
            return self._build_response(obj, False, "_manage_wizardblock", None, "Invalid managing object")

        try:
            if action == "create":
                project.blocks.add(obj)
                logger.info(f"Created WizardBlock '{obj.name}'")
                return self._build_response(obj, True, "_manage_wizardblock", obj.to_dict())
            elif action == "update":
                if not project.blocks.has_item(obj.name):
                    return self._build_response(obj, False, "_manage_wizardblock", None, f"Block '{obj.name}' not found")
                project.blocks.set_item(obj.name, obj)
                logger.info(f"Updated WizardBlock '{obj.name}'")
                return self._build_response(obj, True, "_manage_wizardblock", obj.to_dict())
            elif action == "delete":
                if not project.blocks.has_item(obj.name):
                    return self._build_response(obj, False, "_manage_wizardblock", None, f"Block '{obj.name}' not found")
                project.blocks.remove(obj.name)
                logger.info(f"Deleted WizardBlock '{obj.name}'")
                return self._build_response(obj, True, "_manage_wizardblock", None)
            else:
                logger.error(f"Invalid action: {action}")
                return self._build_response(obj, False, "_manage_wizardblock", None, f"Invalid action: {action}")
        except Exception as e:
            logger.error(f"Failed to manage WizardBlock '{obj.name}': {str(e)}")
            return self._build_response(obj, False, "_manage_wizardblock", None, str(e))

    def _manage_connections(self, obj: WizardProject, attributes: Dict[str, Any] = None) -> Dict[str, Any]:
        """Manage connections between WizardBlocks.

        Args:
            obj (WizardProject): The project containing the blocks and connections.
            attributes (Dict[str, Any], optional): Connection attributes (e.g., "source": str, "target": str, "action": "connect" or "disconnect").

        Returns:
            Dict[str, Any]: Standardized response with status, object, method, result, and error (if any).

        Raises:
            ValueError: If required attributes are missing or invalid.
        """
        if attributes is None:
            attributes = {}
        action = attributes.get("action")
        source = attributes.get("source")
        target = attributes.get("target")

        if not source or not target:
            logger.error("Source and target must be provided for connection management")
            return self._build_response(obj, False, "_manage_connections", None, "Missing source or target")

        try:
            if action == "connect":
                if source not in obj.blocks:
                    return self._build_response(obj, False, "_manage_connections", None, f"Source block '{source}' not found")
                if target not in obj.blocks:
                    return self._build_response(obj, False, "_manage_connections", None, f"Target block '{target}' not found")
                if source not in obj.connections:
                    obj.connections[source] = []
                if target not in obj.connections[source]:
                    obj.connections[source].append(target)
                    obj.blocks[source].connections.append(target)
                    logger.info(f"Connected block '{source}' to '{target}'")
                return self._build_response(obj, True, "_manage_connections", obj.connections)
            elif action == "disconnect":
                if source not in obj.connections or target not in obj.connections[source]:
                    return self._build_response(obj, False, "_manage_connections", None, f"No connection between '{source}' and '{target}'")
                obj.connections[source].remove(target)
                obj.blocks[source].connections.remove(target)
                logger.info(f"Disconnected block '{source}' from '{target}'")
                return self._build_response(obj, True, "_manage_connections", obj.connections)
            else:
                logger.error(f"Invalid action: {action}")
                return self._build_response(obj, False, "_manage_connections", None, f"Invalid action: {action}")
        except Exception as e:
            logger.error(f"Failed to manage connections: {str(e)}")
            return self._build_response(obj, False, "_manage_connections", None, str(e))