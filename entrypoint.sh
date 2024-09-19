#!/usr/bin/env bash

source ~/.bashrc

cd /app/df-server
rye run fastapi run src/df_server/main.py &

cd ../ui
pnpm dev --host 0.0.0.0
