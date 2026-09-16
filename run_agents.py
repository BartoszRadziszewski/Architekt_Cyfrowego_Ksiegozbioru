import sys
import src.config as config
from src.agent1_rules import run_agent1
from src.agent2_sync import run_agent2

def main():
    print("================================", flush=True)
    try:
        run_agent1()
    except Exception as e:
        print(f"Błąd podczas pracy Agenta 1: {e}", flush=True)
        
    print("================================", flush=True)
    try:
        run_agent2()
    except Exception as e:
        print(f"Błąd podczas pracy Agenta 2: {e}", flush=True)
        
    print("================================", flush=True)

if __name__ == "__main__":
    main()
