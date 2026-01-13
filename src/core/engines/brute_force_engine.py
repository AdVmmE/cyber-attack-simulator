import time
from core.attack_base import AttackEngine
from database.db_manager import DBManager

class BruteForceEngine(AttackEngine):
    def __init__(self):
        self.db = DBManager()
        self.is_running = False
        self.target_user = "admin"
        self.lockout_enabled = False
        self.failed_attempts = 0
        self.lockout_threshold = 3
        self.locked_out = False

    def reset(self):
        self.is_running = False
        self.failed_attempts = 0
        self.locked_out = False

    def run_step(self):
        pass

    def set_target(self, username):

        self.target_user = username

    def set_lockout_policy(self, enabled):
        self.lockout_enabled = enabled
        self.reset() # Reset counts when policy changes

    def check_password(self, password):
        if self.locked_out:
            return {"success": False, "status": "LOCKED", "message": "Account is locked due to too many failed attempts."}

        # Check in DB
        # Secure login check (safe from SQLi, we just want to check creds)
        # In a real brute force, this is the "server response"
        
        # Simulate Network Delay (handled by UI timer typically, but we can sleep here if threaded)
        # For this sim, we return immediate result
        
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        user = self.db.execute_query(query, (self.target_user, password), fetch_one=True)
        
        if user:
            self.failed_attempts = 0
            return {"success": True, "status": "OK", "message": f"Login Success! Password found: {password}"}
        else:
            self.failed_attempts += 1
            if self.lockout_enabled and self.failed_attempts >= self.lockout_threshold:
                self.locked_out = True
                return {"success": False, "status": "LOCKED", "message": "Account Locked."}
            
            return {"success": False, "status": "FAIL", "message": "Invalid credentials."}
