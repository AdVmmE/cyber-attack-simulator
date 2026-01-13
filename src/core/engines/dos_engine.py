from core.attack_base import AttackEngine

class DoSEngine(AttackEngine):
    def __init__(self):
        self.request_count = 0
        self.server_health = 100
        self.max_requests_per_sec = 1000 # Server capacity
        self.current_rps = 0
        self.rate_limit_enabled = False
        self.rate_limit_cap = 200

    def reset(self):
        self.request_count = 0
        self.server_health = 100
        self.current_rps = 0

    def run_step(self):
        pass
    
    def update_simulation(self, attacker_nodes):
        # Calculate RPS (Requests per second) based on nodes
        # Each node sends ~50 requests/sec simulated
        raw_rps = attacker_nodes * 50
        
        accepted_rps = raw_rps
        dropped_rps = 0
        
        if self.rate_limit_enabled:
            if raw_rps > self.rate_limit_cap:
                accepted_rps = self.rate_limit_cap
                dropped_rps = raw_rps - self.rate_limit_cap
        
        self.current_rps = accepted_rps
        
        # Calculate Health Impact
        # Health decreases if accepted_rps > threshold (e.g. 500)
        # Recovers if low
        
        overload = max(0, accepted_rps - 500)
        damage = overload / 10 # Scale down
        
        self.server_health -= damage
        if accepted_rps < 400:
             self.server_health += 5 # Recover
             
        self.server_health = max(0, min(100, self.server_health))
        
        return {
            "health": self.server_health,
            "rps": raw_rps,
            "accepted": accepted_rps,
            "dropped": dropped_rps
        }
