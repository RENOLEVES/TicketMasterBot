import subprocess
import time

start_time = time.time()

# Run main.py
subprocess.run(["python", "s/main.py"])

# Run process.py
subprocess.run(["python", "s/process.py"])

# # Wait for 5 minutes (300 seconds)
# if i < 9:  # No need to wait after the last iteration
#     print("Waiting 5 minutes...")
#     time.sleep(300)

end_time = time.time()
print("\nDone.")
print("seconds: ",end_time-start_time)