# Codex Environment Setup & Validation Commands

Use these exact commands for setup and validation:

1. `python -m pip install -r requirements.txt`
2. `PYTHONPATH=src python scripts/run_pipeline.py --input data/sample/games_sample.csv --output data/processed/steam_games_cleaned.csv`
3. `PYTHONPATH=src python scripts/validate_data.py --input data/processed/steam_games_cleaned.csv`
4. `PYTHONPATH=src pytest -q`
