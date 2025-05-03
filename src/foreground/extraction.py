import pandas as pd
import numpy as np
from pathlib import Path

def extract_and_save_population(pop, name, save_dir="extracted_data"):
    """
    Extracts bpp and final positions from a Cogsworth Population object,
    aligns them using bin_num, and saves to a single .parquet file.

    Parameters:
    -----------
    pop : cogsworth.pop.Population
        The population object (e.g., g1010_014)
    name : str
        Output filename prefix (e.g., "g1010_014")
    save_dir : str
        Directory to save the .parquet file
    """

    _ = pop.final_pos  # Ensure it's loaded
    pos_array = pop._final_pos.to("kpc").value
    bin_nums = pop.bin_nums

    safe_mask = bin_nums < len(pos_array)
    safe_bin_nums = bin_nums[safe_mask]
    safe_pos_array = pos_array[safe_bin_nums]

    pos_df = pd.DataFrame(safe_pos_array, columns=["x_kpc", "y_kpc", "z_kpc"])
    pos_df["bin_num"] = safe_bin_nums

    bpp = pop._final_bpp
    bpp_trimmed = bpp[bpp["bin_num"].isin(safe_bin_nums)].copy()

    merged_df = pd.merge(bpp_trimmed, pos_df, on="bin_num")

    Path(save_dir).mkdir(parents=True, exist_ok=True)
    out_path = Path(save_dir) / f"{name}_bpp_with_pos.parquet"
    merged_df.to_parquet(out_path, index=False)

    print(f" Saved: {out_path} (shape = {merged_df.shape})")
