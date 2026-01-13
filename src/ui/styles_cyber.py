
# Cyber Sim 2.0 - Dark Theme (Default)
CYBER_STYLESHEET = """
/* --- Global Window & Fonts --- */
QMainWindow, QWidget {
    background-color: #0d1117; /* GitHub Dark Dimmed */
    color: #c9d1d9;
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    font-size: 14px;
}
/* ... (Keep existing Dark styles, abbreviated here for brevity if overwriting entire file) */
/* Actually, I should keep the full file content to avoid breaking it. */
/* Re-pasting the full DARK content + LIGHT content below */

QLabel[class="h1"] { font-size: 26px; font-weight: 800; color: #ffffff; padding-bottom: 5px; }
QLabel[class="h2"] { font-size: 18px; font-weight: 600; color: #58a6ff; margin-top: 15px; margin-bottom: 5px; }
QLabel[class="mono"] { font-family: 'Consolas', 'Courier New', monospace; color: #79c0ff; }

/* Sidebar */
QWidget#Sidebar { background-color: #010409; border-right: 1px solid #30363d; }
QPushButton[class="nav_btn"] { text-align: left; padding: 12px 20px; background-color: transparent; border: none; border-left: 3px solid transparent; color: #8b949e; font-size: 14px; }
QPushButton[class="nav_btn"]:hover { background-color: #161b22; color: #c9d1d9; }
QPushButton[class="nav_btn"]:checked { background-color: #161b22; color: #58a6ff; border-left: 3px solid #58a6ff; font-weight: bold; }
QLabel[class="category_header"] { color: #8b949e; font-size: 11px; font-weight: bold; text-transform: uppercase; padding: 15px 20px 5px 20px; }

/* Tabs */
QTabWidget::pane { border: 1px solid #30363d; background: #0d1117; top: -1px; }
QTabBar::tab { background: #161b22; border: 1px solid #30363d; color: #8b949e; padding: 10px 20px; margin-right: 2px; border-top-left-radius: 4px; border-top-right-radius: 4px; }
QTabBar::tab:selected { background: #0d1117; color: #58a6ff; border-bottom: 1px solid #0d1117; font-weight: bold; }
QTabBar::tab:hover { background: #21262d; color: #c9d1d9; }

/* Cards & Components */
QGroupBox { border: 1px solid #30363d; border-radius: 6px; margin-top: 24px; background-color: #161b22; padding: 15px; }
QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px; margin-left: 10px; color: #58a6ff; font-weight: bold; background-color: #0d1117; border: 1px solid #30363d; border-radius: 4px; }
QLineEdit, QTextEdit, QTextBrowser { background-color: #0d1117; border: 1px solid #30363d; border-radius: 6px; color: #c9d1d9; padding: 8px; selection-background-color: #1f6feb; }
QLineEdit:focus, QTextEdit:focus { border: 1px solid #58a6ff; }
QPushButton { background-color: #21262d; border: 1px solid #30363d; color: #c9d1d9; padding: 6px 16px; border-radius: 6px; font-weight: 600; }
QPushButton:hover { background-color: #30363d; border-color: #8b949e; }
QPushButton[class="primary"] { background-color: #238636; color: white; border: 1px solid #2ea043; }
QPushButton[class="primary"]:hover { background-color: #2ea043; }
QPushButton[class="danger"] { background-color: #da3633; color: white; border: 1px solid #f85149; }
QSplitter::handle { background: #30363d; height: 2px; }
QSplitter::handle:hover { background: #58a6ff; }
"""

# Cyber Sim 2.0 - Light Theme (Day Mode)
LIGHT_STYLESHEET = """
/* --- Global Window & Fonts --- */
QMainWindow, QWidget {
    background-color: #f6f8fa; /* GitHub Light */
    color: #24292f;
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    font-size: 14px;
}

QLabel[class="h1"] { font-size: 26px; font-weight: 800; color: #24292f; padding-bottom: 5px; }
QLabel[class="h2"] { font-size: 18px; font-weight: 600; color: #0969da; margin-top: 15px; margin-bottom: 5px; }
QLabel[class="mono"] { font-family: 'Consolas', 'Courier New', monospace; color: #0550ae; }

/* Sidebar */
QWidget#Sidebar { background-color: #ffffff; border-right: 1px solid #d0d7de; }
QPushButton[class="nav_btn"] { text-align: left; padding: 12px 20px; background-color: transparent; border: none; border-left: 3px solid transparent; color: #57606a; font-size: 14px; }
QPushButton[class="nav_btn"]:hover { background-color: #f6f8fa; color: #24292f; }
QPushButton[class="nav_btn"]:checked { background-color: #f6f8fa; color: #0969da; border-left: 3px solid #0969da; font-weight: bold; }
QLabel[class="category_header"] { color: #57606a; font-size: 11px; font-weight: bold; text-transform: uppercase; padding: 15px 20px 5px 20px; }

/* Tabs */
QTabWidget::pane { border: 1px solid #d0d7de; background: #ffffff; top: -1px; }
QTabBar::tab { background: #f6f8fa; border: 1px solid #d0d7de; color: #57606a; padding: 10px 20px; margin-right: 2px; border-top-left-radius: 4px; border-top-right-radius: 4px; }
QTabBar::tab:selected { background: #ffffff; color: #0969da; border-bottom: 1px solid #ffffff; font-weight: bold; }
QTabBar::tab:hover { background: #ffffff; color: #24292f; }

/* Cards & Components */
QGroupBox { border: 1px solid #d0d7de; border-radius: 6px; margin-top: 24px; background-color: #ffffff; padding: 15px; }
QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px; margin-left: 10px; color: #0969da; font-weight: bold; background-color: #f6f8fa; border: 1px solid #d0d7de; border-radius: 4px; }
QLineEdit, QTextEdit, QTextBrowser { background-color: #ffffff; border: 1px solid #d0d7de; border-radius: 6px; color: #24292f; padding: 8px; selection-background-color: #0969da; selection-color: white; }
QLineEdit:focus, QTextEdit:focus { border: 1px solid #0969da; }
QPushButton { background-color: #f6f8fa; border: 1px solid #d0d7de; color: #24292f; padding: 6px 16px; border-radius: 6px; font-weight: 600; }
QPushButton:hover { background-color: #f3f4f6; border-color: #8c959f; }
QPushButton[class="primary"] { background-color: #2da44e; color: white; border: 1px solid #2da44e; }
QPushButton[class="primary"]:hover { background-color: #2c974b; }
QPushButton[class="danger"] { background-color: #cf222e; color: white; border: 1px solid #d1242f; }
QSplitter::handle { background: #d0d7de; height: 2px; }
QSplitter::handle:hover { background: #0969da; }
"""
