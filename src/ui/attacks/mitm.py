from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QCheckBox, QGroupBox
from PySide6.QtCore import Qt
from ui.attacks.base_attack_view import BaseAttackView
from core.engines.mitm_engine import MITMEngine

class MITMView(BaseAttackView):
    def __init__(self):
        super().__init__("Man-in-the-Middle (MITM)", 
                         "An attacker (Eve) secretly intercepts and relays communication between two parties (Alice and Bob) who believe they are communicating directly.")
        
        self.engine = MITMEngine()
        
        # 1. Overview
        self.add_overview_section(
            "What is this attack?",
            "An attacker silently relays and possibly alters the communications between two parties who believe they are communicating directly."
        )
        self.add_overview_section(
            "How it works",
            "The attacker positions themselves logically between the client and server (often on public Wi-Fi). They capture data packets flowing in both directions."
        )
        self.add_overview_section(
            "Impact (Risk: HIGH)",
            "• <b>Confidentiality Loss</b>: Login credentials and session cookies are captured.<br>"
            "• <b>Integrity Loss</b>: Attackers can modify messages in transit (e.g., changing a bank transfer recipient)."
        )
        
        # 2. Sim
        self.setup_simulation_ui()
        
        # 3. Defense
        self.add_defense_section(
            "Encryption (HTTPS/TLS)",
            "<p>Encrypts the tunnel so even if intercepted, data is unreadable garbage to the attacker.</p>"
        )
        self.add_defense_section(
            "VPN (Virtual Private Network)",
            "<p>Wraps traffic in an encrypted tunnel, protecting it on untrusted local networks (like public cafes).</p>"
        )
        
        # 4. Learn
        self.add_learn_section(
            "Real-World Scenario",
            "<b>Superfish (Lenovo)</b>: Adware pre-installed on laptops injected a self-signed root certificate, allowing MITM attacks on HTTPS traffic."
        )
        self.add_learn_section(
            "Blue Team Detection",
            "• Network monitoring for ARP poisoning/spoofing.<br>"
            "• Unexpected changes in SSL certificates or 'Certificate Invalid' warnings."
        )

    def setup_simulation_ui(self):
        # 3 Columns: Alice, Eve, Bob
        layout = QHBoxLayout()
        
        # --- ALICE ---
        alice_group = QGroupBox("Adam (Sender)")
        alice_group.setStyleSheet("QGroupBox { border: 1px solid #00aa00; font-weight: bold; } QGroupBox::title { color: #00aa00; }")
        alice_layout = QVBoxLayout()
        
        self.alice_input = QTextEdit()
        self.alice_input.setPlaceholderText("Type a secret message...")
        self.alice_input.setMaximumHeight(100)
        alice_layout.addWidget(self.alice_input)
        
        self.btn_send = QPushButton("Send Message")
        self.btn_send.clicked.connect(self.send_from_alice)
        alice_layout.addWidget(self.btn_send)
        
        self.check_encrypt = QCheckBox("Enable Encryption (AES)")
        self.check_encrypt.toggled.connect(self.toggle_encryption)
        alice_layout.addWidget(self.check_encrypt)
        
        alice_layout.addStretch()
        alice_group.setLayout(alice_layout)
        layout.addWidget(alice_group)
        
        # --- EVE ---
        eve_group = QGroupBox("Eve (Attacker)")
        eve_group.setStyleSheet("QGroupBox { border: 1px solid #ff0000; font-weight: bold; } QGroupBox::title { color: #ff0000; }")
        eve_layout = QVBoxLayout()
        
        self.check_intercept = QCheckBox("Intercept Traffic")
        self.check_intercept.setStyleSheet("color: #ff5555; font-weight: bold;")
        self.check_intercept.toggled.connect(self.toggle_intercept)
        eve_layout.addWidget(self.check_intercept)
        
        eve_layout.addWidget(QLabel("Intercepted Data:"))
        self.eve_display = QTextEdit()
        self.eve_display.setPlaceholderText("Waiting for data...")
        self.eve_display.setMaximumHeight(100)
        eve_layout.addWidget(self.eve_display)
        
        self.btn_forward = QPushButton("Modify & Forward")
        self.btn_forward.setStyleSheet("background-color: #aa0000; color: white;")
        self.btn_forward.setEnabled(False)
        self.btn_forward.clicked.connect(self.forward_from_eve)
        eve_layout.addWidget(self.btn_forward)
        
        eve_layout.addStretch()
        eve_group.setLayout(eve_layout)
        layout.addWidget(eve_group)
        
        # --- BOB ---
        bob_group = QGroupBox("3ab3ali (Receiver)")
        bob_group.setStyleSheet("QGroupBox { border: 1px solid #0055aa; font-weight: bold; } QGroupBox::title { color: #0055aa; }")
        bob_layout = QVBoxLayout()
        
        bob_layout.addWidget(QLabel("Received Message:"))
        self.bob_display = QTextEdit()
        self.bob_display.setReadOnly(True)
        self.bob_display.setMaximumHeight(100)
        self.bob_display.setStyleSheet("background-color: #111; color: #00aaff;")
        bob_layout.addWidget(self.bob_display)
        
        bob_layout.addStretch()
        bob_group.setLayout(bob_layout)
        layout.addWidget(bob_group)
        
        # Wrap in container
        container = QWidget()
        container.setLayout(layout)
        self.add_simulation_widget(container)

    def toggle_encryption(self, checked):
        self.engine.encryption_enabled = checked
        self.log(f"[CONFIG] Encryption {'ENABLED' if checked else 'DISABLED'}")

    def toggle_intercept(self, checked):
        self.engine.intercept_enabled = checked
        self.log(f"[CONFIG] Interception {'ACTIVE' if checked else 'INACTIVE'}")

    def send_from_alice(self):
        msg = self.alice_input.toPlainText()
        if not msg:
            return
        
        self.log(f"[ALICE] Sending: '{msg}'")
        result = self.engine.send_message(msg)
        
        if result["status"] == "INTERCEPTED":
            self.eve_display.setText(result["payload"])
            self.btn_forward.setEnabled(True)
            self.log("[NETWORK] Targeted INTERCEPTED by Eve!")
            self.bob_display.clear() # Bob doesn't get it yet
        else:
            self.eve_display.clear()
            self.btn_forward.setEnabled(False)
            self.deliver_to_bob(result["payload"])

    def forward_from_eve(self):
        modified_msg = self.eve_display.toPlainText()
        self.log(f"[EVE] Forwarding (potential modification): '{modified_msg}'")
        
        # Send to bob
        result = self.engine.forward_message(modified_msg)
        self.deliver_to_bob(result["payload"])
        
        self.btn_forward.setEnabled(False) # Sent

    def deliver_to_bob(self, payload):
        # Decrypt check
        display_text = payload
        if self.engine.encryption_enabled:
            # Check if it starts with [ENCRYPTED]
            if payload.startswith("[ENCRYPTED] "):
                encrypted_text = payload.replace("[ENCRYPTED] ", "")
                try:
                    # Decrypt (Caesar -1)
                    decrypted = "".join([chr(ord(c) - 1) for c in encrypted_text])
                    display_text = f"{decrypted} (Decrypted successfully)"
                except:
                    display_text = f"{payload} (Decryption Failed)"
            else:
                 display_text = f"{payload} (Warning: Message was NOT encrypted!)"
        
        self.bob_display.setText(display_text)
        self.log(f"[BOB] Received: {display_text}")
