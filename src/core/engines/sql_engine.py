from core.attack_base import AttackEngine
from database.db_manager import DBManager

class SQLEngine(AttackEngine):
    def __init__(self):
        self.db = DBManager()

    def reset(self):
        # Could reset DB data if needed
        pass

    def run_step(self):
        pass

    def simulate_login(self, username, password, secure=False):
        """
        Simulates a login attempt.
        secure=False -> Vulnerable to SQLi (String concatenation)
        secure=True -> Secure (Parameterized Query)
        """
        
        # 1. Construct Query
        if not secure:
            # VULNERABLE: Direct string concatenation
            query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
            print(f"Executing VULNERABLE Query: {query}")
        else:
            # SECURE: Parameterized
            query = "SELECT * FROM users WHERE username = ? AND password = ?"
            print(f"Executing SECURE Query: {query} with params ({username}, {password})")

        # 2. Execute
        try:
            if not secure:
                # Use the unsafe method in DBManager
                result = self.db.execute_unsafe_query(query)
            else:
                # Use the safe method
                result = self.db.execute_query(query, (username, password), fetch_all=True)
            
            # 3. Analyze Result
            success = False
            user_data = None
            
            if result and isinstance(result, list) and len(result) > 0:
                success = True
                user_data = result[0] # Just take the first user found (Simulates bypass logging in as first match)
                
            return {
                "success": success,
                "query": query,
                "result": user_data,
                "raw_result": result,
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "query": query,
                "result": None,
                "raw_result": None,
                "error": str(e)
            }
