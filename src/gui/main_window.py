from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QColor, QAction, QTransform
from PyQt6.QtWidgets import QMainWindow, QButtonGroup
from PyQt6.QtCore import QObject
from gui.settings_window import Ui_settingsWindow
from theme.styles import Styles
from gui.dialog import show_dialog
from ebay.ebay import Ebay
from utils import Utils
from plot.mpl import Chart
import os

# Constructs the main window

class Ui_mainWindow(QObject):
    def __init__(self):
        super().__init__()
        # Variable to hold API request data
        self.default_response = {}
        
        # Data corresponding to eBay item category: 'Trading Card Singles'
        self.keywords = ""
        self.excluded_keywords = "box case break cgc cu ga ags lc tcm hga" + \
            "sge csg ksa gma bvg bccg wsg wgs"
        self.max_search_results = "240"
        self.category_id = "261328"
        self.remove_outliers = True
        self.site_id = "0"
        self.aspects = [{"name": "Graded", "value": "No"}]

        # To access matplotlib chart generator
        self.history_chart = Chart()

        # To access util methods
        self.utils = Utils()

        # Init the main window
        self.mainWindow = QMainWindow()

        # Init the settings window
        self.settings_window = QMainWindow()

        # Init the settings window obj to store changed values
        self.settingsWindow = Ui_settingsWindow()

        # Save location for settings
        self.settings_path = self.settingsWindow.settings_location

        # Save location for default save
        self.default_save = self.settings_path

        # To use make_request()
        self.ebay = self.settingsWindow.ebay

        # Set current visual theme
        self.current_theme = Styles.default_theme

        # Construct the window
        self.setupUi()

        # Receive Ui_settingsWindow emitted signal, then apply the set theme
        self.settingsWindow.theme_changed.connect(self.applyTheme)

        # Stage the search method event listener
        self.btnSearch.clicked.connect(self.search)
        self.txtSearch.returnPressed.connect(self.search)
    
    def applyTheme(self, theme:str):
        """Apply visual theme on load, called from constructor"""
        default_widgets = [
            "mainWindow",
            "lblCardHighest",
            "lblCardLowest",
            "lblCategory",
            "lblGraded",
            "lblService",
            "rbServicePSA",
            "rbServiceSGC",
            "rbServiceBGS",
            "rbGradedNo",
            "rbGradedYes",
            "btnClear",
            "btnExit",
            "btnSearch",
            "tabMain",
            "lblTitle",
            "txtSearch",
            "menubar",
            "txtInfoHighest",
            "txtInfoLowest",
            "file_menu"
            
        ]
        objects_to_style = {
            "default": default_widgets,
            "dark": default_widgets,
            "light": default_widgets,
        }

        for widget_name in objects_to_style[theme]:
            if theme == 'default':
                Styles.apply_style(self, widget_name, Styles.default_theme)
            elif theme == 'dark':
                Styles.apply_style(self, widget_name, Styles.dark_theme)
            elif theme == 'light':
                Styles.apply_style(self, widget_name, Styles.light_theme)
    
    def setupUi(self):
        """Constructs the window"""
        if not os.path.exists(self.settings_path):
            os.makedirs(self.settings_path)
        
        # Load user's settings file, if found
        loaded_file = self.settingsWindow.load_settings()
        if loaded_file != {}:
            # Store the user file path in self.default_save
            self.default_save = loaded_file["default_file_location"]
            # Set the user's api
            self.settingsWindow.set_api_from_settings(loaded_file)
            # Set the user's save path
            new_default_path = self.settingsWindow.set_default_save_from_settings(loaded_file, self.settings_path)
            self.default_save = new_default_path
            # Set the user's theme 
            user_theme = self.settingsWindow.set_theme_from_settings(loaded_file)
            self.settingsWindow.theme = user_theme
            # Pass settings data back to settings window
            if user_theme == "default":
                self.current_theme = Styles.default_theme
                self.settingsWindow.current_theme = Styles.default_theme
                self.settingsWindow.set_color("default")
            elif user_theme == "dark":
                self.current_theme = Styles.dark_theme
                self.settingsWindow.set_color("dark")
            elif user_theme == "light":
                self.current_theme = Styles.light_theme
                self.settingsWindow.set_color("light")
                
            show_dialog("success", "User preferences were loaded")
        else:
            self.ebay.set_appid("Your rapidapi key")
            print(loaded_file)
            
        self.mainWindow.setObjectName("mainWindow")
        self.mainWindow.setEnabled(True)
        self.mainWindow.resize(820, 650)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mainWindow.sizePolicy().hasHeightForWidth())
        self.mainWindow.setSizePolicy(sizePolicy)
        self.mainWindow.setMinimumSize(QtCore.QSize(820, 650))
        self.mainWindow.setMaximumSize(QtCore.QSize(820, 650))
        self.mainWindow.setBaseSize(QtCore.QSize(820, 650))
        self.mainWindow.setAutoFillBackground(False)
        self.mainWindow.setStyleSheet(f"background-color: {self.current_theme['background']}")
        self.mainWindow.setToolButtonStyle(
            QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.mainWindow.setDocumentMode(False)
        self.mainWindow.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.mainWindow.setDockNestingEnabled(False)
        self.mainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(self.mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lblCategory = QtWidgets.QLabel(self.centralwidget)
        self.lblCategory.setStyleSheet(
            f"font-size: 14pt; color: {self.current_theme['foreground']}; text-align: center;")
        self.lblCategory.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.lblCategory.setObjectName("lblCategory")
        self.verticalLayout_3.addWidget(self.lblCategory)
        self.lblGraded = QtWidgets.QLabel(self.centralwidget)
        
        self.serviceGroup = QButtonGroup()
        self.yesNoGroup = QButtonGroup()
        
        # Label for 'Graded' radio button filters
        self.lblGraded.setStyleSheet(
            f"font-size: 12pt; color: {self.current_theme['foreground']}; text-align: center;")
        self.lblGraded.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading |
                                    QtCore.Qt.AlignmentFlag.AlignLeft | 
                                    QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lblGraded.setObjectName("lblGraded")
        self.verticalLayout_3.addWidget(self.lblGraded)
        # Graded filter
        self.rbGradedYes = QtWidgets.QRadioButton(self.centralwidget)
        self.rbGradedYes.setStyleSheet(f"color: {self.current_theme['foreground']}")
        self.rbGradedYes.setText("Yes")
        self.rbGradedYes.setObjectName("rbGradedYes")
        self.verticalLayout_3.addWidget(self.rbGradedYes)
        # Ungraded filter
        self.rbGradedNo = QtWidgets.QRadioButton(self.centralwidget)
        self.rbGradedNo.setStyleSheet(f"color: {self.current_theme['foreground']}")
        self.rbGradedNo.setText("No")
        self.rbGradedNo.setObjectName("rbGradedNo")
        self.verticalLayout_3.addWidget(self.rbGradedNo)
        # Exclude the radio buttons yes and no
        self.yesNoGroup.addButton(self.rbGradedYes)
        self.yesNoGroup.addButton(self.rbGradedNo)
        
        # Label for 'Service' radio button filters
        self.lblService = QtWidgets.QLabel(self.centralwidget)
        self.lblService.setStyleSheet(f"font-size: 12pt; color: {self.current_theme['foreground']}; text-align: center;")
        self.lblService.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading |
                                    QtCore.Qt.AlignmentFlag.AlignLeft | 
                                    QtCore.Qt.AlignmentFlag.AlignVCenter)
        
        self.lblService.setObjectName("lblService")
        self.lblService.setVisible(False)
        self.verticalLayout_3.addWidget(self.lblService)
        # PSA filter
        self.rbServicePSA = QtWidgets.QRadioButton(self.centralwidget)
        self.rbServicePSA.setStyleSheet(f"color: {self.current_theme['foreground']}")
        self.rbServicePSA.setText("PSA")
        self.rbServicePSA.setObjectName("rbServicePSA")
        self.verticalLayout_3.addWidget(self.rbServicePSA)
        # SGC filter
        self.rbServiceSGC = QtWidgets.QRadioButton(self.centralwidget)
        self.rbServiceSGC.setStyleSheet(f"color: {self.current_theme['foreground']}")
        self.rbServiceSGC.setText("SGC")
        self.rbServiceSGC.setObjectName("rbServiceSGC")
        self.verticalLayout_3.addWidget(self.rbServiceSGC)
        # BGS filter
        self.rbServiceBGS = QtWidgets.QRadioButton(self.centralwidget)
        self.rbServiceBGS.setStyleSheet(f"color: {self.current_theme['foreground']}")
        self.rbServiceBGS.setText("BGS")
        self.rbServiceBGS.setObjectName("rbServiceBGS")
        self.verticalLayout_3.addWidget(self.rbServiceBGS)
        # Exclude the service radio buttons
        self.serviceGroup.addButton(self.rbServicePSA)
        self.serviceGroup.addButton(self.rbServiceSGC)
        self.serviceGroup.addButton(self.rbServiceBGS)
        
        self.rbServicePSA.setVisible(False)
        self.rbServiceSGC.setVisible(False)
        self.rbServiceBGS.setVisible(False)
        
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.btnClear = QtWidgets.QPushButton(self.centralwidget)
        self.btnClear.setMinimumSize(QtCore.QSize(80, 0))
        self.btnClear.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.btnClear.setAutoFillBackground(False)
        self.btnClear.setStyleSheet(f"""
            QPushButton {{
                color: {self.current_theme['foreground']};
                border: 1px solid {self.current_theme['foreground']};
                border-radius: 10px;
                padding: 3px;
            }}
            QPushButton:pressed {{
                color: {self.current_theme['fore_inverse']};
                border: 1px solid {self.current_theme['foreground']};
                border-radius: 10px;
                padding: 3px;
                background-color: {self.current_theme['back_inverse']};
            }}
            """)
        self.btnClear.setAutoDefault(False)
        self.btnClear.setObjectName("btnClear")
        self.verticalLayout_3.addWidget(self.btnClear)
        self.btnExit = QtWidgets.QPushButton(self.centralwidget)
        self.btnExit.setMinimumSize(QtCore.QSize(80, 0))
        self.btnExit.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.btnExit.setAutoFillBackground(False)
        self.btnExit.setStyleSheet(f"""
            QPushButton {{
                color: {self.current_theme['foreground']};
                border: 1px solid {self.current_theme['foreground']};
                border-radius: 10px;
                padding: 3px;
            }}
            QPushButton:pressed {{
                color: {self.current_theme['fore_inverse']};
                border: 1px solid {self.current_theme['foreground']};
                border-radius: 10px;
                padding: 3px;
                background-color: {self.current_theme['back_inverse']};
            }}
            """)
        self.btnExit.setAutoDefault(False)
        self.btnExit.setObjectName("btnExit")
        self.verticalLayout_3.addWidget(self.btnExit)
        self.gridLayout.addLayout(self.verticalLayout_3, 2, 3, 2, 1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.btnSearch = QtWidgets.QPushButton(self.centralwidget)
        self.btnSearch.setMinimumSize(QtCore.QSize(80, 0))
        self.btnSearch.setLayoutDirection(
            QtCore.Qt.LayoutDirection.LeftToRight)
        self.btnSearch.setAutoFillBackground(False)
        self.btnSearch.setStyleSheet(f"""
            QPushButton {{
                color: {self.current_theme['foreground']};
                border: 1px solid {self.current_theme['foreground']};
                border-radius: 10px;
                padding: 3px;
            }}
            QPushButton:pressed {{
                color: {self.current_theme['fore_inverse']};
                border: 1px solid {self.current_theme['foreground']};
                border-radius: 10px;
                padding: 3px;
                background-color: {self.current_theme['back_inverse']};
            }}
            """)
        self.btnSearch.setAutoDefault(False)
        self.btnSearch.setObjectName("btnSearch")
        self.gridLayout.addWidget(self.btnSearch, 0, 3, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblTitle = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lblTitle.sizePolicy().hasHeightForWidth())
        self.lblTitle.setSizePolicy(sizePolicy)
        self.lblTitle.setStyleSheet(
            f"color: {self.current_theme['foreground']}; \n"
            f"border: 1px solid {self.current_theme['foreground']}; border-radius: 10px; \n"
            f"padding-left: 10px; padding-right: 10px")
        self.lblTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lblTitle.setObjectName("lblTitle")
        self.horizontalLayout.addWidget(self.lblTitle)
        self.txtSearch = QtWidgets.QLineEdit(self.centralwidget)
        self.txtSearch.setStyleSheet(
            f"border: none; border-radius: 10px; margin: 0 10px; \n"
            f"color: {self.current_theme['foreground']}; padding: 3px; \n"
            f"background-color: {self.current_theme['accent']};")
        self.txtSearch.setObjectName("txtSearch")
        self.txtSearch.setPlaceholderText(
            "Include specific information, (ex. 1986-87 Fleer - #57 Michael Jordan (RC) #57)")
        self.horizontalLayout.addWidget(self.txtSearch)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        
        self.tabMain = QtWidgets.QTabWidget(self.centralwidget)
        self.tabMain.setStyleSheet(
            f"""
            QTabWidget::pane{{
                border: 2px solid {self.current_theme['accent']};
                border-radius: 15px;
                padding: 5px
            }}

            QTabWidget::tab-bar{{
                alignment: right
            }}

            QTabBar::tab{{
                background-color: {self.current_theme['background']};
                color: {self.current_theme['foreground']};
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                min-width: 70px;
                margin: 0px 10px 0px;
                padding: 5px;
                transition: background-color 0.3s ease-in-out, color 0.3s ease-in-out;
            }}

            QTabBar::tab:!selected{{
                margin-top: 5px;
            }}

            QTabBar::tab:hover{{
                background-color: {self.current_theme['back_inverse']};
                color: {self.current_theme['fore_inverse']};
            }}
            """)

        self.tabMain.setTabPosition(QtWidgets.QTabWidget.TabPosition.North)
        self.tabMain.setElideMode(QtCore.Qt.TextElideMode.ElideRight)
        self.tabMain.setObjectName("tabMain")
        self.tabHighest = QtWidgets.QWidget()
        self.tabHighest.setEnabled(True)
        self.tabHighest.setObjectName("tabHighest")
        self.gridLayoutWidget = QtWidgets.QWidget(self.tabHighest)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 651, 481))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lblCardHighest = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lblCardHighest.setMinimumSize(QtCore.QSize(325, 475))
        self.lblCardHighest.setMaximumSize(QtCore.QSize(325, 475))
        self.lblCardHighest.setStyleSheet(
            f"border-radius: 10px;\n"
            f"background-color: {self.current_theme['accent']}; \n"
            f"color: {self.current_theme['foreground']};")
        self.lblCardHighest.setText("")
        self.lblCardHighest.setScaledContents(True)
        self.lblCardHighest.setContentsMargins(10, 10, 10, 10)
        self.lblCardHighest.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lblCardHighest.setObjectName("lblCardHighest")
        self.gridLayout_2.addWidget(self.lblCardHighest, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.txtInfoHighest = QtWidgets.QTextBrowser(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.txtInfoHighest.sizePolicy().hasHeightForWidth())
        self.txtInfoHighest.setSizePolicy(sizePolicy)
        self.txtInfoHighest.setMinimumSize(QtCore.QSize(310, 475))
        self.txtInfoHighest.setStyleSheet(
            f"font-size: 10pt; color: {self.current_theme['foreground']}; padding: 5px;")
        self.txtInfoHighest.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.txtInfoHighest.setAutoFormatting(
            QtWidgets.QTextBrowser.AutoFormattingFlag.AutoNone)
        self.txtInfoHighest.setUndoRedoEnabled(False)
        self.txtInfoHighest.setLineWrapColumnOrWidth(0)
        # self.txtInfoHighest.setReadOnly(True)
        self.txtInfoHighest.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)
        self.txtInfoHighest.setPlaceholderText("")
        self.txtInfoHighest.acceptRichText = True
        self.txtInfoHighest.setOpenExternalLinks(True)
        self.txtInfoHighest.setObjectName("txtInfoHighest")
        self.verticalLayout.addWidget(self.txtInfoHighest)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 2, 1, 1)
        self.tabMain.addTab(self.tabHighest, "")
        self.tabLowest = QtWidgets.QWidget()
        self.tabLowest.setObjectName("tabLowest")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.tabLowest)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 651, 481))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.lblCardLowest = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.lblCardLowest.setMinimumSize(QtCore.QSize(325, 475))
        self.lblCardLowest.setMaximumSize(QtCore.QSize(325, 475))
        self.lblCardLowest.setStyleSheet(
            f"border-radius: 10px;\n"
            f"background-color: {self.current_theme['accent']}; \n"
            f"color: {self.current_theme['foreground']};")
        self.lblCardLowest.setText("")
        self.lblCardLowest.setScaledContents(True)
        self.lblCardLowest.setContentsMargins(10, 10, 10, 10)
        self.lblCardLowest.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lblCardLowest.setObjectName("lblCardLowest")
        self.gridLayout_3.addWidget(self.lblCardLowest, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.txtInfoLowest = QtWidgets.QTextBrowser(self.gridLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.txtInfoLowest.sizePolicy().hasHeightForWidth())
        self.txtInfoLowest.setSizePolicy(sizePolicy)
        self.txtInfoLowest.setMinimumSize(QtCore.QSize(310, 475))
        self.txtInfoLowest.setStyleSheet(
            f"font-size: 10pt; color: {self.current_theme['foreground']}; padding: 5px")
        self.txtInfoLowest.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.txtInfoLowest.setAutoFormatting(
            QtWidgets.QTextBrowser.AutoFormattingFlag.AutoNone)
        self.txtInfoLowest.setUndoRedoEnabled(False)
        self.txtInfoLowest.setLineWrapColumnOrWidth(0)
        # self.txtInfoLowest.setReadOnly(True)
        self.txtInfoLowest.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)
        self.txtInfoLowest.setPlaceholderText("")
        self.txtInfoLowest.setObjectName("txtInfoLowest")
        self.verticalLayout_2.addWidget(self.txtInfoLowest)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 2, 1, 1)
        self.tabMain.addTab(self.tabLowest, "")
        self.tabHistory = QtWidgets.QWidget()
        self.tabHistory.setObjectName("tabHistory")
        self.lblHistory = QtWidgets.QLabel(self.tabHistory)
        self.lblHistory.setGeometry(QtCore.QRect(10, 10, 651, 481))
        self.lblHistory.setStyleSheet("border-radius: 10px; padding: 10px;")
        self.lblHistory.setText("")
        self.lblHistory.setObjectName("lblHistory")
        self.tabMain.addTab(self.tabHistory, "")
        self.horizontalLayout_2.addWidget(self.tabMain)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 1, 2, 1)
        self.mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self.mainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 820, 22))
        self.menubar.setObjectName("menubar")
        self.menubar.setFont(QtGui.QFont("Segoe UI", 10))
        self.menubar.setStyleSheet(
            f"""
            QMenuBar {{
            background-color: {self.current_theme['background']};
            color: {self.current_theme['foreground']};
            }}
            
            QMenuBar::item {{
            background-color: {self.current_theme['background']};
            color: {self.current_theme['foreground']};
            }}

            QMenuBar::item:selected {{
            background-color: {self.current_theme['back_inverse']};
            color: {self.current_theme['fore_inverse']};
            }}
            """)
        self.mainWindow.setMenuBar(self.menubar)
        self.file_menu = self.menubar.addMenu('File')
        self.file_menu.setFont(QtGui.QFont("Segoe UI", 10))
        self.file_menu.setStyleSheet(
            f"""
            QMenu {{
            background-color: {self.current_theme['background']};
            color: {self.current_theme['foreground']};
            }}

            QMenu::item {{
            background-color: {self.current_theme['background']};
            color: {self.current_theme['foreground']};
            }}

            QMenu::item:selected {{
            background-color: {self.current_theme['back_inverse']};
            color: {self.current_theme['fore_inverse']};
            }}
            """)
        
        # Items in 'File'
        save_default = QAction('Save', self.mainWindow)
        save_as = QAction('Save As...', self.mainWindow)
        settings = QAction('Settings', self.mainWindow)
        self.file_menu.addActions([save_default, save_as, settings])
        
        # Validate response content
        # Save As
        def save_content():
            if self.default_response == {}:
                show_dialog("error", "There is nothing to save")
            else:
                return self.utils.save_as_dialog(self.default_response)
        # Default Save
        def default_save_content():
            if self.default_response == {}:
                show_dialog("error", "There is nothing to save")
            else:
                self.utils.dict_to_txt(
                    self.default_response,
                    self.default_save,
                    self.txtSearch.text()
                )
                show_dialog("success", f"File was saved:\n{self.default_save}")

        
        # obj.signal.signal_method(slot)
        settings.triggered.connect(self.openSettingsWindow)
        save_as.triggered.connect(save_content)
        save_default.triggered.connect(default_save_content)

        self.retranslateUi(self.mainWindow)
        self.tabMain.setCurrentIndex(0)
        self.btnClear.clicked.connect(self.clear_content)
        self.btnExit.clicked.connect(self.close_all)
        QtCore.QMetaObject.connectSlotsByName(self.mainWindow)
        self.rbGradedYes.clicked.connect(self.rb_clicked)
        self.rbGradedNo.clicked.connect(self.rb_clicked)
    
    def close_all(self):
        """Closes all opened windows """
        self.mainWindow.close()
        self.settingsWindow.settings_ui.close()
    
    def rb_clicked(self):
        """Show new filters if graded filter is active, otherwise hide filters"""
        if self.rbGradedYes.isChecked():
            self.lblService.setVisible(True)
            self.rbServicePSA.setVisible(True)
            self.rbServiceSGC.setVisible(True)
            self.rbServiceBGS.setVisible(True)
        elif self.rbGradedNo.isChecked():
            self.rbServicePSA.setChecked(False)
            self.rbServiceSGC.setChecked(False)
            self.rbServiceBGS.setChecked(False)
            self.lblService.setVisible(False)
            self.rbServicePSA.setVisible(False)
            self.rbServiceSGC.setVisible(False)
            self.rbServiceBGS.setVisible(False)
            
    def clear_content(self):
        '''Clears the data assigned to class widgets and attributes'''
        self.default_response.clear()
        self.lblCardHighest.clear()
        self.lblCardLowest.clear()
        self.txtInfoHighest.clear()
        self.txtInfoLowest.clear()
        self.lblHistory.clear()
        self.keywords = ""
        self.excluded_keywords = "box case break " + \
        "cgc cu ga ags lc tcm hga " + \
            "sge csg ksa gma bvg bccg wsg wgs"

    def handle_api_error(self):
        '''Prompt user based on status code value of Ebay.code'''
        if Ebay.code != 200:
            self.lblCardHighest.setText("No data was found")
            self.lblCardLowest.setText("No data was found")
            if Ebay.code == 429:
                show_dialog("success", f"{Ebay.code}: You've exceeded your monthly call limit")
            elif Ebay.code == 401:
                show_dialog("error", f"{Ebay.code}: API key not found. Please enter your API key to continue.")
            return

    def render_images(self, response, imgHigh, imgLow, descendingResults, ascendingResults):
        """Assigns an image to the widgets: Highest, Lowest, History

        Args:
            - response (dict): The data retrieved from API
            - imgHigh (QPixmap): Converted image of highest sold card
            - imgLow (QPixmap): Converted image of lowest sold card
            - descendingResults (str): Stringified data in desc order
            - ascendingResults (str): Stringified data in asc order
        """
        text_color = "#FF7F7F"
        salesHistoryQImage = self.history_chart.generate_chart(response, text_color)
        pmWidthHighest, pmHeightHighest = imgHigh.width(), imgHigh.height()
        self.lblCardHighest.setPixmap(imgHigh.transformed(QTransform().rotate(-90)) if pmWidthHighest > pmHeightHighest else imgHigh)
        self.txtInfoHighest.setHtml(descendingResults)
        pmWidthLowest, pmHeightLowest = imgLow.width(), imgLow.height()
        self.lblCardLowest.setPixmap(imgLow.transformed(QTransform().rotate(-90)) if pmWidthLowest > pmHeightLowest else imgLow)
        self.txtInfoLowest.setHtml(ascendingResults)
        self.lblHistory.setPixmap(salesHistoryQImage)

    def set_grade_aspects(self):
        """Adds the servicer acronym to user keyword based on selection.
        \nReturns True if 'Graded' filter is 'Yes'"""
        if self.rbGradedYes.isChecked() == True:
            if self.rbServicePSA.isChecked():
                self.keywords += " PSA"
                self.excluded_keywords += " sgc bgs"
            elif self.rbServiceSGC.isChecked():
                self.keywords += " SGC"
                self.excluded_keywords += " psa bgs"
            elif self.rbServiceBGS.isChecked():
                self.keywords += " BGS"
                self.excluded_keywords += " sgc psa"
            return True
        else:
            return False

    def search(self):
        """ Searches for the item. This slot is called when a signal is triggered by widgets:
            - QLineEdit.txtSearch
            - QButton.btnSearch
        """
        # Discard the previously displayed data
        self.clear_content()
        print("\n\nContent cleared: " + self.keywords)
        
        # Set the new keyword
        self.keywords = self.txtSearch.text()
        
        # Check if any filters were toggled
        if self.set_grade_aspects() == True:
            self.aspects = [{"name": "Graded", "value": "Yes"}]
            print("Filter changed: Graded")
        else:
            self.aspects = [{"name": "Graded", "value": "No"}]
            
        # If search term absent or invalid, exit method
        if self.keywords == "":
            self.txtInfoHighest.setText("Nothing was searched")
            self.txtInfoLowest.setText("Nothing was searched")
            return
        if self.utils.validate_input(self.keywords) == False:
            self.txtInfoHighest.setText("Improper search term")
            self.txtInfoLowest.setText("Improper search term")
            self.txtInfoHighest.setTextColor(QColor(250, 50, 90))
            self.txtInfoLowest.setTextColor(QColor(250, 50, 90))
            return
        # A search term was given, so make the request
        payload = self.ebay.make_payload(
            self.keywords, self.excluded_keywords, 
            self.max_search_results, self.category_id, 
            self.remove_outliers, self.site_id, self.aspects
            )
        # Store retrieved data locally
        response = self.ebay.make_request(payload)
        if "message" not in response: 
            item_count = response["results"] 
            print(f"Number of results: {item_count}")
        # Store retrieved data for file saving
        self.default_response = response
        # Sort the data and retrieve the converted images
        descendingResults = self.utils.get_data(response, "desc")
        ascendingResults = self.utils.get_data(response, "asc")
        imgHigh = self.utils.get_pixmap(response, "desc")
        imgLow = self.utils.get_pixmap(response, "asc")
        
        # If response status code is not OK, exit method
        self.handle_api_error()
        
        # Render images on the interface if there are images to convert
        if imgHigh is not None and imgLow is not None:
            self.render_images(response, imgHigh, imgLow, descendingResults, ascendingResults)
        else: # The response is empty
            self.lblCardHighest.setText("No data was found")
            self.lblCardLowest.setText("No data was found")
        
        print(f"\n--------Values Used--------\n")
        print(f"Payload Aspects: {payload}")
        print(f"Keyword: {self.keywords}\n")    

    def openSettingsWindow(self):
        '''Open the settings UI when 'Settings' clicked'''
        self.settingsWindow.settings_ui.show()
      
    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Comps.exe"))
        self.lblCategory.setText(_translate("mainWindow", "Category"))
        self.lblGraded.setText(_translate("mainWindow", "Graded"))
        self.lblService.setText(_translate("mainWindow", "Service"))
        self.btnClear.setText(_translate("mainWindow", "Clear"))
        self.btnExit.setText(_translate("mainWindow", "Exit"))
        self.btnSearch.setText(_translate("mainWindow", "Search"))
        self.lblTitle.setText(_translate("mainWindow", "COMPS.EXE"))
        titleFont = QtGui.QFont("Futura PT", 28)
        self.lblTitle.setFont(titleFont)
        self.tabMain.setTabText(self.tabMain.indexOf(
            self.tabHighest), _translate("mainWindow", "Highest"))
        self.tabMain.setTabToolTip(self.tabMain.indexOf(
            self.tabHighest), _translate("mainWindow", "Highest Sold Price"))
        self.tabMain.setTabText(self.tabMain.indexOf(
            self.tabLowest), _translate("mainWindow", "Lowest"))
        self.tabMain.setTabToolTip(self.tabMain.indexOf(
            self.tabLowest), _translate("mainWindow", "Lowest Sold Price"))
        self.tabMain.setTabText(self.tabMain.indexOf(
            self.tabHistory), _translate("mainWindow", "History"))
        self.tabMain.setTabToolTip(self.tabMain.indexOf(
            self.tabHistory), _translate("mainWindow", "Sales History"))

