import subprocess

NUM_RUNS = 20

for i in range(NUM_RUNS):
    print(f"=== Run {i+1}/{NUM_RUNS} ===")
    subprocess.run(["python", "main.py"])
