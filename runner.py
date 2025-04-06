import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

input_dir = "./input"
output_dir = "./output"
script_to_run = "main.py"
max_workers = os.cpu_count() - 2

os.makedirs(output_dir, exist_ok=True)

custom_permutations = [
    "RDUL",
    "RDLU",
    "DRUL",
    "DRLU",
    "LUDR",
    "LURD",
    "ULDR",
    "ULRD"
]

heuristics = ['manh', 'hamm']

input_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]

jobs = []

for input_file in input_files:
    base_name = os.path.splitext(input_file)[0]
    input_path = os.path.join(input_dir, input_file)

    for alg in ["bfs", "dfs"]:
        for perm in custom_permutations:
            output_file = os.path.join(output_dir, f"{base_name}_{alg}_{perm}_sol.txt")
            stats_file = os.path.join(output_dir, f"{base_name}_{alg}_{perm}_stats.txt")
            jobs.append([
                "python", script_to_run,
                alg,
                perm,
                input_path,
                output_file,
                stats_file
            ])

    for h in heuristics:
        output_file = os.path.join(output_dir, f"{base_name}_astr_{h}_sol.txt")
        stats_file = os.path.join(output_dir, f"{base_name}_astr_{h}_stats.txt")
        jobs.append([
            "python", script_to_run,
            "astr",
            h,
            input_path,
            output_file,
            stats_file
        ])

def run_job(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[ERROR] {' '.join(cmd)}\n{result.stderr}")
        else:
            print(f"[OK] {' '.join(cmd[3:])}")
        return cmd
    except Exception as e:
        print(f"[EXCEPTION] {' '.join(cmd)}: {e}")
        return None

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = [executor.submit(run_job, job) for job in jobs]
    for future in as_completed(futures):
        _ = future.result()
