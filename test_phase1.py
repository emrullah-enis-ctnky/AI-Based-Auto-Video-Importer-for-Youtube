import os
import sys

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from utils.logger import logger
from utils.app_init import initialize_app

def test_phase1():
    print("--- Phase 1 Verification Start ---")
    
    # Test App Initialization (should fail if .env is missing, which is expected now)
    print("\n1. Testing App Initialization (Expecting failure due to missing .env):")
    init_success = initialize_app()
    
    # Test Manual Logging
    print("\n2. Testing Manual Logging:")
    logger.info("This is an INFO message (should see this in terminal and file)")
    logger.debug("This is a DEBUG message (should only see this in file)")
    logger.warning("This is a WARNING message")
    logger.success("This is a SUCCESS message")
    
    # Check if log file exists
    log_file = "logs/app.log"
    if os.path.exists(log_file):
        print(f"\n3. SUCCESS: Log file created at {log_file}")
        with open(log_file, 'r') as f:
            lines = f.readlines()
            print(f"   Log file has {len(lines)} lines.")
    else:
        print(f"\n3. FAILURE: Log file NOT found at {log_file}")

    print("\n--- Phase 1 Verification End ---")

if __name__ == "__main__":
    test_phase1()
