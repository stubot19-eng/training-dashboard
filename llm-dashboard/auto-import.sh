#!/bin/bash
# Auto-import LLM usage data every 60 seconds

cd /root/.openclaw/workspace/llm-dashboard

while true; do
  node import-usage.js > /tmp/import.log 2>&1
  sleep 60
done
