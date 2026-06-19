"""
stats.py — Validate label distribution of a labeled CSV.

Reads a labeled CSV (default: data/takemeter_dataset.csv) and prints
label counts, percentages, and warnings for imbalance issues.

Usage:
    python stats.py                          # reads data/takemeter_dataset.csv
    python stats.py data/prelabeled_posts.csv  # reads a specific file
"""

import csv
import sys
from collections import Counter
from pathlib import Path


def main():
    # Determine which CSV to read
    script_dir = Path(__file__).resolve().parent
    if len(sys.argv) > 1:
        csv_path = Path(sys.argv[1])
    else:
        csv_path = script_dir / "data" / "takemeter_dataset.csv"

    if not csv_path.exists():
        print(f"❌ File not found: {csv_path}")
        sys.exit(1)

    # Read the CSV
    with open(csv_path, "r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print(f"❌ {csv_path} is empty.")
        sys.exit(1)

    total = len(rows)

    # Count labels
    label_counts = Counter(row.get("label", "MISSING") for row in rows)

    # Count notes
    notes_count = sum(
        1 for row in rows
        if row.get("notes", "").strip()
        and row.get("notes", "").strip() != "[AI-prelabeled]"
    )

    # Print results
    print(f"\n{'='*50}")
    print(f"📊 Dataset Statistics: {csv_path}")
    print(f"{'='*50}")
    print(f"\nTotal examples: {total}")
    print(f"\n{'Label':<25} {'Count':>6} {'%':>8}")
    print(f"{'-'*41}")

    warnings = []

    for label, count in sorted(label_counts.items(), key=lambda x: -x[1]):
        pct = (count / total) * 100
        flag = ""

        if label == "UNKNOWN":
            flag = " ⚠️  NEEDS REVIEW"
            warnings.append(f"  {count} examples labeled UNKNOWN — need manual labeling")
        elif pct > 70:
            flag = " ⚠️  ABOVE 70%"
            warnings.append(
                f"  '{label}' is {pct:.1f}% of dataset — exceeds 70% threshold"
            )
        elif count < 20:
            flag = " ⚠️  BELOW 20"
            warnings.append(
                f"  '{label}' has only {count} examples — below 20 minimum"
            )

        print(f"  {label:<23} {count:>6} {pct:>7.1f}%{flag}")

    print(f"\nPosts with manual notes: {notes_count}")

    # Milestone 3 checkpoint checks
    print(f"\n{'='*50}")
    print(f"📍 Milestone 3 Checkpoint")
    print(f"{'='*50}")

    checks = []

    # Check 1: At least 200 examples
    if total >= 200:
        checks.append(("✅", f"Total examples: {total} (≥ 200)"))
    else:
        checks.append(("❌", f"Total examples: {total} (need ≥ 200, missing {200 - total})"))

    # Check 2: No label above 70%
    max_label = max(label_counts.items(), key=lambda x: x[1])
    max_pct = (max_label[1] / total) * 100
    if max_pct <= 70:
        checks.append(("✅", f"Max label: '{max_label[0]}' at {max_pct:.1f}% (≤ 70%)"))
    else:
        checks.append(("❌", f"Max label: '{max_label[0]}' at {max_pct:.1f}% (exceeds 70%)"))

    # Check 3: At least 3 difficult cases documented
    if notes_count >= 3:
        checks.append(("✅", f"Documented difficult cases: {notes_count} (≥ 3)"))
    else:
        checks.append(("❌", f"Documented difficult cases: {notes_count} (need ≥ 3)"))

    for icon, msg in checks:
        print(f"  {icon} {msg}")

    # Print warnings
    if warnings:
        print(f"\n⚠️  Warnings:")
        for w in warnings:
            print(w)

    print()


if __name__ == "__main__":
    main()
