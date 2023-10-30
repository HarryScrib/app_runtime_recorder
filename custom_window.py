import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFrame, QPushButton
from PyQt5.QtCore import QEvent

class CustomWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle("Custom Window Style")
        self.setGeometry(100, 100, 400, 300)
        self.setAttribute(Qt.WA_TranslucentBackground)  # Make the window background translucent

        # Set a thicker border
        self.border = 6

        # Create a central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Add a "Close" button
        self.close_button = QPushButton("Close", self)
        self.close_button.setGeometry(10, 10, 80, 30)
        self.close_button.clicked.connect(self.close_window)

        # Add a "Lock" button
        self.lock_button = QPushButton("Lock", self)
        self.lock_button.setGeometry(100, 10, 80, 30)
        self.locked = False
        self.lock_button.clicked.connect(self.toggle_lock)

        self.dragging = False
        self.locked_position = False

    def paintEvent(self, event):
        # Create custom window style with curved edges and thicker border
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(48, 48, 48)))  # Background color
        painter.setPen(QColor(48, 48, 48))  # Border color
        painter.drawRoundedRect(self.border, self.border, self.width() - 2 * self.border, self.height() - 2 * self.border, 15, 15)

    def close_window(self):
        self.close()

    def toggle_lock(self):
        if self.locked:
            self.unlock_window()
        else:
            self.lock_window()

    def lock_window(self):
        self.locked = True
        self.lock_button.setText("Unlock")  # Change button label to "Unlock"
        self.locked_position = self.pos()

    def unlock_window(self):
        self.locked = False
        self.lock_button.setText("Lock")  # Change button label to "Lock"
        self.locked_position = None

    def eventFilter(self, obj, event):
        if self.locked:
            if event.type() == QEvent.MouseButtonPress:
                # Block mouse click events outside the application's locked area
                event_pos = event.pos()
                if not self.rect().contains(QRect(event_pos, event_pos)):
                    return True

            if event.type() == QEvent.MouseButtonDblClick:
                # Disable double-clicking when locked
                return True

            if event.type() == QEvent.MouseMove:
                if self.dragging:
                    if self.locked_position:
                        # Limit movement to the locked position
                        self.move(self.locked_position)

        return super().eventFilter(obj, event)

    def mousePressEvent(self, event):
        if self.locked:
            if event.button() == Qt.LeftButton:
                self.dragging = True

    def mouseReleaseEvent(self, event):
        if self.dragging:
            self.dragging = False

def main():
    app = QApplication(sys.argv)
    window = CustomWindow()
    window.show()
    window.installEventFilter(window)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
