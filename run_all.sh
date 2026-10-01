#!/usr/bin/env bash
set -euo pipefail
python src/prepare_data.py
python src/quality_checks.py
python src/run_analysis.py
echo "PayPulse pipeline completed successfully."
