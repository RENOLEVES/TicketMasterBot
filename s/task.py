import subprocess
import time

for i in range(1):
    print(f"\n--- Iteration {i+1} ---")

    # Run main.py
    subprocess.run(["python", "s/main.py"])

    # Run process.py
    subprocess.run(["python", "s/process.py"])

    # # Wait for 5 minutes (300 seconds)
    # if i < 9:  # No need to wait after the last iteration
    #     print("Waiting 5 minutes...")
    #     time.sleep(300)

print("\nDone.")