import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from core.engines.sql_engine import SQLEngine

def test_sql_injection():
    engine = SQLEngine()
    
    print("Testing Secure Login (Should Fail with bad pass)...")
    res = engine.simulate_login("admin", "wrongpass", secure=True)
    print(f"Result: {res['success']} (Expected: False)")
    
    print("\nTesting Secure Login (Should Success with correct pass)...")
    res = engine.simulate_login("admin", "admin123", secure=True)
    print(f"Result: {res['success']} (Expected: True)")
    
    print("\nTesting Vulnerable Login with Injection Payload...")
    # Payload: Close quote, OR true, Comment out the rest
    payload = "' OR '1'='1' --"
    res = engine.simulate_login(payload, "whatever", secure=False)
    print(f"Query: {res['query']}")
    print(f"Result: {res['success']} (Expected: True due to injection)")
    if res['success']:
        print(f"Logged in as: {res['result']}")


if __name__ == "__main__":
    test_sql_injection()
