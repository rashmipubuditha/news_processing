#!/bin/bash

python /app/src/run.py process_data -cfg /app/config/cfg.yaml -dataset news -dirout "/app/outputs/"
python /app/src/run.py process_data_all -cfg /app/config/cfg.yaml -dataset news -dirout "/app/outputs/"
