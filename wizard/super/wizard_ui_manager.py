# wizard/super/wizard_ui_manager.py
from typing import Dict, Any, Optional, Tuple
from common.super.super import Super
from common.super.manipulator import Manipulator
from wizard.base.wizard_block import WizardBlock
from wizard.super.wizard_project import WizardProject
from common.utils.logging_setup import logger
from PySide6.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QFont

class UIManager(Super):
    """Super-class for managing PySide6-based UI rendering in MSBWizard.

    Handles rendering of WizardBlocks and their connections on a QGraphicsScene, with drag-and-drop support.

    Attributes:
        _manipulator (Manipulator): Associated Manipulator instance.
        _methods (Dict[Type, Dict[str, Callable]]): Method registry for UI operations.
        _operation (str): Operation name ("render").
        _scene (QGraphicsScene): PySide6 graphics scene for rendering blocks.
        _block_items (Dict[str, QGraphicsRectItem]): Mapping of block names to their rendered items.
        _connection_lines (Dict[Tuple[str, str], QGraphicsLineItem]): Mapping of (source, target) to connection lines.
    """
    _operation: str = "render"

    def __init__(self, manipulator: Manipulator = None, scene: QGraphicsScene = None):
        """Initialize the UIManager."""
        super().__init__(manipulator=manipulator)
        if scene is None:
            raise ValueError("QGraphicsScene must be provided")
        self._scene = scene
        self._block_items = {}
        self._connection_lines = {}
        logger.info(f"Initialized UIManager with scene ID: {id(self._scene)}")
    
    def _render_wizardproject(self, obj: WizardProject, attributes: Dict[str, Any] = None) -> Dict[str, Any]:
        """Render or refresh all WizardBlocks and connections in a WizardProject on the PySide6 canvas."""
        if attributes is None:
            attributes = {}
        try:
            self._scene.clear()
            self._block_items.clear()
            self._connection_lines.clear()

            width = attributes.get("width", 100)
            height = attributes.get("height", 50)
            for block in obj.blocks.get_all().values():
                x, y = block.position
                block_item = QGraphicsRectItem(x, y, width, height)
                block_item.setFlag(QGraphicsRectItem.ItemIsMovable, True)
                block_item.setToolTip(f"{block.name} ({block.block_type})")
                # Add background color for visibility
                block_item.setBrush(QBrush(QColor(200, 200, 255)))
                text_item = QGraphicsTextItem(block.name, block_item)
                text_item.setFont(QFont("Arial", 10))
                text_rect = text_item.boundingRect()
                text_x = (width - text_rect.width()) / 2
                text_y = (height - text_rect.height()) / 2
                text_item.setPos(text_x, text_y)
                logger.debug(f"Project block '{block.name}': pos=({x}, {y}), size={width}x{height}, text_rect={text_rect.width()}x{text_rect.height()}, text_pos=({text_x}, {text_y})")
                self._scene.addItem(block_item)
                self._block_items[block.name] = block_item

            for source, targets in obj.connections.items():
                for target in targets:
                    if source in self._block_items and target in self._block_items:
                        self._render_connection(source, target)

            logger.info(f"Rendered WizardProject '{obj.name}' with {len(self._block_items)} blocks")
            self._scene.update()
            return self._build_response(obj, True, "_render_wizardproject", None)
        except Exception as e:
            logger.error(f"Failed to render WizardProject '{obj.name}': {str(e)}")
            return self._build_response(obj, False, "_render_wizardproject", None, str(e))

    def _render_wizardblock(self, obj: WizardBlock, attributes: Dict[str, Any] = None) -> Dict[str, Any]:
        """Render a WizardBlock on the PySide6 canvas, handling add, remove, or refresh actions."""
        if attributes is None:
            attributes = {}
        action = attributes.get("action", "add")
        logger.debug(f"Processing render action '{action}' for WizardBlock '{obj.name}'")

        try:
            if action == "add":
                return self._add_wizardblock(obj, attributes)
            elif action == "remove":
                return self._remove_wizardblock(obj, attributes)
            elif action == "refresh":
                return self._refresh_wizardblock(obj, attributes)
            else:
                logger.error(f"Unsupported render action: {action}")
                return self._build_response(obj, False, "_render_wizardblock", None, f"Unsupported action: {action}")
        except Exception as e:
            logger.error(f"Failed to process render action '{action}' for WizardBlock '{obj.name}': {str(e)}")
            return self._build_response(obj, False, "_render_wizardblock", None, str(e))

    def _add_wizardblock(self, obj: WizardBlock, attributes: Dict[str, Any] = None) -> Dict[str, Any]:
        """Add a WizardBlock to the PySide6 canvas."""
        if attributes is None:
            attributes = {}
        width = attributes.get("width", 100)
        height = attributes.get("height", 50)

        try:
            # Remove existing block to prevent duplication
            if obj.name in self._block_items:
                logger.debug(f"Block '{obj.name}' already exists in _block_items, removing before re-rendering")
                self._scene.removeItem(self._block_items[obj.name])
                del self._block_items[obj.name]

            x, y = obj.position
            block_item = QGraphicsRectItem(x, y, width, height)
            block_item.setFlag(QGraphicsRectItem.ItemIsMovable, True)
            block_item.setToolTip(f"{obj.name} ({obj.block_type})")
            # Add background color for visibility
            block_item.setBrush(QBrush(QColor(200, 200, 255)))
            text_item = QGraphicsTextItem(obj.name, block_item)
            text_item.setFont(QFont("Arial", 10))
            text_rect = text_item.boundingRect()
            text_x = (width - text_rect.width()) / 2
            text_y = (height - text_rect.height()) / 2
            text_item.setPos(text_x, text_y)
            logger.debug(f"Added block '{obj.name}': pos=({x}, {y}), size={width}x{height}, text_rect={text_rect.width()}x={text_rect.height()}, text_pos=({text_x}, {text_y})")
            self._scene.addItem(block_item)
            self._block_items[obj.name] = block_item

            # Render connections
            project = self._get_managing_object()
            if isinstance(project, WizardProject) and obj.name in project.connections:
                for target in project.connections[obj.name]:
                    if target in self._block_items:
                        self._render_connection(obj.name, target)
            logger.info(f"Successfully added WizardBlock '{obj.name}' at position {obj.position}")
            self._scene.update()
            return self._build_response(obj, True, "_add_wizardblock", block_item)
        except Exception as e:
            logger.error(f"Failed to add WizardBlock '{obj.name}': {str(e)}")
            return self._build_response(obj, False, "_add_wizardblock", None, str(e))
    
    def _remove_wizardblock(self, obj: WizardBlock, attributes: Dict[str, Any] = None) -> Dict[str, Any]:
        """Remove a WizardBlock and its connections from the PySide6 canvas."""
        if attributes is None:
            attributes = {}
        try:
            block_name = obj.name
            if block_name not in self._block_items:
                logger.error(f"Block '{block_name}' not found in rendered items. Available: {list(self._block_items.keys())}")
                return self._build_response(obj, False, "_remove_wizardblock", None, f"Block '{block_name}' not rendered")

            block_item = self._block_items[block_name]
            self._scene.removeItem(block_item)
            del self._block_items[block_name]

            connections_to_remove = [
                key for key in self._connection_lines
                if key[0] == block_name or key[1] == block_name
            ]
            for key in connections_to_remove:
                self._scene.removeItem(self._connection_lines[key])
                del self._connection_lines[key]

            logger.info(f"Successfully removed WizardBlock '{block_name}' and its connections")
            self._scene.update()
            return self._build_response(obj, True, "_remove_wizardblock", None)
        except Exception as e:
            logger.error(f"Failed to remove WizardBlock '{block_name}': {str(e)}")
            return self._build_response(obj, False, "_remove_wizardblock", None, str(e))

    def _refresh_wizardblock(self, obj: WizardBlock, attributes: Dict[str, Any] = None) -> Dict[str, Any]:
        """Refresh a block by re-rendering it on the PySide6 canvas."""
        try:
            remove_response = self._remove_wizardblock(obj, attributes)
            if not remove_response["status"]:
                return remove_response
            return self._add_wizardblock(obj, attributes)
        except Exception as e:
            logger.error(f"Failed to refresh WizardBlock '{obj.name}'': {str(e)}")
            return self._build_response(obj, False, "_refresh_wizardblock", None, str(e))

    def _render_connection(self, source: str, target: str) -> None:
        """Render a connection line between two blocks."""
        try:
            source_item = self._block_items.get(source)
            target_item = self._block_items.get(target)
            if not source_item or not target_item:
                logger.warning(f"Cannot render connection: block '{source}' or '{target}' not found")
                return
            line = QGraphicsLineItem(
                source_item.rect().center().x(), source_item.rect().center().y(),
                target_item.rect().center().x(), target_item.rect().center().y()
            )
            self._scene.addItem(line)
            self._connection_lines[(source, target)] = line
            logger.debug(f"Successfully rendered connection from '{source}' to '{target}'")
        except Exception as e:
            logger.error(f"Failed to render connection from '{source}' to '{target}': {str(e)}")

    def _update_position(self, obj: WizardBlock, attributes: Dict[str, Any] = None) -> Dict[str, Any]:
        """Update the position of a WizardBlock and its connections."""
        if attributes is None or not attributes.get("position") is None:
            logger.error("Position not provided for update")
            return self._build_response(obj, False, "_update_position", None, "Position not provided")
        try:
            new_position = attributes["position"]
            if not isinstance(new_position, (tuple, list)) or len(new_position) != 2:
                raise ValueError("Position must be a tuple of (x, y)")
            obj.position = new_position
            if obj.name in self._block_items:
                self._block_items[obj.name].setPos(new_position[0], new_position[1])
                # Update connection lines
                project = self._get_managing_object()
                if isinstance(project, WizardProject):
                    for target in project.connections.get(obj.name, []):
                        if (obj.name, target) in self._connection_lines:
                            self._scene.removeItem(self._connection_lines[(obj.name, target)])
                            del self._connection_lines[(obj.name, target)]
                            self._render_connection(obj.name, target)
                    for source, targets in project.connections.items():
                        if obj.name in targets and (source, obj.name) in self._connection_lines:
                            self._scene.removeItem(self._connection_lines[(source, obj.name)])
                            del self._connection_lines[(source, obj.name)]
                            self._render_connection(source, obj.name)
            logger.info(f"Successfully updated position of WizardBlock '{obj.name}' to {new_position}")
            return self._build_response(obj, True, "_update_position", new_position)
        except Exception as e:
            logger.error(f"Failed to update position of WizardBlock '{obj.name}'': {str(e)}")
            return self._build_response(obj, False, "_update_position", None, str(e))