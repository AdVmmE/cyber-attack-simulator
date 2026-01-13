from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel, QStackedWidget
from PySide6.QtCore import Qt
from ui.sidebar import Sidebar

# Attacks
from ui.attacks.sql_injection import SQLInjectionView
from ui.attacks.xss import XSSView
from ui.attacks.brute_force import BruteForceView
from ui.attacks.phishing import PhishingView
from ui.attacks.dos import DoSView
from ui.attacks.mitm import MITMView

from ui.styles_cyber import CYBER_STYLESHEET

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Cyber Security Attack Simulator v2.0")
        self.resize(1280, 850)
        
        # Apply Global Cyber Theme
        self.setStyleSheet(CYBER_STYLESHEET)
        
        # Central Widget & Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # 1. Left Sidebar
        self.sidebar = Sidebar()
        self.sidebar.attack_selected.connect(self.switch_view)
        self.sidebar.btn_theme.clicked.connect(self.toggle_theme) # Connect toggle
        
        # 2. Center Panel (Simulations - Full Width)
        self.center_panel = QStackedWidget()
        
        # 0. Placeholder
        self.placeholder_center = QLabel()
        self.placeholder_center.setText("INITIALIZING CYBER RANGE...\nSELECT A MODULE TO BEGIN\n\n[ Built by Advxm ]")
        self.placeholder_center.setAlignment(Qt.AlignCenter)
        self.placeholder_center.setStyleSheet("font-size: 18px; color: #30363d; font-weight: 800; letter-spacing: 2px;")
        self.center_panel.addWidget(self.placeholder_center)
        
        self.is_dark = True

        # 1. SQL Injection View
        self.sql_view = SQLInjectionView()
        self.center_panel.addWidget(self.sql_view)
        
        # 2. XSS View
        self.xss_view = XSSView()
        self.center_panel.addWidget(self.xss_view)
        
        # 3. Brute Force View
        self.brute_force_view = BruteForceView()
        self.center_panel.addWidget(self.brute_force_view)
        
        # 4. Phishing View
        self.phishing_view = PhishingView()
        self.center_panel.addWidget(self.phishing_view)
        
        # 5. DoS View
        self.dos_view = DoSView()
        self.center_panel.addWidget(self.dos_view)
        
        # 6. MITM View
        self.mitm_view = MITMView()
        self.center_panel.addWidget(self.mitm_view)
        
        # Add to Main Layout (Sidebar + Center)
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.center_panel, 1) # Stretch factor 1

    def switch_view(self, view_name):
        # Maps view names to widgets
        widgets = {
            "sql_injection": self.sql_view,
            "xss": self.xss_view,
            "brute_force": self.brute_force_view,
            "phishing": self.phishing_view,
            "dos": self.dos_view,
            "mitm": self.mitm_view
        }
        
        if view_name in widgets:
            self.center_panel.setCurrentWidget(widgets[view_name])
        else:
            self.center_panel.setCurrentWidget(self.placeholder_center)

    def toggle_theme(self):
        from ui.styles_cyber import CYBER_STYLESHEET, LIGHT_STYLESHEET
        if self.is_dark:
            self.setStyleSheet(LIGHT_STYLESHEET)
            self.sidebar.btn_theme.setText("Dark Mode")
            self.is_dark = False
        else:
            self.setStyleSheet(CYBER_STYLESHEET)
            self.sidebar.btn_theme.setText("Light Mode")
            self.is_dark = True







