#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_scaled_his_datasets.py

Generate scaled variants of selected HIS dataset tables:
- scale_100k
- scale_500k
- scale_1m

The target size refers to the number of rows in the medical records table.
Related tables are scaled proportionally to preserve the structure of the
original academic HIS dataset.
"""

import argparse
import csv
import random
import shutil
from datetime import datetime, timedelta
from pathlib import Path


TARGETS = {
    "scale_100k": 100_000,
    "scale_500k": 500_000,
    "scale_1m": 1_000_000,
}

INPUT_FILES = {
    "MEDICAL_CARD": ["medical_cards.csv", "ZDRAVOTNA_KARTA.csv"],
    "MEDICAL_RECORD": [
        "medical_records.csv",
        "ZDRAVOTNY_ZAZNAM.csv",
        "ZDRAVOTNY_ZAZ1.csv",
        "ZDRAVOTNY_ZAZ.csv",
    ],
    "HOSPITALIZATION": ["hospitalizations.csv", "HOSPITALIZACIA.csv"],
    "EXAMINATION": ["examinations.csv", "VYSETRENIE.csv"],
}

OUTPUT_FILES = {
    "MEDICAL_CARD": "medical_cards.csv",
    "MEDICAL_RECORD": "medical_records.csv",
    "HOSPITALIZATION": "hospitalizations.csv",
    "EXAMINATION": "examinations.csv",
}


def parse_args():
    parser = argparse.ArgumentParser(description="Generate scaled HIS dataset variants.")
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Directory containing the source CSV files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory where scaled outputs will be generated. Defaults to <input-dir>/scaled_output.",
    )
    return parser.parse_args()


def find_input_file(base_dir: Path, candidates: list[str]) -> Path:
    for name in candidates:
        path = base_dir / name
        if path.exists():
            return path
    raise FileNotFoundError(f"Missing input file. Tried: {', '.join(candidates)}")


def read_csv_rows(path: Path) -> list[list[str]]:
    with open(path, "r", encoding="utf-8", errors="replace", newline="") as f:
        return list(csv.reader(f))


def write_csv_rows(path: Path, rows_iterable):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for row in rows_iterable:
            writer.writerow(row)


def shift_date(value: str, shift_days: int) -> str:
    if value is None:
        return value

    text = str(value).strip()
    if not text or text.lower() == "null":
        return value

    try:
        date_value = datetime.strptime(text, "%Y-%m-%d").date()
        return (date_value + timedelta(days=shift_days)).isoformat()
    except ValueError:
        return value


def copy_baseline(src_paths: dict[str, Path], out_dir: Path):
    baseline_dir = out_dir / "baseline"
    baseline_dir.mkdir(parents=True, exist_ok=True)

    for key, out_name in OUTPUT_FILES.items():
        shutil.copyfile(src_paths[key], baseline_dir / out_name)


def generate_scaled_variant(
    variant_name: str,
    target_record_count: int,
    src: dict[str, list[list[str]]],
    out_root: Path,
):
    out_dir = out_root / variant_name
    out_dir.mkdir(parents=True, exist_ok=True)

    n_cards = len(src["MEDICAL_CARD"])
    n_records = len(src["MEDICAL_RECORD"])
    n_hospitalizations = len(src["HOSPITALIZATION"])
    n_examinations = len(src["EXAMINATION"])

    target_cards = round(target_record_count * n_cards / n_records)
    target_hospitalizations = round(target_record_count * n_hospitalizations / n_records)
    target_examinations = round(target_record_count * n_examinations / n_records)

    print(f"\nGenerating {variant_name}")
    print(f"  medical_cards:    {target_cards:,}")
    print(f"  medical_records:  {target_record_count:,}")
    print(f"  hospitalizations: {target_hospitalizations:,}")
    print(f"  examinations:     {target_examinations:,}")

    # MEDICAL_CARD: [0] card ID, [1] patient ID, [2] blood type, [3] from date, [4] to date
    def gen_cards():
        for i in range(target_cards):
            row = list(src["MEDICAL_CARD"][i % n_cards])
            cycle = i // n_cards
            shift = (cycle * 17) % 3650

            if len(row) > 0:
                row[0] = str(i + 1)
            if len(row) > 1:
                row[1] = str(i + 1)
            if len(row) > 3:
                row[3] = shift_date(row[3], shift)
            if len(row) > 4:
                row[4] = shift_date(row[4], shift)

            yield row

    # MEDICAL_RECORD: [0] record ID, [1] card ID, last column = date
    def gen_records():
        rng = random.Random(1000 + target_record_count)
        for i in range(target_record_count):
            row = list(src["MEDICAL_RECORD"][i % n_records])
            cycle = i // n_records
            shift = (cycle * 23) % 3650

            if len(row) > 0:
                row[0] = str(i + 1)
            if len(row) > 1:
                row[1] = str(rng.randint(1, target_cards))
            if len(row) > 0:
                row[-1] = shift_date(row[-1], shift)

            yield row

    # HOSPITALIZATION: [0] ID, [2] previous hospitalization, [3] record ID, [4:5] dates
    def gen_hospitalizations():
        rng = random.Random(2000 + target_record_count)
        for i in range(target_hospitalizations):
            row = list(src["HOSPITALIZATION"][i % n_hospitalizations])
            cycle = i // n_hospitalizations
            shift = (cycle * 29) % 3650

            if len(row) > 0:
                row[0] = str(i + 1)

            if len(row) > 2:
                old_prev = str(row[2]).strip().lower()
                if old_prev != "null" and i > 0:
                    row[2] = str(rng.randint(1, i))
                else:
                    row[2] = "null"

            if len(row) > 3:
                row[3] = str(rng.randint(1, target_record_count))
            if len(row) > 4:
                row[4] = shift_date(row[4], shift)
            if len(row) > 5:
                row[5] = shift_date(row[5], shift)

            yield row

    # EXAMINATION: [0] examination ID, [3] record ID, [4] date
    def gen_examinations():
        rng = random.Random(3000 + target_record_count)
        for i in range(target_examinations):
            row = list(src["EXAMINATION"][i % n_examinations])
            cycle = i // n_examinations
            shift = (cycle * 31) % 3650

            if len(row) > 0:
                row[0] = str(i + 1)
            if len(row) > 3:
                row[3] = str(rng.randint(1, target_record_count))
            if len(row) > 4:
                row[4] = shift_date(row[4], shift)

            yield row

    write_csv_rows(out_dir / OUTPUT_FILES["MEDICAL_CARD"], gen_cards())
    write_csv_rows(out_dir / OUTPUT_FILES["MEDICAL_RECORD"], gen_records())
    write_csv_rows(out_dir / OUTPUT_FILES["HOSPITALIZATION"], gen_hospitalizations())
    write_csv_rows(out_dir / OUTPUT_FILES["EXAMINATION"], gen_examinations())

    return {
        "variant": variant_name,
        "medical_cards": target_cards,
        "medical_records": target_record_count,
        "hospitalizations": target_hospitalizations,
        "examinations": target_examinations,
    }


def write_readme(out_root: Path, manifest: list[dict]):
    readme = out_root / "README.md"
    with open(readme, "w", encoding="utf-8") as f:
        f.write("# Scaled HIS Dataset Variants\n\n")
        f.write("This directory contains scaled variants of the synthetic academic HIS dataset.\n\n")
        f.write("The target size refers to the number of rows in `medical_records.csv`. ")
        f.write("Related tables were scaled proportionally to preserve the structure of the original HIS dataset.\n\n")

        f.write("| Variant | medical_cards | medical_records | hospitalizations | examinations |\n")
        f.write("|---|---:|---:|---:|---:|\n")
        for item in manifest:
            f.write(
                f"| {item['variant']} | {item['medical_cards']} | "
                f"{item['medical_records']} | {item['hospitalizations']} | {item['examinations']} |\n"
            )

        f.write("\n## Generation Notes\n\n")
        f.write("- Primary identifiers were regenerated sequentially.\n")
        f.write("- Foreign-key-like references were remapped to valid generated identifiers.\n")
        f.write("- Dates were deterministically shifted across generation cycles.\n")
        f.write("- Domain values and statistical patterns were preserved by controlled scaling of the baseline dataset.\n")


def main():
    args = parse_args()
    base_dir = args.input_dir.resolve()
    out_root = args.output_dir.resolve() if args.output_dir else base_dir / "scaled_output"

    print("Input directory:", base_dir)
    print("Output directory:", out_root)

    src_paths = {
        key: find_input_file(base_dir, candidates)
        for key, candidates in INPUT_FILES.items()
    }

    print("\nInput files:")
    for key, path in src_paths.items():
        print(f"  {key}: {path.name}")

    src = {
        key: read_csv_rows(path)
        for key, path in src_paths.items()
    }

    print("\nBaseline counts:")
    for key, rows in src.items():
        print(f"  {key}: {len(rows):,}")

    if out_root.exists():
        shutil.rmtree(out_root)
    out_root.mkdir(parents=True, exist_ok=True)

    copy_baseline(src_paths, out_root)

    manifest = []
    for variant, target in TARGETS.items():
        manifest.append(generate_scaled_variant(variant, target, src, out_root))

    write_readme(out_root, manifest)

    print("\nDone.")
    print(f"Generated datasets are stored in: {out_root}")


if __name__ == "__main__":
    main()
