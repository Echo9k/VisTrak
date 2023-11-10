#!/bin/bash

# Execute extract.py
python /workspaces/anaconda-postgres/etl/extract.py

# Execute transform.py
python /workspaces/anaconda-postgres/etl/transform.py

# Execute load.py
python /workspaces/anaconda-postgres/etl/load.py
