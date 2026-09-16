import sys
import argparse
from src.agent1_rules import run_agent1
from src.agent2_sync import run_agent2

def main():
    parser = argparse.ArgumentParser(description="Uruchamia agentów zarządzających Księgozbiorem.")
    parser.add_argument('--agent1', action='store_true', help="Uruchom tylko Agenta 1 (Zasady)")
    parser.add_argument('--agent2', action='store_true', help="Uruchom tylko Agenta 2 (Monitoring)")
    args = parser.parse_args()

    if args.agent1:
        run_agent1()
    elif args.agent2:
        run_agent2()
    else:
        print("================================")
        run_agent1()
        print("================================")
        run_agent2()
        print("================================")

if __name__ == "__main__":
    main()
