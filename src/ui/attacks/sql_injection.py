from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QCheckBox, QLabel, QHBoxLayout
from ui.attacks.base_attack_view import BaseAttackView
from core.engines.sql_engine import SQLEngine

class SQLInjectionView(BaseAttackView):
    def __init__(self):
        super().__init__("SQL Injection (SQLi)", 
                         "This simulation demonstrates a classic 'Login Bypass' attack.")
        
        self.engine = SQLEngine()
        
        # 1. Overview
        self.add_overview_section(
            "What is this attack?",
            "SQL Injection (SQLi) is a code injection technique where an attacker executes malicious SQL statements that control a web application's database server."
        )
        self.add_overview_section(
            "How it works",
            "Web applications often use user input (like a username) directly in database queries without proper cleaning. An attacker inputs crafted SQL code (e.g., <span style='font-family:monospace; color:#ff7b72;'>' OR '1'='1</span>) which the database interprets as a valid command rather than text."
        )
        self.add_overview_section(
            "Impact (Risk: HIGH)",
            "• <b>Data Compromise</b>: Access to sensitive user data (passwords, PII).<br>"
            "• <b>Authentication Bypass</b>: Logging in as Admin without a password.<br>"
            "• <b>Loss of Integrity</b>: Modifying or deleting database records."
        )
        
        # 2. Simulation (The Lab)
        self.setup_simulation_ui()

        # 3. Defense
        self.add_defense_section(
            "Prepared Statements (Parameterized Queries)",
            "<p>The most effective defense. It forces the database to treat user input as data, not executable code.</p>"
            "<pre style='background:#0d1117; color:#79c0ff; padding:10px;'>cursor.execute('SELECT * FROM users WHERE user = ?', (username,))</pre>"
        )
        self.add_defense_section(
            "Input Validation",
            "In 2011, LulzSec used SQL Injection to compromise Sony Pictures, stealing data of 1M+ accounts."
        )
        self.add_learn_section(
            "Resources",
            "• <a href='https://owasp.org/www-community/attacks/SQL_Injection' style='color:#58a6ff;'>OWASP SQL Injection</a><br>"
            "• <a href='https://portswigger.net/web-security/sql-injection' style='color:#58a6ff;'>PortSwigger SQLi Guide</a>"
        )

    def setup_simulation_ui(self):
        # Form Layout for Inputs
        form_layout = QFormLayout()
        
        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Enter username")
        self.input_username.setText("admin") # Default
        
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Enter password")
        self.input_password.setEchoMode(QLineEdit.Password)
        
        self.check_secure = QCheckBox("Enable Secure Mode (Parameterized Queries)")
        self.check_secure.setStyleSheet("color: #00ff00;")
        
        form_layout.addRow("Username:", self.input_username)
        form_layout.addRow("Password:", self.input_password)
        form_layout.addRow("", self.check_secure)
        
        # Action Buttons
        btn_layout = QHBoxLayout()
        self.btn_login = QPushButton("Login")
        self.btn_login.setStyleSheet("background-color: #007acc; color: white; padding: 5px 15px; font-weight: bold;")
        self.btn_login.clicked.connect(self.execute_login)
        
        self.btn_inject = QPushButton("Auto-Fill Attack Payload")
        self.btn_inject.setStyleSheet("background-color: #d62828; color: white; padding: 5px 15px;")
        self.btn_inject.clicked.connect(self.autofill_attack)
        
        btn_layout.addWidget(self.btn_login)
        btn_layout.addWidget(self.btn_inject)
        
        # Add widget to the base class container
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.addLayout(form_layout)
        container_layout.addLayout(btn_layout)
        
        self.add_simulation_widget(container)

    def autofill_attack(self):
        # Classic login bypass payload with comment
        self.input_username.setText("' OR '1'='1' --")
        self.input_password.setText("anything")
        self.log("[INFO] Payload inserted: ' OR '1'='1' -- \nThis closes the string, adds a TRUE condition, and comments out the password check.")


    def execute_login(self):
        username = self.input_username.text()
        password = self.input_password.text()
        is_secure = self.check_secure.isChecked()
        
        self.log(f"\n[ACTION] Attempting login... (Secure Mode: {is_secure})")
        
        response = self.engine.simulate_login(username, password, secure=is_secure)
        
        self.log(f"[DB] Constructed Query: {response['query']}")
        
        if response['error']:
            self.log(f"[ERROR] Database Error: {response['error']}")
        else:
            if response['success']:
                user = response['result']
                self.log(f"[SUCCESS] Login Successful! Logged in as: {user[1]} (Role: {user[3]})")
                self.log("[EXPLANATION] The query returned a result, so the application accepted the login.")
            else:
                self.log("[FAILED] Login Failed. Invalid credentials or query returned no results.")
                
        if not is_secure and "' OR '1'='1" in username:
             self.log("[ANALYSIS] Notice how the payload closed the quote and added OR '1'='1'. This makes the WHERE clause always TRUE.")

