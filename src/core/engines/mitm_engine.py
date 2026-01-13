from core.attack_base import AttackEngine

class MITMEngine(AttackEngine):
    def __init__(self):
        self.intercept_enabled = False
        self.encryption_enabled = False
        self.current_message = None
        
    def reset(self):
        self.intercept_enabled = False
        self.encryption_enabled = False
        self.current_message = None

    def run_step(self):
        pass

    def send_message(self, message):
        """Alice sends a message."""
        if self.encryption_enabled:
            # Simple simulation of encryption
            encrypted = "".join([chr(ord(c) + 1) for c in message]) # Caesar cipher +1
            transit_message = f"[ENCRYPTED] {encrypted}"
        else:
            transit_message = message
            
        if self.intercept_enabled:
            self.current_message = transit_message
            return {"status": "INTERCEPTED", "payload": transit_message}
        else:
            # Goes straight to Bob
            return {"status": "DELIVERED", "payload": transit_message}

    def forward_message(self, modified_message):
        """Eve forwards the message to Bob."""
        # Does Eve know it's encrypted? Yes, she sees the payload.
        # If encrypted, she might forward garbage or modified garbage.
        return {"status": "DELIVERED", "payload": modified_message}
