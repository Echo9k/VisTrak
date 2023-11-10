import subprocess

# execute extract.py
subprocess.run(["python", "/workspaces/anaconda-postgres/etl/extract.py"])

# execute transform.py
subprocess.run(["python", "/workspaces/anaconda-postgres/etl/transform.py"])

# execute load.py
subprocess.run(["python", "/workspaces/anaconda-postgres/etl/load.py"])