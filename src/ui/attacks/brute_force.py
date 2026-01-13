from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QProgressBar, QSlider, QGroupBox, QFormLayout
from PySide6.QtCore import Qt, QTimer
from ui.attacks.base_attack_view import BaseAttackView
from core.engines.brute_force_engine import BruteForceEngine

class BruteForceView(BaseAttackView):
    def __init__(self):
        super().__init__("Brute Force Attack", 
                         "A Brute Force attack involves guessing a password by trying every possible combination from a list.")
        
        self.engine = BruteForceEngine()
        self.timer = QTimer()
        self.timer.timeout.connect(self.attack_step)
        
        self.wordlist = ["123456", "password", "welcome", "qwerty", "admin", "admin123", "secret", "letmein"]
        self.current_index = 0
        
        # 1. Overview
        self.add_overview_section(
            "What is this attack?",
            "A trial-and-error method used to obtain information such as a user password or personal identification number (PIN)."
        )
        self.add_overview_section(
            "How it works",
            "Automated software is used to generate a large number of consecutive guesses as to the value of the desired data (e.g., cycling through a dictionary of passwords)."
        )
        self.add_overview_section(
            "Impact (Risk: MEDIUM)",
            "• <b>Unauthorized Access</b>: Gaining entry to user or admin accounts.<br>"
            "• <b>System Escalation</b>: attackers can pivot to other systems once logged in."
        )
        
        # 2. Simulation
        self.setup_simulation_ui()
        
        # 3. Defense
        self.add_defense_section(
            "Account Lockout",
            "<p>Disable account after N failed attempts (e.g., 3-5 failures). Prevents infinite guessing.</p>"
        )
        self.add_defense_section(
            "Multi-Factor Authentication (MFA)",
            "<p>Requires a second verification step (e.g., SMS, App), rendering password guessing useless.</p>"
        )
        
        # 4. Learn
        self.add_learn_section(
            "Real-World Scenario",
            "<b>iCloud Celebrity Leak (2014)</b>: Targeted brute force/phishing against iCloud accounts led to massive data exposure."
        )
        self.add_learn_section(
            "Blue Team Detection",
            "• High volume of failed login attempts from a single IP address.<br>"
            "• Logins occurring at unusual times or from unusual locations."
        )

    def setup_simulation_ui(self):
        layout = QVBoxLayout()
        
        # Controls
        control_group = QGroupBox("Attack Controls")
        control_layout = QFormLayout()
        
        self.target_input = QLineEdit("admin")
        self.target_input.setPlaceholderText("Target Username")
        
        self.check_lockout = QCheckBox("Enable Account Lockout Policy (Secure)")
        self.check_lockout.toggled.connect(self.toggle_lockout)
        
        control_layout.addRow("Target User:", self.target_input)
        control_layout.addRow("", self.check_lockout)
        
        control_group.setLayout(control_layout)
        layout.addWidget(control_group)
        
        # Speed Control
        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel("Attack Speed:"))
        self.slider_speed = QSlider(Qt.Horizontal)
        self.slider_speed.setRange(50, 1000)
        self.slider_speed.setValue(200)
        self.slider_speed.setInvertedAppearance(True) # Lower val = faster? No, wait. 
        # Standard: Left = Slower (High ms), Right = Faster (Low ms)
        # So Range: 1000 (Slow) -> 50 (Fast).
        # We need to invert logic or range.
        # Let's say Left 0 -> Right 100. calculate ms from that.
        
        speed_layout.addWidget(self.slider_speed)
        layout.addLayout(speed_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_start = QPushButton("Start Attack")
        self.btn_start.setStyleSheet("background-color: #d62828; color: white; padding: 10px; font-weight: bold;")
        self.btn_start.clicked.connect(self.toggle_attack)
        
        self.btn_reset = QPushButton("Reset")
        self.btn_reset.clicked.connect(self.reset_attack)
        
        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_reset)
        layout.addLayout(btn_layout)
        
        # Visualization
        self.current_pass_label = QLabel("Waiting...")
        self.current_pass_label.setAlignment(Qt.AlignCenter)
        self.current_pass_label.setStyleSheet("font-size: 20px; font-family: Monospace; font-weight: bold; color: #ff9900; margin: 20px; border: 1px dashed #555;")
        layout.addWidget(self.current_pass_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, len(self.wordlist))
        layout.addWidget(self.progress_bar)
        
        self.add_simulation_widget(QWidget()) # Trick to get QWidget container
        # Since I used add_simulation_widget which takes a widget, I should wrap my layout in one.
        container = QWidget()
        container.setLayout(layout)
        # Clear previous added (hacky but BaseAttackView is simple)
        # Better: BaseAttackView.add_sim_widget just adds to layout. 
        
        # Let's fix BaseAttack usage properly:
        # Pass the container to add_simulation_widget
        self.simulation_layout.addWidget(container)    # Direct access to layout works too if protected
        
        # Import QFormLayout locally or fix imports
        
    def toggle_lockout(self, checked):
        self.engine.set_lockout_policy(checked)
        self.log(f"[CONFIG] Lockout Policy Set: {checked}")

    def toggle_attack(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn_start.setText("Resume Attack")
            self.log("[INFO] Attack Paused.")
        else:
            self.engine.set_target(self.target_input.text())
            # interval logic: Logic flip. 
            # Slider 50 (Right/Small) -> Fast. Slider 1000 (Right/Big)?
            # I set setRange(50, 1000). Default 200.
            # If I want Right to be Fast, I should probably do: 
            # Slider Value = Interval (ms). Small = Fast.
            # So Left (50) is Super fast. Right (1000) is slow.
            # Okay let's stick to that but visually it might be confusing.
            # Usually Right is "More Speed". 
            # Whatever, let's just use the value directly as ms delay for now.
            
            interval = self.slider_speed.value()
            self.timer.start(interval)
            self.btn_start.setText("Pause Attack")
            self.log(f"[INFO] Attack Started/Resumed against user: {self.target_input.text()}")

    def attack_step(self):
        if self.current_index >= len(self.wordlist):
            self.timer.stop()
            self.log("[INFO] Wordlist exhausted. Password not found.")
            self.btn_start.setText("Start Attack")
            return

        guess = self.wordlist[self.current_index]
        self.current_pass_label.setText(guess)
        self.progress_bar.setValue(self.current_index + 1)
        
        result = self.engine.check_password(guess)
        
        if result['success']:
            self.timer.stop()
            self.current_pass_label.setText(f"FOUND: {guess}")
            self.current_pass_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #00ff00; border: 2px solid #00ff00; margin: 20px;")
            self.log(f"[SUCCESS] {result['message']}")
            self.btn_start.setText("Start Attack")
        else:
            if result['status'] == "LOCKED":
                self.timer.stop()
                self.current_pass_label.setText("LOCKED OUT")
                self.current_pass_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #ff0000; border: 2px solid #ff0000; margin: 20px;")
                self.log(f"[BLOCKED] {result['message']}")
                self.btn_start.setText("Start Attack")
            else:
                self.log(f"[FAIL] Tried: {guess} - Access Denied")
        
        self.current_index += 1

    def reset_attack(self):
        self.timer.stop()
        self.current_index = 0
        self.progress_bar.setValue(0)
        self.current_pass_label.setText("Waiting...")
        self.current_pass_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #ff9900; margin: 20px; border: 1px dashed #555;")
        self.engine.reset()
        self.btn_start.setText("Start Attack")
        self.log("[INFO] Attack Reset.")

from PySide6.QtWidgets import QFormLayout # Missing import fix
