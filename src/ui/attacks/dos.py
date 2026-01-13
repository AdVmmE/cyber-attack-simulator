from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QProgressBar, QCheckBox, QGroupBox
from PySide6.QtCore import Qt, QTimer
from ui.attacks.base_attack_view import BaseAttackView
from core.engines.dos_engine import DoSEngine

class DoSView(BaseAttackView):
    def __init__(self):
        super().__init__("DoS / DDoS Attack", 
                         "Denial of Service (DoS) aims to shut down a machine or network, making it inaccessible to its intended users.")
        
        self.engine = DoSEngine()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(500) # Update every 500ms
        
        # 1. Overview
        self.add_overview_section(
            "What is this attack?",
            "An attack meant to shut down a machine or network, making it inaccessible to its intended users by flooding it with traffic."
        )
        self.add_overview_section(
            "How it works",
            "DoS floods the target with traffic or sends information that triggers a crash. In DDoS (Distributed DoS), the traffic comes from many compromised devices (botnet)."
        )
        self.add_overview_section(
            "Impact (Risk: MEDIUM)",
            "• <b>Service Downtime</b>: Websites or APIs become unreachable.<br>"
            "• <b>Financial Loss</b>: Business operations are halted.<br>"
            "• <b>Distraction</b>: Often used to distract security teams from other intrusions."
        )
        
        # 2. Sim
        self.setup_simulation_ui()
        
        # 3. Defense
        self.add_defense_section(
            "Rate Limiting",
            "<p>Restrict the number of requests a user/IP can make in a given timeframe (e.g., 60 req/min).</p>"
        )
        self.add_defense_section(
            "WAF / Traffic Analysis",
            "<p>Identify and filter malicious traffic patterns (e.g., bot signatures) and use Content Delivery Networks (CDNs) to absorb load.</p>"
        )
        
        # 4. Learn
        self.add_learn_section(
            "Real-World Scenario",
            "<b>Mirai Botnet (2016)</b>: Took down Dyn DNS, affecting major sites like Twitter and Netflix, by using infected IoT devices."
        )
        self.add_learn_section(
            "Blue Team Detection",
            "• Sudden, unexplained spikes in network traffic.<br>"
            "• Slow server response times or HTTP 503 errors."
        )

    def setup_simulation_ui(self):
        layout = QVBoxLayout()
        
        # Controls
        control_group = QGroupBox("Botnet Control")
        control_layout = QVBoxLayout()
        
        control_layout.addWidget(QLabel("Number of Attacker Nodes (Bots):"))
        self.node_slider = QSlider(Qt.Horizontal)
        self.node_slider.setRange(0, 50) # 0 to 50 bots
        self.node_slider.setValue(0)
        self.node_slider.valueChanged.connect(self.on_slider_change)
        control_layout.addWidget(self.node_slider)
        
        self.lbl_nodes = QLabel("Active Bots: 0")
        control_layout.addWidget(self.lbl_nodes)
        
        self.check_ratelimit = QCheckBox("Enable WAF Rate Limiting (Prevention)")
        self.check_ratelimit.toggled.connect(self.toggle_prevention)
        control_layout.addWidget(self.check_ratelimit)
        
        control_group.setLayout(control_layout)
        layout.addWidget(control_group)

        # Dashboard
        dash_group = QGroupBox("Server Monitor")
        dash_layout = QVBoxLayout()
        
        # Health
        dash_layout.addWidget(QLabel("Server CPU/Memory Health:"))
        self.health_bar = QProgressBar()
        self.health_bar.setRange(0, 100)
        self.health_bar.setValue(100)
        self.health_bar.setStyleSheet("QProgressBar::chunk { background-color: #00ff00; }")
        dash_layout.addWidget(self.health_bar)
        
        # Traffic
        dash_layout.addWidget(QLabel("Incoming Traffic (Req/Sec):"))
        self.traffic_bar = QProgressBar()
        self.traffic_bar.setRange(0, 3000) # Max scale
        self.traffic_bar.setTextVisible(True)
        self.traffic_bar.setFormat("%v RPS")
        dash_layout.addWidget(self.traffic_bar)
        
        dash_group.setLayout(dash_layout)
        layout.addWidget(dash_group)
        
        self.add_simulation_widget(control_group)
        self.add_simulation_widget(dash_group) # Add roughly to layout
        
        # Add a status label
        self.status_lbl = QLabel("Server Status: ONLINE")
        self.status_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: green;")
        self.status_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_lbl)
        
        container = QWidget() # Wrapper if needed, but add_simulation_widget adds individually. 
        # Actually add_simulation_widget adds to self.simulation_layout.
        # I added widgets twice (wrapper layout vs individual). 
        # let's just use self.simulation_layout manually for the status label
        self.simulation_layout.addWidget(self.status_lbl)

    def on_slider_change(self, value):
        self.lbl_nodes.setText(f"Active Bots: {value}")
        if value > 0:
            self.log(f"[ATTACK] Botnet scaled to {value} nodes.")

    def toggle_prevention(self, checked):
        self.engine.rate_limit_enabled = checked
        self.log(f"[DEFENSE] Rate Limiting {'ENABLED' if checked else 'DISABLED'}")

    def update_stats(self):
        bots = self.node_slider.value()
        stats = self.engine.update_simulation(bots)
        
        # Update UI
        self.health_bar.setValue(int(stats['health']))
        self.traffic_bar.setValue(stats['rps'])
        
        # Styles
        if stats['health'] > 70:
            self.health_bar.setStyleSheet("QProgressBar::chunk { background-color: #00ff00; }") # Green
            self.status_lbl.setText("Server Status: ONLINE")
            self.status_lbl.setStyleSheet("color: green; font-weight: bold; font-size: 18px;")
        elif stats['health'] > 30:
            self.health_bar.setStyleSheet("QProgressBar::chunk { background-color: #ffff00; }") # Yellow
            self.status_lbl.setText("Server Status: DEGRADED")
            self.status_lbl.setStyleSheet("color: yellow; font-weight: bold; font-size: 18px;")
        else:
            self.health_bar.setStyleSheet("QProgressBar::chunk { background-color: #ff0000; }") # Red
            self.status_lbl.setText("Server Status: OFFLINE (DoS)")
            self.status_lbl.setStyleSheet("color: red; font-weight: bold; font-size: 18px;")

        if stats['dropped'] > 0:
            self.log(f"[FIREWALL] Dropped {stats['dropped']} requests/sec due to rate limiting.")
