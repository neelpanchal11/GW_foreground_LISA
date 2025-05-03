import pandas as pd
from pathlib import Path

def merge_galaxy_batches(galaxy_name, base_path="/Users/neelpanchal/extracted_data"):
    batch_dir = Path(base_path) / galaxy_name / "batches"
    output_path = Path(base_path) / f"{galaxy_name}_merged.parquet"

    # Match all .parquet files regardless of name
    files = sorted(batch_dir.glob("*.parquet"))

    if not files:
        print(f" No parquet files found in {batch_dir}")
        return

    print(f"📦 Merging {len(files)} files in {galaxy_name}/batches...")

    df = pd.concat((pd.read_parquet(f) for f in files), ignore_index=True)
    df.to_parquet(output_path, index=False)

    print(f" Merged file saved at: {output_path} | Rows: {len(df)}")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("galaxy_name")
    ap.add_argument("--base-path", default="data")
    args = ap.parse_args()
    merge_galaxy_batches_anyname(args.galaxy_name, args.base_path)
