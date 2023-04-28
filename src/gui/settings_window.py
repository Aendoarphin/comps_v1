from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import QMainWindow
from gui.dialog import show_dialog
from utils import Utils
from ebay.ebay import Ebay
from theme.styles import Styles
import json, os

# Constructs the settings window

class Ui_settingsWindow(QObject):
    # Signal to notify main window of theme change
    theme_changed = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        # Location of settings
        self.settings_location = os.path.join(os.path.expanduser("~"), "Downloads\CompsExe")
        # Location for default save
        self.default_save_location = ""
        # To use utils
        self.utils = Utils()
        # Variable to store theme state
        self.theme = "default"
        # Color theme
        self.current_theme = Styles.default_theme
        # Flag: if new fields were modified
        self.settings_changed = False
        
        self.settings_ui = QMainWindow()
        self.ebay = Ebay()
        self.setupUi()
        self.update_key()
        self.update_default_path()
        
    # Construct the window
    def setupUi(self):
        self.settings_ui.setObjectName("settingsWindow")
        self.settings_ui.setEnabled(True)
        self.settings_ui.resize(390, 437)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settings_ui.sizePolicy().hasHeightForWidth())
        self.settings_ui.setSizePolicy(sizePolicy)
        self.settings_ui.setMinimumSize(QtCore.QSize(390, 437))
        self.settings_ui.setMaximumSize(QtCore.QSize(390, 437))
        self.settings_ui.setBaseSize(QtCore.QSize(820, 630))
        font = QtGui.QFont()
        font.setKerning(True)
        self.settings_ui.setFont(font)
        self.settings_ui.setAutoFillBackground(False)
        self.settings_ui.setStyleSheet(f"background-color: {self.current_theme['background']}")
        self.settings_ui.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.settings_ui.setDocumentMode(False)
        self.settings_ui.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.settings_ui.setDockNestingEnabled(False)
        self.settings_ui.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(parent=self.settings_ui)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buttonBox.setFont(font)
        self.buttonBox.setStyleSheet("QPushButton{\n"
            f"color: {self.current_theme['foreground']};\n"
            f"border: 1px solid {self.current_theme['foreground']};\n"
            "border-radius: 12px;\n"
            "padding: 5px;\n"
            "}\n"
            "@keyframes fadeOut{\n"
            "from{opacity: 1;}\n"
            "to{opacity: 0;}\n"
            "}\n"
            "@keyframes fadeIn{\n"
            "from{opacity: 0;}\n"
            "to{opacity: 1;}\n"
            "}\n"
            "QPushButton:pressed{\n"
            f"color: {self.current_theme['fore_inverse']};\n"
            f"border: 1px solid {self.current_theme['fore_inverse']};\n"
            "border-radius: 12px;\n"
            "padding: 5px;\n"
            f"background-color: {self.current_theme['back_inverse']};\n"
            
            "}")
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Apply|QtWidgets.QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 1)
        self.groupTheme = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupTheme.setMinimumSize(QtCore.QSize(0, 55))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setKerning(True)
        self.groupTheme.setFont(font)
        self.groupTheme.setStyleSheet(f"border-style: none; color: {self.current_theme['foreground']}")
        self.groupTheme.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.groupTheme.setFlat(False)
        self.groupTheme.setCheckable(False)
        self.groupTheme.setObjectName("groupTheme")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupTheme)
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 1)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        
        self.rbThemeDefault = QtWidgets.QRadioButton(parent=self.groupTheme)
        self.rbThemeDefault.setObjectName("rbThemeDefault")
        self.horizontalLayout_2.addWidget(self.rbThemeDefault)

        self.rbThemeLight = QtWidgets.QRadioButton(parent=self.groupTheme)
        self.rbThemeLight.setObjectName("rbThemeLight")
        self.horizontalLayout_2.addWidget(self.rbThemeLight)
        
        self.rbThemeDark = QtWidgets.QRadioButton(parent=self.groupTheme)
        self.rbThemeDark.setObjectName("rbThemeDark")
        self.horizontalLayout_2.addWidget(self.rbThemeDark)
        
        self.gridLayout.addWidget(self.groupTheme, 1, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 4, 0, 1, 1)
        self.lblKey = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        self.lblKey.setFont(font)
        self.lblKey.setStyleSheet(f"color: {self.current_theme['foreground']};")
        self.lblKey.setIndent(9)
        self.lblKey.setObjectName("lblKey")
        self.gridLayout_2.addWidget(self.lblKey, 0, 0, 1, 1)
        self.txtDefaultPath = QtWidgets.QLineEdit(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtDefaultPath.sizePolicy().hasHeightForWidth())
        self.txtDefaultPath.setSizePolicy(sizePolicy)
        self.txtDefaultPath.setStyleSheet("border-style: none; \n"
            "border-radius: 10px; \n"
            f"color: {self.current_theme['foreground']}; \n"
            "padding: 5px; \n"
            f"background-color: {self.current_theme['accent']}; \n"
            "margin-left:8px")
        self.txtDefaultPath.setObjectName("txtDefaultPath")
        self.gridLayout_2.addWidget(self.txtDefaultPath, 3, 0, 1, 1)
        self.lblDefaultPath = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        self.lblDefaultPath.setFont(font)
        self.lblDefaultPath.setStyleSheet(f"color: {self.current_theme['foreground']};")
        self.lblDefaultPath.setIndent(9)
        self.lblDefaultPath.setObjectName("lblDefaultPath")
        self.gridLayout_2.addWidget(self.lblDefaultPath, 2, 0, 1, 1)
        self.txtKey = QtWidgets.QLineEdit(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtKey.sizePolicy().hasHeightForWidth())
        self.txtKey.setSizePolicy(sizePolicy)
        self.txtKey.setStyleSheet("border-style: none; \n"
            "border-radius: 10px; \n"
            f"color: {self.current_theme['foreground']}; \n"
            "padding: 5px; \n"
            f"background-color: {self.current_theme['accent']}; \n"
            "margin-left: 8px")
        self.txtKey.setObjectName("txtKey")
        self.gridLayout_2.addWidget(self.txtKey, 1, 0, 1, 1)
        self.btnKey = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnKey.sizePolicy().hasHeightForWidth())
        self.btnKey.setSizePolicy(sizePolicy)
        self.btnKey.setMinimumSize(QtCore.QSize(0, 0))
        self.btnKey.setStyleSheet("QPushButton{\n"
            f"            color: {self.current_theme['foreground']};\n"
            f"            border: 1px solid {self.current_theme['foreground']};\n"
            "            border-radius: 12px;\n"
            "            padding: 5px;\n"
            "}\n"
            "@keyframes fadeOut{\n"
            "from{opacity: 1;}\n"
            "to{opacity: 0;}\n"
            "}\n"
            "@keyframes fadeIn{\n"
            "from{opacity: 0;}\n"
            "to{opacity: 1;}\n"
            "}\n"
            "QPushButton:pressed{\n"
            f"color: {self.current_theme['fore_inverse']};\n"
            f"border: 1px solid {self.current_theme['fore_inverse']};\n"
            "border-radius: 12px;\n"
            "padding: 5px;\n"
            f"background-color: {self.current_theme['back_inverse']};\n"
            
            "}")
        self.btnKey.setObjectName("btnKey")
        self.gridLayout_2.addWidget(self.btnKey, 1, 1, 1, 1)
        self.btnDefaultPath = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnDefaultPath.sizePolicy().hasHeightForWidth())
        self.btnDefaultPath.setSizePolicy(sizePolicy)
        self.btnDefaultPath.setStyleSheet("QPushButton{\n"
            f"           color: {self.current_theme['foreground']};\n"
            f"           border: 1px solid {self.current_theme['foreground']};\n"
            "            border-radius: 12px;\n"
            "            padding: 5px;\n"
            "}\n"
            "@keyframes fadeOut{\n"
            "from{opacity: 1;}\n"
            "to{opacity: 0;}\n"
            "}\n"
            "@keyframes fadeIn{\n"
            "from{opacity: 0;}\n"
            "to{opacity: 1;}\n"
            "}\n"
            "QPushButton:pressed{\n"
            f"color: {self.current_theme['fore_inverse']};\n"
            f"border: 1px solid {self.current_theme['fore_inverse']};\n"
            "border-radius: 12px;\n"
            "padding: 5px;\n"
            f"background-color: {self.current_theme['back_inverse']};\n"
            
            "}")
        self.btnDefaultPath.setObjectName("btnDefaultPath")
        self.gridLayout_2.addWidget(self.btnDefaultPath, 3, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 3, 0, 1, 1)
        
        self.lblHelp = QtWidgets.QLabel(self.centralwidget)
        self.lblHelp.setObjectName(f"lblHelp")
        self.lblHelp.setMinimumSize(QtCore.QSize(0, 150))
        self.lblHelp.setStyleSheet(f"padding: 10px; color: {self.current_theme['foreground']};")
        self.lblHelp.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading
                                  |QtCore.Qt.AlignmentFlag.AlignLeft
                                  |QtCore.Qt.AlignmentFlag.AlignTop)
        self.lblHelp.setWordWrap(True)
        self.lblHelp.setIndent(-1)
        self.lblHelp.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)

        self.gridLayout_2.addWidget(self.lblHelp, 4, 0, 1, 1)
        
        self.settings_ui.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=self.settings_ui)
        self.menubar.setEnabled(False)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 390, 22))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menubar.sizePolicy().hasHeightForWidth())
        self.menubar.setSizePolicy(sizePolicy)
        self.menubar.setObjectName("menubar")
        self.settings_ui.setMenuBar(self.menubar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.settings_ui)
        self.settings_ui.setTabOrder(self.txtKey, self.txtDefaultPath)
        self.settings_ui.setTabOrder(self.txtDefaultPath, self.rbThemeDefault)
        self.settings_ui.setTabOrder(self.rbThemeDefault, self.rbThemeLight)
        self.settings_ui.setTabOrder(self.rbThemeLight, self.rbThemeDark)
        self.settings_ui.setTabOrder(self.rbThemeDark, self.btnKey)
        self.settings_ui.setTabOrder(self.btnKey, self.btnDefaultPath)
        # Handler, user may leave one field unchanged after applying settings
        def apply_button_clicked():
            api_key = self.txtKey.text()
            save_location = self.txtDefaultPath.text()
            theme = self.theme
            user_settings = {"key": api_key, "default_file_location": save_location, "theme": theme}
            
            # If settings changed
            if self.settings_changed == True:
                self.save_settings(user_settings)
                self.txtKey.setText(api_key)
                self.txtDefaultPath.setText(save_location)
                self.settings_changed = False
                show_dialog("success", f"Your settings have been updated: \n{self.settings_location}\n"
                            f"Please restart the program for your settings to take effect.")
            else:
                show_dialog("success", "No new values given. Using default preferences.")
                
            self.settings_ui.close()

        # Event listeners
        self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Close).clicked.connect(self.settings_ui.close)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Apply).clicked.connect(apply_button_clicked)
        QtCore.QMetaObject.connectSlotsByName(self.settings_ui)
        
        def change_theme():
            # If theme is checked and is not the same as current theme
            if self.rbThemeDefault.isChecked() == True and self.theme != 'default':
                self.theme = 'default'
                self.set_color(self.theme)
            elif self.rbThemeDark.isChecked() == True and self.theme != 'dark':
                self.theme = 'dark'
                self.set_color(self.theme)
            elif self.rbThemeLight.isChecked() == True and self.theme != 'light':
                self.theme = 'light'
                self.set_color(self.theme)
                
        # Change the visual theme
        self.rbThemeDefault.clicked.connect(change_theme)
        self.rbThemeDark.clicked.connect(change_theme)
        self.rbThemeLight.clicked.connect(change_theme)
        
    def set_color(self, current_theme:str):
        # Set the new theme 
        self.set_theme(current_theme)
        if current_theme == "default":
            self.current_theme = Styles.default_theme
        elif current_theme == "dark":
            self.current_theme = Styles.dark_theme
        elif current_theme == "light":
            self.current_theme = Styles.light_theme
        self.settings_changed = True
        self.settings_ui.setStyleSheet(
            f"background-color: {self.current_theme['background']};\n"
        )
        self.lblHelp.setStyleSheet(
            f"color: {self.current_theme['foreground']};\n"
            "padding: 10px; \n"
        )
        self.lblKey.setStyleSheet(
            f"color: {self.current_theme['foreground']};\n"
        )
        self.lblDefaultPath.setStyleSheet(
            f"color: {self.current_theme['foreground']};\n"
        )
        self.groupTheme.setStyleSheet(
            f"color: {self.current_theme['foreground']};\n"
        )
        self.buttonBox.setStyleSheet(
            "QPushButton{\n"
            f"color: {self.current_theme['foreground']};\n"
            f"border: 1px solid {self.current_theme['foreground']};\n"
            "border-radius: 12px;\n"
            "padding: 5px;\n"
            "}\n"
            "QPushButton:pressed{\n"
            f"color: {self.current_theme['fore_inverse']};\n"
            f"border: 1px solid {self.current_theme['fore_inverse']};\n"
            "border-radius: 12px;\n"
            "padding: 5px;\n"
            f"background-color: {self.current_theme['back_inverse']};\n"
            "}"
        )
        self.btnDefaultPath.setStyleSheet(
            "QPushButton{\n"
            f"color: {self.current_theme['foreground']};\n"
            f"border: 1px solid {self.current_theme['foreground']};\n"
            "border-radius: 12px;\n"
            "padding: 5px;\n"
            "}\n"
            "QPushButton:pressed{\n"
            f"color: {self.current_theme['fore_inverse']};\n"
            f"border: 1px solid {self.current_theme['fore_inverse']};\n"
            "border-radius: 12px;\n"
            "padding: 5px;\n"
            f"background-color: {self.current_theme['back_inverse']};\n"
            "}"
        )
        self.btnKey.setStyleSheet(
            "QPushButton{\n"
            f"color: {self.current_theme['foreground']};\n"
            f"border: 1px solid {self.current_theme['foreground']};\n"
            "border-radius: 12px;\n"
            "padding: 5px;\n"
            "}\n"
            "QPushButton:pressed{\n"
            f"color: {self.current_theme['fore_inverse']};\n"
            f"border: 1px solid {self.current_theme['fore_inverse']};\n"
            "border-radius: 12px;\n"
            "padding: 5px;\n"
            f"background-color: {self.current_theme['back_inverse']};\n"
            "}"
        )
        self.txtDefaultPath.setStyleSheet(
            "border-style: none; \n"
            "border-radius: 10px; \n"
            f"color: {self.current_theme['foreground']}; \n"
            "padding: 5px; \n"
            f"background-color: {self.current_theme['accent']}; \n"
            "margin-left:8px"
        )
        self.txtKey.setStyleSheet(
            "border-style: none; \n"
            "border-radius: 10px; \n"
            f"color: {self.current_theme['foreground']}; \n"
            "padding: 5px; \n"
            f"background-color: {self.current_theme['accent']}; \n"
            "margin-left:8px"
        )
        print(f"Theme: {current_theme} passed")
    # Write the .json settings file
    def save_settings(self, settings: dict):
        filename = "comps_exe_user_settings.json"
        def_path = self.settings_location
            
        settings_file_path = os.path.join(def_path, filename)
        with open(settings_file_path, 'w') as f:
            json.dump(settings, f)
    # Emit signal for Ui_mainWindow, notify that the theme changed
    def set_theme(self, theme:str):
        self.theme = theme
        self.theme_changed.emit(theme)
    # Find the user settings .json file, return {} if fnf
    @staticmethod
    def load_settings():
        # Look for the settings file in the user's Downloads/CompsExe folder
        downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        comps_exe_dir = os.path.join(downloads_dir, "CompsExe")

        for root, dirs, files in os.walk(comps_exe_dir):
            if "comps_exe_user_settings.json" in files:
                settings_file_path = os.path.join(root, "comps_exe_user_settings.json")
                break

        else:
            # If the settings file isn't found, return an empty dictionary
            return {}

        # Load the settings from the file
        with open(settings_file_path, "r") as f:
            settings = json.load(f)

        return settings
    # Handler for update_key()
    def set_api(self):
        new_api = self.txtKey.text()
        payload = {
        "keywords": "Michael Jordan",  # str
        "max_search_results": "240"  # str
    }
        if self.txtKey.text() != "":
            status = self.ebay.is_valid_key(new_api, payload)
            if status == True:
                self.ebay.set_appid(new_api)
                show_dialog("success", "The key was successfully changed")
                self.settings_changed = True
            else:
                show_dialog("error", "Invalid key")
        else:
            show_dialog("error", "No key was given")   
    # txtKey: Event listener, SUBMIT or RETURN PRESSED
    def update_key(self):
        self.txtKey.returnPressed.connect(self.set_api)
        self.btnKey.clicked.connect(self.set_api)
    # Handlers for update_default_path()
    def browse_clicked(self):
        # Open the file dialog
        new_location = self.utils.choose_path()
        # Check if directory
        validated_path = self.utils.validate_path(new_location)
        # If path specified is directory and isn't empty string
        if new_location != None and validated_path != "invalid":
            # Display path
            updated_path = self.txtDefaultPath.setText(new_location)
            # A setting was changed
            self.settings_changed = True
            return updated_path
        else: # Path was not directory
            show_dialog("error", "Invalid directory")
    def return_pressed(self):
        user_path = self.txtDefaultPath.text()
        validated_path = self.utils.validate_path(user_path)
        if validated_path != None and validated_path != "invalid":
            self.txtDefaultPath.setText(validated_path)
            self.settings_changed = True
            show_dialog("success", f"The default save location was updated:\n{validated_path}")
        else:
            show_dialog("error", "Invalid directory")
    # txtDefaultPath: Event listener for RETURN PRESSED
    def update_default_path(self):
        # Function to run when user presses enter or selects from dialog
        self.txtDefaultPath.returnPressed.connect(self.return_pressed)
        self.btnDefaultPath.clicked.connect(self.browse_clicked)
    # Called from Ui_mainWindow to set api/default path from loaded user preference
    def set_api_from_settings(self, in_dict:dict):
        if isinstance(in_dict, dict):
            user_api = in_dict.get("key", "")
            self.txtKey.setText(user_api)
            self.ebay.set_appid(user_api)
        else:
            print("Error: input parameter is not a dictionary")
    def set_default_save_from_settings(self, in_dict:dict, old_path: str) -> str:
        if isinstance(in_dict, dict):
            new_path = in_dict.get("default_file_location", "")
            self.txtDefaultPath.setText(new_path)
            old_path = new_path
            return old_path
        else:
            print("Error: input parameter is not a dictionary")
            return old_path
    def set_theme_from_settings(self, in_dict:dict):
        if isinstance(in_dict, dict):
            theme_from_settings = in_dict.get("theme", "")
            return theme_from_settings
            
    def retranslateUi(self):
        
        _translate = QtCore.QCoreApplication.translate
        self.settings_ui.setWindowTitle(_translate("settingsWindow", "Settings"))
        self.groupTheme.setTitle(_translate("settingsWindow", "Theme"))
        self.rbThemeDefault.setText(_translate("settingsWindow", "Default"))
        self.rbThemeLight.setText(_translate("settingsWindow", "Light"))
        self.rbThemeDark.setText(_translate("settingsWindow", "Dark"))
        self.lblKey.setText(_translate("settingsWindow", "User API Key"))
        self.lblDefaultPath.setText(_translate("settingsWindow", "Default Save Location"))
        self.btnKey.setText(_translate("settingsWindow", "Submit"))
        self.btnDefaultPath.setText(_translate("settingsWindow", "Browse"))
        # Open user browser when link clicked
        def open_link(url):
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))
        # Info: How to get api key
        self.lblHelp.setText(QtCore.QCoreApplication.translate("settingsWindow", 
            u"<html><head/><body><p><span style=\" font-size:8pt;\">\n"
            "You can acquire an API key for </span><span style=\"\n"
            "font-size:8pt; font-weight:700;\">Comps.exe</span>\n"
            "<span style=\" font-size:8pt;\"> at </span>\n"
            "<a href=\"https://rapidapi.com/ecommet/api/ebay-average-selling-price\">\n"
            "<span style=\" font-size:8pt; text-decoration: underline; \n"
            "color:#0000ff;\">rapidapi.com</span></a><span style=\" \n"
            "font-size:8pt;\">: </span></p><p><span style=\" font-size:8pt;\">\n"
            "1. Login or sign up for a RapidAPI account</span></p><p>\n"
            "<span style=\" font-size:8pt;\">\n"
            "2. Go to 'Pricing' and select your subscription type</span></p><p>\n"
            "<span style=\" font-size:8pt;\">\n"
            "3. Find your API key labeled 'X-RapidAPI-Key' in 'Endpoints'</span></p><p>\n"
            "<span style=\" font-size:8pt; font-style:italic;\">\n"
            "NOTE: If your key appears valid but cannot be submitted, you may have \n"
            "reached the maximum call limit for that specific subscription type.</span></p></body></html>",
            None))
        self.lblHelp.setOpenExternalLinks(True)
        self.lblHelp.linkActivated.connect(open_link)
