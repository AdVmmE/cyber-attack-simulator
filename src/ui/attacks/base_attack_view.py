from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTabWidget, QTextBrowser, 
    QScrollArea, QFrame, QHBoxLayout, QTextEdit
)
from PySide6.QtCore import Qt

class BaseAttackView(QWidget):
    """
    Base class for all attack simulations (Cyber Sim 2.0).
    Now implements a 4-tab layout: Overview, Simulation, Defense, Learn More.
    """
    def __init__(self, title, description, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # 1. Header (Common Title)
        header = QFrame()
        header.setStyleSheet("background-color: #0d1117; border-bottom: 1px solid #30363d;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        title_lbl = QLabel(title.upper())
        title_lbl.setProperty("class", "h1")
        header_layout.addWidget(title_lbl)
        
        # Add Stretch to push title to left
        header_layout.addStretch()
        
        self.layout.addWidget(header)

        # 2. Main Tab Widget
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # --- Tab 1: Overview ---
        self.overview_tab = QWidget()
        overview_scroll = QScrollArea()
        overview_scroll.setWidgetResizable(True)
        overview_scroll.setWidget(self.overview_tab)
        
        self.overview_layout = QVBoxLayout(self.overview_tab)
        self.overview_layout.setAlignment(Qt.AlignTop)
        self.overview_layout.setContentsMargins(30, 30, 30, 30)
        self.overview_layout.setSpacing(20)
        
        # Description Card
        desc_lbl = QLabel("ATTACK OVERVIEW")
        desc_lbl.setProperty("class", "h2")
        self.overview_layout.addWidget(desc_lbl)
        
        self.desc_text = QLabel(description)
        self.desc_text.setWordWrap(True)
        self.desc_text.setStyleSheet("color: #8b949e; font-size: 15px; margin-bottom: 10px; line-height: 1.5;")
        self.overview_layout.addWidget(self.desc_text)
        
        self.tabs.addTab(overview_scroll, "OVERVIEW")

        # --- Tab 2: Simulation (The Lab) ---
        self.simulation_tab = QWidget()
        
        # We need a layout for the tab
        sim_tab_layout = QVBoxLayout(self.simulation_tab)
        sim_tab_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create Splitter
        from PySide6.QtWidgets import QSplitter
        self.splitter = QSplitter(Qt.Vertical)
        
        # Top: Simulation Content (Scrollable)
        self.sim_content_widget = QWidget()
        self.simulation_layout = QVBoxLayout(self.sim_content_widget) # Subclasses add here
        self.simulation_layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll Area for Sim Content
        sim_scroll = QScrollArea()
        sim_scroll.setWidgetResizable(True)
        sim_scroll.setWidget(self.sim_content_widget)
        
        self.splitter.addWidget(sim_scroll)
        
        # Bottom: Logs
        log_container = QWidget()
        log_layout = QVBoxLayout(log_container)
        log_layout.setContentsMargins(0, 0, 0, 0)
        log_layout.addWidget(QLabel("EVENT LOGS"))
        
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setPlaceholderText("Simulation Logs...")
        self.log_output.setStyleSheet("font-family: Consolas; border: 1px solid #30363d;")
        log_layout.addWidget(self.log_output)
        
        self.splitter.addWidget(log_container)
        
        # Set Splitter Ratios (70% Sim, 30% Logs)
        self.splitter.setSizes([500, 200])
        
        sim_tab_layout.addWidget(self.splitter)
        
        self.tabs.addTab(self.simulation_tab, "SIMULATION")

        # --- Tab 3: Defense (Blue Team) ---
        self.defense_tab = QWidget()
        defense_scroll = QScrollArea()
        defense_scroll.setWidgetResizable(True)
        defense_scroll.setWidget(self.defense_tab)
        
        self.defense_layout = QVBoxLayout(self.defense_tab)
        self.defense_layout.setAlignment(Qt.AlignTop)
        self.defense_layout.setContentsMargins(30, 30, 30, 30)
        
        self.tabs.addTab(defense_scroll, "DEFENSE")

        # --- Tab 4: Learn More ---
        self.learn_tab = QWidget()
        learn_scroll = QScrollArea()
        learn_scroll.setWidgetResizable(True)
        learn_scroll.setWidget(self.learn_tab)
        
        self.learn_layout = QVBoxLayout(self.learn_tab)
        self.learn_layout.setAlignment(Qt.AlignTop)
        self.learn_layout.setContentsMargins(30, 30, 30, 30)
        
        self.tabs.addTab(learn_scroll, "LEARN MORE")
        
        # Default content for empty tabs
        self.add_defense_section("Defense Strategies", "Content coming soon...")
        self.add_learn_section("Resources", "Content coming soon...")

    def log(self, message):
        self.log_output.append(message)
        # Scroll to bottom
        sb = self.log_output.verticalScrollBar()
        sb.setValue(sb.maximum())

    def clear_log(self):
        self.log_output.clear()

    def add_simulation_widget(self, widget):
        """Used by subclasses to add attack-specific UI"""
        self.simulation_layout.addWidget(widget)

    def add_overview_section(self, title, content):
        """Helper to add cards to Overview tab"""
        lbl = QLabel(title)
        lbl.setProperty("class", "h2")
        self.overview_layout.addWidget(lbl)
        
        txt = QLabel(content)
        txt.setWordWrap(True)
        txt.setTextInteractionFlags(Qt.TextSelectableByMouse)
        txt.setStyleSheet("""
            color: #c9d1d9; 
            background: #161b22; 
            padding: 15px; 
            border: 1px solid #30363d; 
            border-radius: 6px;
            margin-bottom: 20px;
        """)
        self.overview_layout.addWidget(txt)

    def add_defense_section(self, title, content):
        """Helper to add sections to Defense tab"""
        lbl = QLabel(title)
        lbl.setProperty("class", "h2")
        lbl.setStyleSheet("color: #7ee787;") # Green
        self.defense_layout.addWidget(lbl)
        
        txt = QLabel(content)
        txt.setWordWrap(True)
        txt.setStyleSheet("color: #c9d1d9; font-size: 14px; margin-bottom: 20px;")
        self.defense_layout.addWidget(txt)
        
    def add_learn_section(self, title, content):
        lbl = QLabel(title)
        lbl.setProperty("class", "h2")
        self.learn_layout.addWidget(lbl)
        
        txt = QLabel(content)
        txt.setWordWrap(True)
        txt.setStyleSheet("color: #8b949e; margin-bottom: 10px;")
        self.learn_layout.addWidget(txt)
