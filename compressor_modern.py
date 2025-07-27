import sys, os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QFileDialog, QLabel, QMessageBox, QHBoxLayout)
from PyQt5.QtGui import QFont, QIcon
from patoolib import extract_archive, create_archive


class CompressorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Universal Compressor & Extractor")
        self.setGeometry(200, 100, 500, 400)
        self.setWindowIcon(QIcon("icon.png"))  # optional icon

        self.archive_file = ""
        self.dest_folder = ""
        self.files_to_compress = []
        self.output_file = ""

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title = QLabel("Universal Compressor & Extractor")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #0078d4; margin-bottom: 20px; text-align: center;")
        layout.addWidget(title)

        # --- Extract Section ---
        extract_label = QLabel("Extract Files")
        extract_label.setFont(QFont("Arial", 14))
        layout.addWidget(extract_label)

        extract_btn1 = QPushButton("Select Archive File")
        extract_btn1.setStyleSheet(self.button_style())
        extract_btn1.clicked.connect(self.select_archive)
        layout.addWidget(extract_btn1)

        extract_btn2 = QPushButton("Select Destination Folder")
        extract_btn2.setStyleSheet(self.button_style())
        extract_btn2.clicked.connect(self.select_dest)
        layout.addWidget(extract_btn2)

        extract_btn3 = QPushButton("Extract Now")
        extract_btn3.setStyleSheet(self.main_button_style())
        extract_btn3.clicked.connect(self.extract)
        layout.addWidget(extract_btn3)

        layout.addSpacing(20)

        # --- Compress Section ---
        compress_label = QLabel("Compress Files")
        compress_label.setFont(QFont("Arial", 14))
        layout.addWidget(compress_label)

        compress_btn1 = QPushButton("Select Files to Compress")
        compress_btn1.setStyleSheet(self.button_style())
        compress_btn1.clicked.connect(self.select_files)
        layout.addWidget(compress_btn1)

        compress_btn2 = QPushButton("Select Output File")
        compress_btn2.setStyleSheet(self.button_style())
        compress_btn2.clicked.connect(self.select_output)
        layout.addWidget(compress_btn2)

        compress_btn3 = QPushButton("Compress Now")
        compress_btn3.setStyleSheet(self.main_button_style())
        compress_btn3.clicked.connect(self.compress)
        layout.addWidget(compress_btn3)

        self.setLayout(layout)
        self.setStyleSheet("background: #f9f9f9;")

    # ---------- Button Styles ----------
    def button_style(self):
        return """QPushButton {
                    background: #e5e5e5; padding: 10px;
                    border-radius: 6px; font-size: 13px;
                 }
                 QPushButton:hover {
                    background: #d1d1d1;
                 }"""

    def main_button_style(self):
        return """QPushButton {
                    background: #0078d4; color: white;
                    padding: 10px; border-radius: 6px; font-size: 14px;
                 }
                 QPushButton:hover {
                    background: #005a9e;
                 }"""

    # ---------- Functions ----------
    def select_archive(self):
        self.archive_file, _ = QFileDialog.getOpenFileName(self, "Select Archive File")

    def select_dest(self):
        self.dest_folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")

    def extract(self):
        if not self.archive_file or not self.dest_folder:
            QMessageBox.critical(self, "Error", "Select archive and destination folder!")
            return

        try:
            extract_archive(self.archive_file, outdir=self.dest_folder)
            QMessageBox.information(self, "Success", f"Extracted to {self.dest_folder}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def select_files(self):
        self.files_to_compress, _ = QFileDialog.getOpenFileNames(self, "Select Files to Compress")

    def select_output(self):
        self.output_file, _ = QFileDialog.getSaveFileName(self, "Save Archive As", "", "ZIP Files (*.zip);;RAR Files (*.rar);;7Z Files (*.7z)")

    def compress(self):
        if not self.files_to_compress or not self.output_file:
            QMessageBox.critical(self, "Error", "Select files and output path!")
            return

        try:
            create_archive(self.output_file, self.files_to_compress)
            QMessageBox.information(self, "Success", f"Compressed to {self.output_file}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CompressorApp()
    win.show()
    sys.exit(app.exec_())
