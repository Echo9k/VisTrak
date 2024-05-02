import subprocess

# execute extract.py
subprocess.run(["python", "/workspaces/VisTrak/etl/extract.py"])

# execute transform.py
subprocess.run(["python", "/workspaces/VisTrak/etl/transform.py"])

# execute load.py
subprocess.run(["python", "/workspaces/VisTrak/etl/load.py"])