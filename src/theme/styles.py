from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, \
    QTabWidget, QRadioButton, QMenu, QMenuBar, QTextBrowser
from PyQt6.QtCore import QObject

# Applies to widgets three vars representing a color theme

class Styles:
    # Color sets for theme selection
    default_theme = {
        "foreground": "rgb(220, 220, 220)",
        "background": "rgb(63, 71, 79)",
        "accent": "rgb(78, 88, 98)",
        "fore_inverse": "rgb(35, 35, 35)",
        "back_inverse": "rgb(235, 235, 235)"
    }

    light_theme = {
        "foreground": "rgb(63, 71, 79)",
        "background": "rgb(240, 240, 240)",
        "accent": "rgb(225, 225, 225)",
        "fore_inverse": "rgb(192, 192, 192)",
        "back_inverse": "rgb(15, 15, 15)"
    }

    dark_theme = {
        "foreground": "rgb(220, 220, 220)",
        "background": "rgb(40, 40, 40)",
        "accent": "rgb(55, 55, 55)",
        "fore_inverse": "rgb(35, 35, 35)",
        "back_inverse": "rgb(215, 215, 215)"
    }

    def apply_style(window_instance:QObject, obj_name, color_palette: dict):
        my_widgets = [QMainWindow, QLabel, QLineEdit, QPushButton, QRadioButton, 
                    QTabWidget, QMenu, QMenuBar, QTextBrowser]
        
        widget = getattr(window_instance, obj_name)  # Get the object by name from the instance
        
        if isinstance(widget, tuple(my_widgets)):  # Check if it's one of the specified widget types
            # Apply the appropriate stylesheet for the widget type
            if isinstance(widget, QMainWindow):
                return widget.setStyleSheet(f"background-color: {color_palette['background']}")
            elif isinstance(widget, QLabel):
                if widget.objectName() == "lblTitle":
                    return widget.setStyleSheet(
                        f"color: {color_palette['foreground']}; \n"
                        f"border: 1px solid {color_palette['foreground']}; border-radius: 10px; \n"
                        f"padding-left: 10px; padding-right: 10px"
                    )
                elif widget.objectName() in ("lblCardHighest", "lblCardLowest"):
                    return widget.setStyleSheet(
                        f"border-radius: 10px;\n"
                        f"background-color: {color_palette['accent']}; \n"
                        f"color: {color_palette['foreground']};"
                    )
                elif widget.objectName() == "lblCategory":
                    return widget.setStyleSheet(
                        f"font-size: 14pt; color: {color_palette['foreground']}; text-align: center;"
                    )
                elif widget.objectName() == "lblGraded":
                    return widget.setStyleSheet(
                        f"font-size: 12pt; color: {color_palette['foreground']}; text-align: center;"
                    )
                else:
                    return widget.setStyleSheet(f"color: {color_palette['foreground']}")
            elif isinstance(widget, QLineEdit):
                return widget.setStyleSheet(
                    f"border: none; border-radius: 10px; margin: 0 10px; \n"
                    f"color: {color_palette['foreground']}; padding: 3px; \n"
                    f"background-color: {color_palette['accent']};"
                )
            elif isinstance(widget, QPushButton):
                return widget.setStyleSheet(
                    f"""
                    QPushButton {{
                        color: {color_palette['foreground']};
                        border: 1px solid {color_palette['foreground']};
                        border-radius: 10px;
                        padding: 3px;
                    }}
                    QPushButton:pressed {{
                        color: {color_palette['fore_inverse']};
                        border: 1px solid {color_palette['foreground']};
                        border-radius: 10px;
                        padding: 3px;
                        background-color: {color_palette['back_inverse']};
                    }}
                    """
                    )
            elif isinstance(widget, QTabWidget):
                return widget.setStyleSheet(
                    f"""
                    QTabWidget::pane{{
                        border: 2px solid {color_palette['accent']};
                        border-radius: 15px;
                        padding: 5px
                    }}

                    QTabWidget::tab-bar{{
                        alignment: right
                    }}

                    QTabBar::tab{{
                        background-color: {color_palette['background']};
                        color: {color_palette['foreground']};
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
                        background-color: {color_palette['back_inverse']};
                        color: {color_palette['fore_inverse']};
                    }}
                    """
                    )
            elif isinstance(widget, QMenu):
                return widget.setStyleSheet(
                    f"""
                    QMenu {{
                    background-color: {color_palette['background']};
                    color: {color_palette['foreground']};
                    }}

                    QMenu::item {{
                    background-color: {color_palette['background']};
                    color: {color_palette['foreground']};
                    }}

                    QMenu::item:selected {{
                    background-color: {color_palette['back_inverse']};
                    color: {color_palette['fore_inverse']};
                    }}
                    """
                )
            elif isinstance(widget, QMenuBar):
                return widget.setStyleSheet(
                    f"""
                    QMenuBar {{
                    background-color: {color_palette['background']};
                    color: {color_palette['foreground']};
                    }}
                    
                    QMenuBar::item {{
                    background-color: {color_palette['background']};
                    color: {color_palette['foreground']};
                    }}

                    QMenuBar::item:selected {{
                        background-color: {color_palette['back_inverse']};
                        color: {color_palette['fore_inverse']};
                    }}
                    """
                )
            elif isinstance(widget, QRadioButton):
                return widget.setStyleSheet(f"color: {color_palette['foreground']}")
            elif isinstance(widget, QTextBrowser):
                return widget.setStyleSheet(
                    f"font-size: 10pt; color: {color_palette['foreground']}; padding: 5px;")
    