from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QLineEdit, QMessageBox
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from main import gui_entry


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('SE Server Mods')
        self.setFixedSize(300, 115)

        layout = QVBoxLayout()

        # Add button for editing mods.txt
        self.edit_mods_button = QPushButton('Edit mods.txt')
        self.edit_mods_button.clicked.connect(self.edit_mods_txt)
        layout.addWidget(self.edit_mods_button)

        # Add label aligned to top left
        self.label = QLabel('Enter Sandbox_config.sbc file path:')
        self.label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        layout.addWidget(self.label)

        # Add QLineEdit for user input
        self.input_box = QLineEdit()
        layout.addWidget(self.input_box)

        # Create a QHBoxLayout for the buttons
        button_layout = QHBoxLayout()

        # Add browse button
        self.browse_button = QPushButton('Browse..')
        self.browse_button.clicked.connect(self.browse_for_sandbox_file)
        button_layout.addWidget(self.browse_button)

        # Add submit button
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.run_script)
        button_layout.addWidget(self.submit_button)

        # Add the button layout to the main layout
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def edit_mods_txt(self):
        # Open mods.txt file in the default text editor
        #QProcess.startDetached("notepad.exe", ["mods.txt"])
        QDesktopServices.openUrl(QUrl.fromLocalFile('mods.txt'))

    def browse_for_sandbox_file(self):
        options = QFileDialog.Option.DontUseNativeDialog
        sandbox_file, _ = QFileDialog.getOpenFileName(self, "Select Sandbox_config.sbc File", "",
                                                      "Sandbox Files (*.sbc)", options=options)
        if sandbox_file:
            # Set the file path to the input box
            self.input_box.setText(sandbox_file)

    def run_script(self):
        # Get the file path from the input box
        sandbox_file = self.input_box.text().strip()
        if sandbox_file:
            result = gui_entry(file_path=sandbox_file)
            self.show_popup('STATUS', result)

    def show_popup(self, title, message):
        popup = QMessageBox()
        popup.setWindowTitle(title)
        popup.setText(message)
        popup.exec()


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
