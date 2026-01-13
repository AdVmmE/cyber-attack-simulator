
# Global Styles for Cyber Sim

MODERN_STYLESHEET = """
/* Global Window */
QMainWindow, QWidget {
    background-color: #121212;
    color: #e0e0e0;
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    font-size: 14px;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: #1e1e1e;
    width: 10px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #444;
    min-height: 20px;
    border-radius: 5px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Group Boxes - Modern Cards */
QGroupBox {
    border: 1px solid #333;
    border-radius: 8px;
    margin-top: 20px;
    background-color: #1e1e1e;
    padding: 15px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
    color: #007acc;
    font-weight: bold;
    font-size: 14px;
    background-color: transparent;
}

/* Inputs */
QLineEdit, QTextEdit, QTextBrowser {
    background-color: #252526;
    border: 1px solid #3e3e42;
    border-radius: 4px;
    color: white;
    padding: 5px;
    selection-background-color: #094771;
}
QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #007acc;
}

/* Buttons */
QPushButton {
    background-color: #333333;
    color: white;
    border: 1px solid #444;
    border-radius: 4px;
    padding: 6px 15px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #444444;
    border: 1px solid #555;
}
QPushButton:pressed {
    background-color: #007acc;
    border: 1px solid #007acc;
}
QPushButton:disabled {
    background-color: #222;
    color: #666;
    border: 1px solid #333;
}

/* Action Buttons (Primary) */
QPushButton[class="primary"] {
    background-color: #007acc;
    border: none;
}
QPushButton[class="primary"]:hover {
    background-color: #005a9e;
}

/* Red / Danger Buttons */
QPushButton[class="danger"] {
    background-color: #d62828;
    border: none;
}
QPushButton[class="danger"]:hover {
    background-color: #a81b1b;
}

/* Headers */
QLabel[class="h1"] {
    font-size: 24px;
    font-weight: bold;
    color: white;
    margin-bottom: 10px;
}
QLabel[class="h2"] {
    font-size: 18px;
    font-weight: bold;
    color: #cccccc;
    margin-top: 10px;
}

/* Sidebar Specific (Applied in Sidebar, but can be global) */
"""
