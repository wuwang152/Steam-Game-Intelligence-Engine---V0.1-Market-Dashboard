"""Environment dependency verification script for V0.1."""

from __future__ import annotations

import importlib
import sys


DEPENDENCIES = ["pandas", "numpy", "streamlit", "pytest"]


def main() -> int:
    missing: list[str] = []

    print("Checking required Python dependencies...")
    for name in DEPENDENCIES:
        try:
            module = importlib.import_module(name)
        except ModuleNotFoundError:
            missing.append(name)
            continue

        version = getattr(module, "__version__", "unknown")
        print(f"- {name}: {version}")

    if missing:
        print(
            "\nERROR: Missing required dependencies: "
            + ", ".join(missing)
            + ". Install requirements with: python -m pip install -r requirements.txt",
            file=sys.stderr,
        )
        return 1

    print("\nAll required dependencies are installed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
