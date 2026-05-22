# Data Quality Report (V0.1)

## Scope
This report summarizes baseline checks for the processed Steam dataset.

## Validation checks
1. Required columns exist (AppID, Name, release_year, Price, positive_ratio, owners_low, owners_high).
2. AppID is non-null and unique.
3. Price contains no negative values.
4. positive_ratio remains in [0, 1].
5. owners_low is never greater than owners_high.

## Notes
- Use `python scripts/validate_data.py --input <processed_csv_path>` to validate any processed extract.
- Review sampling outliers manually for owner ranges, review totals, and price spikes.
