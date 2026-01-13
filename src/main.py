import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from ui.main_window import MainWindow
from ui.styles_cyber import CYBER_STYLESHEET

def main():
    # Setup Application
    app = QApplication(sys.argv)
    
    # Apply Global Cyber Stylesheet (Default)
    app.setStyleSheet(CYBER_STYLESHEET)
    
    # Set App Icon
    from PySide6.QtGui import QIcon
    import os
    icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.png')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Dark Mode Palette (Keep for fallback/system dialogs)
    from PySide6.QtGui import QPalette, QColor, QIcon
    palette = QPalette()

    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    # Enable High DPI scaling
    os.environ["QT_FONT_DPI"] = "96" # Fix for some windows scaling issues, optional
    
    # Create Main Window
    window = MainWindow()
    window.show()
    
    # Run Event Loop
    sys.exit(app.exec())

if __name__ == "__main__":
    # Add src to pythonpath if running directly
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    main()
