from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QTextBrowser, QPushButton, QSplitter
from PySide6.QtCore import Qt
from ui.attacks.base_attack_view import BaseAttackView

class PhishingView(BaseAttackView):
    def __init__(self):
        super().__init__("Phishing Attack Simulation", 
                         "Phishing involves sending fraudulent communications that appear to come from a reputable source.")
        
        self.emails = [
            {
                "subject": "Urgent: Verify your Bank Account",
                "sender": "security@bank-of-america-verify.com",
                "body": "<h1>Account Locked</h1><p>Dear Customer,</p><p>We detected unusual activity. Please click <a href='http://hacker-site.com/login'>here</a> to verify your account.</p>",
                "analysis": "SENDER: 'bank-of-america-verify.com' is NOT the official 'bankofamerica.com'.\nLINK: Hovering shows 'hacker-site.com'."
            },
            {
                "subject": "You won a price!",
                "sender": "winner@lottery-free.net",
                "body": "<h1>CONGRATULATIONS!</h1><p>Click <a href='http://malware-download.exe'>Claim Scale</a> to get your $1000000!</p>",
                "analysis": "GRAMMAR: 'price' instead of 'prize'.\nLINK: Points to an .exe file (Malware)."
            },
             {
                "subject": "Office 365 Password Expiry",
                "sender": "admin@microsofft.com",
                "body": "<p>Your password expires today. <a href='http://login-microsoft.com.cn'>Reset Now</a></p>",
                "analysis": "SPELLING: 'microsofft' has two 'f's.\nDOMAIN: .cn TLD for a US company login is suspicious."
            }
        ]
        
        # 1. Overview
        self.add_overview_section(
            "What is this attack?",
            "A social engineering attack often used to steal user data, including login credentials. It occurs when an attacker masquerades as a trusted entity."
        )
        self.add_overview_section(
            "How it works",
            "Attackers send fraudulent communications (usually email) that appear to come from a reputable source. The goal is to trick the recipient into clicking a malicious link or downloading an attachment."
        )
        self.add_overview_section(
            "Impact (Risk: HIGH)",
            "• <b>Credentials Theft</b>: Users unknowingly hand over passwords.<br>"
            "• <b>Malware Infection</b>: Links may download ransomware or remote access tools (RATs)."
        )
        
        # 2. Sim
        self.setup_simulation_ui()
        
        # 3. Defense
        self.add_defense_section(
            "Sender Verification",
            "<p>Always check the 'From' address carefully. Look for typos (e.g., <i>microsofft.com</i>) or slightly altered domains.</p>"
        )
        self.add_defense_section(
            "Link Inspection",
            "<p>Hover over links without clicking to see the actual URL destination in the status bar.</p>"
        )
        
        # 4. Learn
        self.add_learn_section(
            "Real-World Scenario",
            "<b>RSA Security Breach (2011)</b>: Started with a phishing email containing an Excel attachment titled '2011 Recruitment Plan.xls'."
        )
        self.add_learn_section(
            "Blue Team Detection",
            "• Analyze email headers for spoofing (DKIM/SPF failures).<br>"
            "• Monitor internet traffic for clicks on known malicious domains."
        )

    def setup_simulation_ui(self):
        splitter = QSplitter(Qt.Horizontal)
        
        # Email List
        self.email_list = QListWidget()
        self.email_list.addItems([e["subject"] for e in self.emails])
        self.email_list.currentRowChanged.connect(self.display_email)
        
        list_container = QWidget()
        list_layout = QVBoxLayout(list_container)
        list_layout.addWidget(QLabel("Inbox"))
        list_layout.addWidget(self.email_list)
        splitter.addWidget(list_container)
        
        # Email Viewer
        viewer_container = QWidget()
        viewer_layout = QVBoxLayout(viewer_container)
        viewer_layout.addWidget(QLabel("Email Content"))
        
        self.header_label = QLabel("From: ...")
        self.header_label.setStyleSheet("font-weight: bold; color: #aaa;")
        viewer_layout.addWidget(self.header_label)
        
        self.body_browser = QTextBrowser()
        self.body_browser.setStyleSheet("background-color: white; color: black; padding: 10px;")
        self.body_browser.highlighted.connect(self.on_hover_link)
        viewer_layout.addWidget(self.body_browser)

        
        self.btn_analyze = QPushButton("Analyze Security Headers")
        self.btn_analyze.clicked.connect(self.analyze_current)
        viewer_layout.addWidget(self.btn_analyze)
        
        splitter.addWidget(viewer_container)
        splitter.setSizes([200, 600])
        
        # Wrap in generic display
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(splitter)
        self.add_simulation_widget(container)
        
        # Status Bar for Link Hover
        self.status_label = QLabel("Hover over a link to inspect it...")
        self.status_label.setStyleSheet("color: #00ff00; font-family: monospace; padding: 5px; background: #222;")
        layout.addWidget(self.status_label)

    def display_email(self, index):
        if index < 0: return
        data = self.emails[index]
        self.header_label.setText(f"From: {data['sender']}")
        self.body_browser.setHtml(data["body"])
        self.log(f"[VIEW] Opened email: {data['subject']}")
        self.status_label.setText("Hover over a link to inspect it...")

    def on_hover_link(self, url):
        if url:
            self.status_label.setText(f"TARGET URL: {url}")
            self.log(f"[INSPECT] Hovered Link Target: {url}")
        else:
            self.status_label.setText("Hover over a link to inspect it...")

    def analyze_current(self):
        idx = self.email_list.currentRow()
        if idx >= 0:
            analysis = self.emails[idx]["analysis"]
            self.log(f"[ANALYSIS] {analysis}")
