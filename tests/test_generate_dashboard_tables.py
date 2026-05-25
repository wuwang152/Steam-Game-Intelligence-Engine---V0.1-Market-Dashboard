import subprocess
import sys

import pandas as pd


def test_cli_generates_outputs(tmp_path):
    in_csv = tmp_path / "input.csv"
    out_dir = tmp_path / "out"
    pd.DataFrame([
        {"AppID": 1, "Name": "A", "owners_mid": 10, "total_reviews": 2, "positive_rate": 1.0},
    ]).to_csv(in_csv, index=False)

    cmd = [sys.executable, "scripts/generate_dashboard_tables.py", "--input", str(in_csv), "--output-dir", str(out_dir), "--top-n", "5", "--min-reviews", "1"]
    result = subprocess.run(cmd, check=False, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert (out_dir / "summary_metrics.csv").exists()
