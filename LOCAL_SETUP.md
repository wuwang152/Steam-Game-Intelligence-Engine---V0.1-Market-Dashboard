# Local Setup (V0.1 Environment Stabilization)

## 1) Create and activate a virtual environment

### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 2) Install dependencies

```bash
python -m pip install -r requirements.txt
```

## 3) Set `PYTHONPATH`

### macOS/Linux
```bash
export PYTHONPATH=src
```

### Windows PowerShell
```powershell
$env:PYTHONPATH = "src"
```

## 4) Run environment check

```bash
python scripts/check_environment.py
```

## 5) Run the sample data pipeline

```bash
PYTHONPATH=src python scripts/run_pipeline.py --input data/sample/games_sample.csv --output data/processed/steam_games_cleaned.csv
```

## 6) Validate processed output

```bash
PYTHONPATH=src python scripts/validate_data.py --input data/processed/steam_games_cleaned.csv
```

## 7) Run tests

```bash
PYTHONPATH=src pytest -q
```

## 8) Run the Streamlit app

```bash
PYTHONPATH=src streamlit run app/Home.py
```

## Data handling note

Place large raw input files under `data/raw/`. Do **not** commit large raw datasets to the repository.
