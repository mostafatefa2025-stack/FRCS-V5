import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Financial Risk & Consulting System - FRCS V5")
        self.resize(600, 400)

        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Header Label
        label = QLabel("أهلاً بك في نظام FRCS V5 للتحليل المالي والتقييم")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 18px; font-weight: bold; color: #1E3A8A;")
        layout.addWidget(label)

        # Status Sub-label
        sub_label = QLabel("الواجهة البرمجية تعمل بنجاح!")
        sub_label.setAlignment(Qt.AlignCenter)
        sub_label.setStyleSheet("font-size: 14px; color: #059669;")
        layout.addWidget(sub_label)

        # Close Button
        btn = QPushButton("إغلاق التطبيق")
        btn.clicked.connect(self.close)
        btn.setStyleSheet("padding: 10px; font-size: 14px; background-color: #DC2626; color: white; border-radius: 5px;")
        layout.addWidget(btn)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())