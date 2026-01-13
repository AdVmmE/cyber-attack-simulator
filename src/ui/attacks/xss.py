from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLineEdit, QPushButton, QLabel, QCheckBox, QHBoxLayout, QListWidget, QMessageBox
from PySide6.QtCore import Qt
import html
from database.db_manager import DBManager
from ui.attacks.base_attack_view import BaseAttackView

class XSSView(BaseAttackView):
    def __init__(self):
        super().__init__("Cross-Site Scripting (XSS)", 
                         "XSS allows attackers to inject malicious scripts into web pages viewed by other users.")
        
        self.db = DBManager()
        
        # 1. Overview
        self.add_overview_section(
            "What is this attack?",
            "XSS occurs when an application includes untrusted data in a web page without proper validation or escaping, allowing execution of malicious scripts in the victim’s browser."
        )
        self.add_overview_section(
            "How it works",
            "An attacker injects JavaScript into input fields. When other users view that data, their browser executes the script, believing it came from the trusted website."
        )
        self.add_overview_section(
            "Impact (Risk: HIGH)",
            "• <b>Session Hijacking</b>: Stealing cookies to take over accounts.<br>"
            "• <b>Malicious Redirection</b>: Sending users to phishing sites.<br>"
            "• <b>Defacement</b>: Altering the appearance of the website."
        )
        
        # 2. Simulation (Nested Tabs)
        self.add_simulation_widget(self.setup_tabs())
        
        # 3. Defense
        self.add_defense_section(
            "Output Encoding",
            "<p>Convert special characters to HTML entities (e.g., <b>&lt;</b> becomes <b>&amp;lt;</b>) before rendering.</p>"
        )
        self.add_defense_section(
            "Content Security Policy (CSP)",
            "<p>A HTTP header that restricts the sources from which scripts can be loaded.</p>"
        )
        
        # 4. Learn More
        self.add_learn_section(
            "Real-World Scenario",
            "<b>Samy Worm (MySpace)</b>: The fastest spreading virus of all time (at the time), adding 1M friends to Samy's profile via XSS."
        )
        self.add_learn_section(
            "Blue Team Detection",
            "• Monitor for script tags (<span style='color:#79c0ff'>&lt;script&gt;, &lt;iframe&gt;, javascript:</span>) in logs.<br>"
            "• Review CSP violation reports."
        )

    def setup_tabs(self):
        tabs = QTabWidget()
        tabs.addTab(self.create_reflected_tab(), "Reflected XSS")
        tabs.addTab(self.create_stored_tab(), "Stored XSS")
        return tabs

    def create_reflected_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Search Bar Simulation
        layout.addWidget(QLabel("Simulated Search Page:"))
        
        input_layout = QHBoxLayout()
        self.reflected_input = QLineEdit()
        self.reflected_input.setPlaceholderText("Search...")
        self.reflected_input.setText("<script>alert('Reflected XSS')</script>")
        self.btn_reflected = QPushButton("Search")
        self.btn_reflected.clicked.connect(self.execute_reflected)
        
        input_layout.addWidget(self.reflected_input)
        input_layout.addWidget(self.btn_reflected)
        layout.addLayout(input_layout)
        
        self.check_secure_reflected = QCheckBox("Enable Sanitization (Secure)")
        layout.addWidget(self.check_secure_reflected)
        
        # Result Area
        layout.addWidget(QLabel("Results:"))
        self.reflected_result_label = QLabel()
        self.reflected_result_label.setStyleSheet("border: 1px solid #444; padding: 10px; background: #222;")
        self.reflected_result_label.setWordWrap(True)
        layout.addWidget(self.reflected_result_label)
        
        layout.addStretch()
        return widget

    def execute_reflected(self):
        user_input = self.reflected_input.text()
        secure = self.check_secure_reflected.isChecked()
        
        self.log(f"[REFLECTED] User searched for: {user_input}")
        
        if secure:
            # Secure: Escape HTML
            sanitized = html.escape(user_input)
            self.reflected_result_label.setTextFormat(Qt.PlainText) # Double safety
            self.reflected_result_label.setText(f"You searched for: {sanitized}")
            self.log(f"[SECURE] Input escaped: {sanitized}")
        else:
            # Vulnerable: Render as HTML (RichText)
            # Note: PySide6 QLabel RichText supports a subset of HTML. <script> won't execute JS, 
            # but we can simulate the "style" or "formatting" injection or simply Detect the tag.
            
            if "<script>" in user_input:
                self.log("[VULNERABLE] <script> tag detected! In a real browser, this would execute JS.")
                QMessageBox.warning(self, "XSS Alert", "Simulated XSS Executed!\n\n<script>alert('XSS')</script>")
            
            self.reflected_result_label.setTextFormat(Qt.RichText)
            self.reflected_result_label.setText(f"You searched for: {user_input}")

    def create_stored_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        layout.addWidget(QLabel("Comments Section:"))
        
        # Comment Input
        self.comment_input = QLineEdit()
        self.comment_input.setPlaceholderText("Leave a comment...")
        self.comment_input.setText("Nice post! <b style='color:red; font-size:20px'>HACKED</b>")
        self.btn_post = QPushButton("Post Comment")
        self.btn_post.clicked.connect(self.post_comment)
        
        layout.addWidget(self.comment_input)
        layout.addWidget(self.btn_post)
        
        self.check_secure_stored = QCheckBox("Enable Output Encoding (Secure)")
        self.check_secure_stored.toggled.connect(self.load_comments) # Reload when mode changes
        layout.addWidget(self.check_secure_stored)
        
        # Comments Display
        self.comments_list = QListWidget()
        layout.addWidget(self.comments_list)
        
        self.load_comments()
        
        return widget

    def post_comment(self):
        content = self.comment_input.text()
        # Save to DB (Always save raw, usually sanitization happens on input or output. We'll do output for this demo)
        self.db.execute_query("INSERT INTO comments (user_id, content) VALUES (?, ?)", (1, content))
        self.log(f"[STORED] Comment saved to database: {content}")
        self.load_comments()

    def load_comments(self):
        self.comments_list.clear()
        results = self.db.execute_query("SELECT content FROM comments", fetch_all=True)
        
        secure = self.check_secure_stored.isChecked()
        
        if results:
            for row in results:
                content = row[0]
                
                # Manual simulation of "Rendering" in a ListWidget Item
                # QListWidget items are text by default, but we can simulate the visual effect
                # or trigger a popup if script tags are found.
                
                if not secure:
                    if "<script>" in content:
                        self.log(f"[VULNERABLE] Loading comment with script: {content}")
                        QMessageBox.warning(self, "Stored XSS", f"Stored XSS Executed from DB!\n\n{content}")
                    elif "style=" in content or "<b>" in content:
                         self.log(f"[VULNERABLE] Rendering HTML styles: {content}")
                
                # In the list, we show the string. 
                # To simulate "Safe" vs "Unsafe" visual in QListWidget is hard without custom delegates.
                # simpler: Just logging the 'Execution' event is enough for simulation.
                
                display_text = content
                if secure:
                     display_text = f"[SAFE] {html.escape(content)}"
                
                self.comments_list.addItem(display_text)
