from PySide6.QtWidgets import QApplication, QMainWindow
from uiFiles.serverUI import Ui_Server
import sys

class interfaceServer(QMainWindow, Ui_Server):  # Change QDialog to QMainWindow
    def __init__(self, parent=None):
        super(interfaceServer, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Server")
        self.setGeometry(100, 100, 450, 400)
        self.setFixedSize(450, 400)

        # Set up the text edit widgets to be read-only
        self.textEdit.setReadOnly(True)
        self.textEdit_2.setReadOnly(True)

        # Set up the line edit widget to accept only numbers
        # self.lineEdit.setValidator(QIntValidator(0, 10000))  # Adjust the range as needed

    def update_received_messages(self, message):
        self.textEdit.append(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = interfaceServer()
    window.show()
    sys.exit(app.exec())