# gui/p_main_window.py
import sys
import os
import json
from typing import Dict, Any
from PySide6.QtWidgets import (
    QMainWindow, 
    QApplication, 
    QFileDialog, 
    QMessageBox, 
    QTreeView, 
    QMenu, 
    QGraphicsScene, 
    QTabBar, 
    QWidget
)
from PySide6.QtCore import Qt, Signal, Slot, QPoint
from PySide6.QtGui import QStandardItemModel, QStandardItem
from wizard.super.wizard_manipulator import WizardManipulator
from wizard.super.wizard_project import WizardProject
from wizard.base.wizard_block import WizardBlock
from common.utils.logging_setup import logger, setup_logging, update_logging_level
import logging

from gui.ui_main_window import Ui_MainWindow

class MSBWizardMainWindow(QMainWindow):
    """Main application window for MSBWizard."""
    project_updated = Signal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.settings = self.load_settings()
        
        # Настройка логирования
        log_level_str = self.settings.get("log_level", "DEBUG")
        log_level = getattr(logging, log_level_str, logging.DEBUG)
        setup_logging(log_file="msbwizard.log", log_level=log_level, clear_log=True)
        update_logging_level(log_level)
        logger.debug("Logging initialized for MSBWizard")

        # Инициализация проекта, сцены и манипулятора
        self.project = WizardProject(name="Untitled Project")
        self.scene = QGraphicsScene()
        self.ui.canvasView.setScene(self.scene)
        self.manipulator = WizardManipulator(managing_object=self.project, scene=self.scene)
        logger.debug(f"MSBWizardMainWindow initialized with project id: {id(self.project)}, manipulator id: {id(self.manipulator)}, scene id: {id(self.scene)}")

        self.current_project_path = None
        self._action_connections = {}
        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        """Setup the UI components and their initial states."""
        self.ui.dockWidget.setVisible(True)
        self.update_project_explorer()

        # Настраиваем вкладки
        for i in range(self.ui.tabContainer.count()):
            if self.ui.tabContainer.widget(i).objectName() == "projectInfoTab":
                self.ui.tabContainer.setCurrentIndex(i)
                self.ui.tabContainer.tabBar().setTabButton(i, QTabBar.ButtonPosition.RightSide, None)
                break
        self.ui.tabContainer.setTabsClosable(True)

        # Настраиваем Project Explorer
        project_explorer = self.ui.dockWidget.findChild(QTreeView, "projectExplorer")
        if project_explorer:
            project_explorer.setContextMenuPolicy(Qt.CustomContextMenu)
            project_explorer.customContextMenuRequested.connect(self.show_context_menu)
            logger.debug("Project explorer context menu connected")
        else:
            logger.error("Project explorer widget not found during setup_ui")

        # Синхронизация видимости dockWidget
        self.ui.dockWidget.visibilityChanged.connect(self.sync_project_explorer_action)

    def setup_connections(self):
        """Connect UI signals to slots, ensuring no duplicates."""
        self.clear_connections()

        actions = [
            (self.ui.actionNewProject, self.new_project),
            (self.ui.actionOpenProject, self.open_project),
            (self.ui.actionSaveProject, self.save_project),
            (self.ui.actionSaveProjectAs, self.save_project_as),
            (self.ui.actionGenerateCode, self.generate_code),
            (self.ui.actionPreferences, self.open_preferences),
        ]
        for action, slot in actions:
            connection = action.triggered.connect(slot)
            self._action_connections[action] = connection
            logger.debug(f"Connected action {action.objectName()}")

        project_explorer = self.ui.dockWidget.findChild(QTreeView, "projectExplorer")
        if project_explorer:
            project_explorer.clicked.connect(self.handle_project_explorer_click)
            logger.debug("Connected project explorer clicked signal")
        else:
            logger.error("Project explorer widget not found during setup_connections")

        self.ui.tabContainer.tabCloseRequested.connect(self.handle_tab_close)
        self.project_updated.connect(self.update_project_explorer)

    def clear_connections(self):
        """Disconnect all action signals to prevent duplicates."""
        for action, connection in self._action_connections.items():
            try:
                action.triggered.disconnect(connection)
                logger.debug(f"Disconnected signal for action {action.objectName()}")
            except Exception as e:
                logger.debug(f"No signal to disconnect for action {action.objectName()}: {str(e)}")
        self._action_connections.clear()

        try:
            self.project_updated.disconnect()
            logger.debug("Disconnected project_updated signal")
        except Exception as e:
            logger.debug(f"No connections to disconnect for project_updated: {str(e)}")

    def load_settings(self) -> Dict[str, Any]:
        """Load application settings from settings.json."""
        settings_file = "settings.json"
        default_settings = {
            "log_level": "DEBUG",
            "template_path": "templates",
        }
        if os.path.exists(settings_file):
            try:
                with open(settings_file, "r") as f:
                    loaded_settings = json.load(f)
                default_settings.update(loaded_settings)
                logger.info(f"Settings loaded from '{settings_file}'")
                return default_settings
            except Exception as e:
                logger.error(f"Failed to load settings from '{settings_file}': {str(e)}")
                QMessageBox.warning(self, "Error", f"Failed to load settings: {str(e)}")
        logger.info("No settings file found, using default settings")
        return default_settings

    def save_settings(self, settings: Dict[str, Any]):
        """Save application settings to settings.json."""
        try:
            with open("settings.json", "w") as f:
                json.dump(settings, f, indent=4)
            logger.info("Settings saved to 'settings.json'")
        except Exception as e:
            logger.error(f"Failed to save settings to 'settings.json': {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to save settings: {str(e)}")

    @Slot()
    def new_project(self):
        """Create a new project, clearing old data."""
        logger.info("Creating new project")
        self.clear_connections()
        for i in range(self.ui.tabContainer.count() - 1, -1, -1):
            self.ui.tabContainer.removeTab(i)
        self.project = WizardProject(name="Untitled Project")
        self.manipulator = WizardManipulator(managing_object=self.project, scene=self.scene)
        self.current_project_path = None
        self.ui.tabContainer.addTab(QWidget(), "Project")
        self.setup_connections()
        self.update_project_explorer()
        logger.debug("New project created and UI updated")

    @Slot()
    def open_project(self):
        """Open an existing project from file."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Project", "", "MSBWizard Project (*.msb)")
        if file_path:
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                self.project = WizardProject.from_dict(data)
                self.manipulator = WizardManipulator(managing_object=self.project, scene=self.scene)
                self.current_project_path = file_path
                self.project_updated.emit()
                for i in range(self.ui.tabContainer.count() - 1, -1, -1):
                    self.ui.tabContainer.removeTab(i)
                self.ui.tabContainer.addTab(QWidget(), "Project")
                logger.info(f"Project opened from '{file_path}'")
            except Exception as e:
                logger.error(f"Failed to open project: {str(e)}")
                QMessageBox.critical(self, "Error", f"Failed to open project: {str(e)}")

    @Slot()
    def save_project(self):
        """Save the current project."""
        if self.current_project_path:
            try:
                with open(self.current_project_path, "w") as f:
                    json.dump(self.project.to_dict(), f, indent=4)
                logger.info(f"Project saved to '{self.current_project_path}'")
            except Exception as e:
                logger.error(f"Failed to save project: {str(e)}")
                QMessageBox.critical(self, "Error", f"Failed to save project: {str(e)}")
        else:
            self.save_project_as()

    @Slot()
    def save_project_as(self):
        """Save the current project to a new file."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Project As", "", "MSBWizard Project (*.msb)")
        if file_path:
            if not file_path.endswith(".msb"):
                file_path += ".msb"
            self.current_project_path = file_path
            self.save_project()

    @Slot()
    def generate_code(self):
        """Generate code for the current project."""
        logger.debug("Generating code")
        result = self.manipulator.process_request({
            "operation": "generate",
            "obj": self.project,
            "attributes": {"template": "default_project_template"}
        })
        if result["status"]:
            logger.info(f"Generated code:\n{result['result']}")
            QMessageBox.information(self, "Success", "Code generated successfully.")
        else:
            logger.error(f"Failed to generate code: {result.get('error', 'Unknown error')}")
            QMessageBox.critical(self, "Error", f"Failed to generate code: {result.get('error', 'Unknown error')}")

    @Slot()
    def open_preferences(self):
        """Open preferences dialog (not implemented)."""
        QMessageBox.information(self, "Info", "Preferences dialog not implemented yet.")
        logger.info("Preferences dialog requested but not implemented")

    @Slot(int)
    def handle_tab_close(self, index):
        """Handle closing of tabs, prevent closing of project tab."""
        widget = self.ui.tabContainer.widget(index)
        if widget.objectName() == "projectInfoTab":
            return
        self.ui.tabContainer.removeTab(index)
        logger.debug(f"Closed tab at index {index}")

    @Slot(QPoint)
    def show_context_menu(self, position: QPoint):
        """Show context menu for Project Explorer."""
        project_explorer = self.ui.dockWidget.findChild(QTreeView, "projectExplorer")
        if not project_explorer:
            return

        index = project_explorer.indexAt(position)
        if not index.isValid():
            return

        item = project_explorer.model().itemFromIndex(index)
        if not item:
            return

        item_type = item.data(Qt.UserRole)
        menu = QMenu(self)

        if item_type == "project":
            add_action = menu.addAction("Add Block")
            add_action.triggered.connect(self.add_block)
        elif item_type == "block":
            block_name = item.text()
            edit_action = menu.addAction("Edit Block")
            remove_action = menu.addAction("Remove Block")
            edit_action.triggered.connect(lambda: self.edit_block(block_name))
            remove_action.triggered.connect(lambda: self.remove_block(block_name))
        else:
            return

        menu.exec(project_explorer.viewport().mapToGlobal(position))

    @Slot()
    def add_block(self):
        """Add a new block to the project."""
        block = WizardBlock(name=f"Block{len(self.project.blocks.get_all()) + 1}", block_type="entity")
        response = self.manipulator.process_request({
            "operation": "manage",
            "obj": block,
            "attributes": {"action": "create"}
        })
        if response["status"]:
            logger.info(f"Block '{block.name}' added")
            render_response = self.manipulator.process_request({
                "operation": "render",
                "obj": block,
                "attributes": {"action": "add"}
            })
            if not render_response["status"]:
                logger.error(f"Failed to render block '{block.name}': {render_response.get('error', 'Unknown error')}")
                QMessageBox.critical(self, "Error", f"Failed to render block: {render_response.get('error', 'Unknown error')}")
            else:
                self.project_updated.emit()
        else:
            logger.error(f"Failed to add block: {response.get('error', 'Unknown error')}")
            QMessageBox.critical(self, "Error", f"Failed to add block: {response.get('error', 'Unknown error')}")

    @Slot(str)
    def edit_block(self, block_name: str):
        """Edit an existing block (not fully implemented)."""
        logger.debug(f"Editing block '{block_name}'")
        QMessageBox.information(self, "Info", f"Edit block '{block_name}' not fully implemented.")

    @Slot(str)
    def remove_block(self, block_name: str):
        """Remove a block from the project and update the canvas."""
        block = self.project.blocks.get(block_name)
        if block:
            response = self.manipulator.process_request({
                "operation": "manage",
                "obj": block,
                "attributes": {"action": "delete"}
            })
            if response["status"]:
                logger.info(f"Block '{block_name}' removed")

                render_response = self.manipulator.process_request({
                    "operation": "render",
                    "obj": block,
                    "attributes": {"action": "remove"}
                })
                if not render_response["status"]:
                    logger.error(f"Failed to remove block from canvas: {render_response.get('error', 'Unknown error')}")
                self.project_updated.emit()
            else:
                logger.error(f"Failed to remove block: {response.get('error', 'Unknown error')}")
                QMessageBox.critical(self, "Error", f"Failed to remove block: {response.get('error', 'Unknown error')}")
        else:
            logger.error(f"Block '{block_name}' not found")
            QMessageBox.critical(self, "Error", f"Block '{block_name}' not found")

    @Slot()
    def handle_project_explorer_click(self, index):
        """Handle clicks on Project Explorer."""
        item = self.ui.projectExplorer.model().itemFromIndex(index)
        if not item:
            return
        item_type = item.data(Qt.UserRole)
        if item_type == "project":
            self.ui.tabContainer.setCurrentIndex(0)
        elif item_type == "block":
            block_name = item.text()
            logger.debug(f"Clicked block: {block_name}")

    def update_project_explorer(self):
        """Update Project Explorer tree."""
        project_explorer = self.ui.dockWidget.findChild(QTreeView, "projectExplorer")
        if not project_explorer:
            logger.error("Project explorer widget not found")
            return

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Project Explorer"])
        root = model.invisibleRootItem()

        project_item = QStandardItem(f"Project: {self.project.name}")
        project_item.setData("project", Qt.UserRole)
        root.appendRow(project_item)

        blocks_item = QStandardItem("Blocks")
        blocks_item.setData("blocks", Qt.UserRole)
        project_item.appendRow(blocks_item)

        for block in self.project.blocks.get_all().values():
            block_item = QStandardItem(block.name)
            block_item.setData("block", Qt.UserRole)
            blocks_item.appendRow(block_item)
            logger.debug(f"Added block '{block.name}' to project explorer")

        project_explorer.setModel(model)
        project_explorer.expandAll()
        project_explorer.viewport().update()
        logger.debug("Project explorer updated")

    @Slot(bool)
    def sync_project_explorer_action(self, visible: bool):
        """Synchronize the Project Explorer action with dockWidget visibility."""
#        self.ui.actionProject_Explorer.setChecked(visible)
        logger.debug(f"Project Explorer action synchronized: checked={visible}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MSBWizardMainWindow()
    window.show()
    sys.exit(app.exec())