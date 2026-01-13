from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PySide6.QtCore import Signal, Qt

class Sidebar(QWidget):
    attack_selected = Signal(str) # Signal emitting the name of the selected attack

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setFixedWidth(280)
        self.setObjectName("Sidebar") # For CSS Grid ID
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 1. Header (Cyber Sim Hub)
        header_container = QWidget()
        header_container.setStyleSheet("background-color: #0d1117; border-bottom: 1px solid #30363d;")
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(20, 25, 20, 25)
        
        title = QLabel("CYBER SIM")
        title.setProperty("class", "h1")
        title.setStyleSheet("font-size: 20px; letter-spacing: 2px; color: #58a6ff;")
        
        subtitle = QLabel("LEARNING HUB")
        subtitle.setStyleSheet("font-size: 10px; color: #8b949e; font-weight: bold; letter-spacing: 1px;")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addWidget(header_container)

        # 2. Navigation
        self.buttons = {}
        
        # Categories
        self.add_category_header("INJECTION ATTACKS", layout)
        self.add_nav_button("SQL Injection", "sql_injection", layout)
        self.add_nav_button("Cross-Site Scripting (XSS)", "xss", layout)
        
        self.add_category_header("BROKEN AUTHENTICATION", layout)
        self.add_nav_button("Brute Force", "brute_force", layout)
        
        self.add_category_header("SOCIAL ENGINEERING", layout)
        self.add_nav_button("Phishing", "phishing", layout)
        
        self.add_category_header("NETWORK ATTACKS", layout)
        self.add_nav_button("DoS / DDoS", "dos", layout)
        self.add_nav_button("Man-in-the-Middle", "mitm", layout)

        # Spacer
        vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(vertical_spacer)

        # 3. User Progress / Footer
        footer = QWidget()
        footer.setStyleSheet("background-color: #161b22; border-top: 1px solid #30363d;")
        footer_layout = QVBoxLayout(footer)
        footer_layout.setContentsMargins(20, 15, 20, 15)
        
        user_lbl = QLabel("USER: Student")
        user_lbl.setStyleSheet("font-weight: bold; color: #c9d1d9;")
        footer_layout.addWidget(user_lbl)
        
        prog_lbl = QLabel("Module Progress: 0/6")
        prog_lbl.setStyleSheet("color: #8b949e; font-size: 11px;")
        footer_layout.addWidget(prog_lbl)
        
        # Simple progress bar
        from PySide6.QtWidgets import QProgressBar, QHBoxLayout
        p_bar = QProgressBar()
        p_bar.setRange(0, 6)
        p_bar.setValue(0)
        p_bar.setTextVisible(False)
        p_bar.setFixedHeight(4)
        p_bar.setStyleSheet("background: #30363d; border: none; border-radius: 2px; QProgressBar::chunk { background: #238636; }")
        footer_layout.addWidget(p_bar)
        
        # Theme Toggle
        toggle_layout = QHBoxLayout()
        toggle_layout.setContentsMargins(0, 10, 0, 0)
        
        self.btn_theme = QPushButton("Light Mode")
        self.btn_theme.setCursor(Qt.PointingHandCursor)
        self.btn_theme.setStyleSheet("background: #21262d; color: #c9d1d9; border: 1px solid #30363d; font-size: 10px; padding: 4px;")
        self.btn_theme.clicked.connect(self.on_toggle_theme)
        
        toggle_layout.addStretch()
        toggle_layout.addWidget(self.btn_theme)
        footer_layout.addLayout(toggle_layout)
        
        layout.addWidget(footer)
        
    def on_toggle_theme(self):
        # We will connect this in MainWindow, but emit signal or just let MainWindow access it
        pass # Signal would be better, but direct connection in Main is fine for now


    def add_category_header(self, text, layout):
        lbl = QLabel(text)
        lbl.setProperty("class", "category_header")
        layout.addWidget(lbl)

    def add_nav_button(self, label, view_name, layout):
        btn = QPushButton(label)
        btn.setCheckable(True)
        btn.setAutoExclusive(True)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setProperty("class", "nav_btn") # CSS Class
        btn.clicked.connect(lambda: self.on_button_clicked(view_name))
        layout.addWidget(btn)
        self.buttons[view_name] = btn



    def on_button_clicked(self, view_name):
        self.attack_selected.emit(view_name)
