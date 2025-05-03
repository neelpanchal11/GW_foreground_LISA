import argparse
from cogsworth import pop, sfh
from extraction import extract_and_save_population
from pathlib import Path
import numpy as np
from cogsworth.pop import Population
import pandas as pd
import astropy.units as u

def main(index):
    output_dir = "batches"
    Path(output_dir).mkdir(exist_ok=True)
    np.random.seed(index)

    p = pop.Population(
    n_binaries=50000,    # no of binaries can be set here
    processes = 1,       # no of processes
    final_kstar1 =[10],  # List of types of k_stars.
    final_kstar2 = [10],
    BSE_settings={
        "kickflag": 1,  # set this to 1 or another valid value
        "metallicity": 0.014, #set the metallicity
        # other parameters as needed...
    }
    )

    p.sample_initial_galaxy()
    p.sample_initial_binaries()
    p.create_population()

    name = f"g1010_014_{index:04d}"  #change the name here based on your preference.
    extract_and_save_population(p, name, save_dir=output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-index", type=int, required=True)
    args = parser.parse_args()
    main(args.batch_index)

