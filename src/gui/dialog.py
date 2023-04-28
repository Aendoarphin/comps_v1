from PyQt6.QtWidgets import QMessageBox

def show_dialog(dialog_type, message):
    msg = QMessageBox()
    if dialog_type == "error":
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Error")
    elif dialog_type == "success":
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Success")
    else:
        raise ValueError("Invalid dialog type")

    msg.setText(message)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    ok_button = msg.button(QMessageBox.StandardButton.Ok)
    ok_button.setStyleSheet("QPushButton{\n"
                "color: white;\n"
                "border: 1px solid white;\n"
                "border-radius: 10px;\n"
                "padding: 5px 10px 5px 10px;\n"
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
                "color: rgb(63, 71, 79);\n"
                "border: 1px solid white;\n"
                "border-radius: 12px;\n"
                "padding: 5px;\n"
                "background-color: white;\n"
                "animation: fadeIn 5s;\n"
                "}")
    msg.setStyleSheet("background-color: rgb(63, 71, 79); color: white; padding: 10px")
    msg.exec()


