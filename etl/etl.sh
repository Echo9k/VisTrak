#!/bin/bash


python /workspaces/VisTrak/etl/extract.py  # Execute extract.py
python /workspaces/VisTrak/etl/transform.py  # Execute transform.py
python /workspaces/VisTrak/etl/load.py  # Execute load.py
