# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_msbwizard_main_windowEkUwQz.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QDockWidget, QGraphicsView, QHeaderView,
    QMainWindow, QMenu, QMenuBar, QSizePolicy,
    QTabWidget, QTreeView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(996, 717)
        MainWindow.setStyleSheet(u"\n"
"QMainWindow {\n"
"    background-color: #f5f5f5;\n"
"    font-family: Arial, sans-serif;\n"
"}\n"
"QMenuBar {\n"
"    background-color: #ffffff;\n"
"    color: #333333;\n"
"    padding: 4px;\n"
"}\n"
"QMenuBar::item {\n"
"    background: #ffffff;\n"
"    padding: 4px 8px;\n"
"    color: #333333;\n"
"}\n"
"QMenuBar::item:selected {\n"
"    background: #0078d7;\n"
"    color: #ffffff;\n"
"}\n"
"QMenu {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #d3d3d3;\n"
"    color: #333333;\n"
"}\n"
"QMenu::item {\n"
"    padding: 4px 24px 4px 8px;\n"
"    background: #ffffff;\n"
"    color: #333333;\n"
"}\n"
"QMenu::item:selected {\n"
"    background: #0078d7;\n"
"    color: #ffffff;\n"
"}\n"
"QTreeView {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #d3d3d3;\n"
"    selection-background-color: #0078d7;\n"
"    selection-color: #ffffff;\n"
"    font-size: 12px;\n"
"}\n"
"QTabWidget::pane {\n"
"    border: 1px solid #d3d3d3;\n"
"    background: #ffffff;\n"
"}\n"
"QTabBar::tab {\n"
"    ba"
                        "ckground: #f0f0f0;\n"
"    padding: 4px 8px;\n"
"    border: 1px solid #d3d3d3;\n"
"    border-bottom: none;\n"
"}\n"
"QTabBar::tab:selected {\n"
"    background: #0078d7;\n"
"    color: #ffffff;\n"
"}\n"
"QGraphicsView {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #d3d3d3;\n"
"}\n"
"   ")
        self.actionNewProject = QAction(MainWindow)
        self.actionNewProject.setObjectName(u"actionNewProject")
        self.actionOpenProject = QAction(MainWindow)
        self.actionOpenProject.setObjectName(u"actionOpenProject")
        self.actionSaveProject = QAction(MainWindow)
        self.actionSaveProject.setObjectName(u"actionSaveProject")
        self.actionSaveProjectAs = QAction(MainWindow)
        self.actionSaveProjectAs.setObjectName(u"actionSaveProjectAs")
        self.actionGenerateCode = QAction(MainWindow)
        self.actionGenerateCode.setObjectName(u"actionGenerateCode")
        self.actionPreferences = QAction(MainWindow)
        self.actionPreferences.setObjectName(u"actionPreferences")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabContainer = QTabWidget(self.centralwidget)
        self.tabContainer.setObjectName(u"tabContainer")
        self.tabContainer.setTabsClosable(True)
        self.projectInfoTab = QWidget()
        self.projectInfoTab.setObjectName(u"projectInfoTab")
        self.tabContainer.addTab(self.projectInfoTab, "")

        self.verticalLayout.addWidget(self.tabContainer)

        self.canvasView = QGraphicsView(self.centralwidget)
        self.canvasView.setObjectName(u"canvasView")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.canvasView.sizePolicy().hasHeightForWidth())
        self.canvasView.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.canvasView)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 996, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.dockWidget = QDockWidget(MainWindow)
        self.dockWidget.setObjectName(u"dockWidget")
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout_2 = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.projectExplorer = QTreeView(self.dockWidgetContents)
        self.projectExplorer.setObjectName(u"projectExplorer")
        self.projectExplorer.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        self.verticalLayout_2.addWidget(self.projectExplorer)

        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dockWidget)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menuFile.addAction(self.actionNewProject)
        self.menuFile.addAction(self.actionOpenProject)
        self.menuFile.addAction(self.actionSaveProject)
        self.menuFile.addAction(self.actionSaveProjectAs)
        self.menuTools.addAction(self.actionGenerateCode)
        self.menuTools.addAction(self.actionPreferences)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MSBWizard", None))
        self.actionNewProject.setText(QCoreApplication.translate("MainWindow", u"New Project", None))
        self.actionOpenProject.setText(QCoreApplication.translate("MainWindow", u"Open Project", None))
        self.actionSaveProject.setText(QCoreApplication.translate("MainWindow", u"Save Project", None))
        self.actionSaveProjectAs.setText(QCoreApplication.translate("MainWindow", u"Save Project As", None))
        self.actionGenerateCode.setText(QCoreApplication.translate("MainWindow", u"Generate Code", None))
        self.actionPreferences.setText(QCoreApplication.translate("MainWindow", u"Preferences", None))
        self.tabContainer.setTabText(self.tabContainer.indexOf(self.projectInfoTab), QCoreApplication.translate("MainWindow", u"Project", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", u"Tools", None))
        self.dockWidget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Project Explorer", None))
    # retranslateUi