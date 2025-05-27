# SIMULATING GALACTIC WHITE DWARF BINARY FOREGROUNDS FOR MULTI-SOURCE GRAVITATIONAL WAVE DETECTION WITH LISA
## Galactic white‑dwarf simulations → Cornish foreground fits → LISA‑ready PSDs
### Overview

> **✨ What’s inside?**

| Stage  | Key file | Purpose |
|--------|----------|---------|
| **1. Population** | `foreground/generation.py` | Uses [**Cogsworth**](https://cogsworth.readthedocs.io/en/latest/index.html) to birth & evolve WD binaries (COSMIC backend). |
| **2. Extraction** | `foreground/extraction.py` | Saves COSMIC BPP + Galactic XYZ to Parquet for each batch. |
| **3. Merging** | `foreground/merging.py` | Concatenates all batch Parquets into one galaxy file. |
| **4. Binning** | `foreground/binning.py` | Computes SNR, masks resolved sources, and logs unresolved PSD. |
| **5. HPC** | `scripts/Galaxy.slurm` | Quest array job → 200 batches in parallel(Can be changed as per user). |

> **Dependencies**

| Library | Role                   |
|---------|------------------------|
| [Cogsworth](https://cogsworth.readthedocs.io/en/latest/index.html) | COSMIC wrapper – stellar & binary evolution |
| [LEGWORK](https://legwork.readthedocs.io/en/latest/index.html)  | Strain, LISA sensitivity, GW PSD utilities |
| NumPy / Pandas / AstroPy | Data wrangling & units |
| Matplotlib / Seaborn | Publication‑quality plots |

> ## Galaxy data can be found here on this [link](https://mega.nz/folder/VBBFVKAD#u5vlzDw9xh3fo9aKCgc0vg)

## Quick demo  *(no SLURM, no Docker)*

```bash
git clone https://github.com/neelpanchal11/GW_foreground_LISA.git
cd wd-foreground-lisa

# add package to PYTHONPATH for one‑off use
export PYTHONPATH=$PWD/src:$PYTHONPATH

# generate one 50k-binary batch - Can be changed by changing the n_binaries in generation.py
python -m foreground.generation --batch-index 0   # batch-index changes the number of batch files. Each Batch File will generate n_binaries

# merge (pointless with one batch, but shows API):
python -m foreground.merging g1010_014

````
*n_binaries* can be changed by changing this line of code in ```generation.py```
````
n_binaries=50000,    # no of binaries can be set here
````

Let's say you want to have a galaxy of $10^7$ binaries, you can have it by generating $n$ binaries in each batch. The number of batches will depend on the value of $n$. For eg: I have *n_binaries* = $50,000$, so I will set the batch_index as 200 (i.e. 0-199) so that the total number of binaries lead to $10^7$ binaries. Both of them are in 'generation.py'.
````
python -m foreground.generation --batch-index 0   # batch-index changes the number of batch files. Each Batch File will generate n_binaries
in each sampling process.
````


Type of k_stars can be changed by changing this line of code in ```generation.py```. It takes list as input and check out the k_star output file to understand it better.
````
final_kstar1 =[10], 
final_kstar2 = [10],
````

Run the notebook to reproduce the thesis figures:

```bash
gw_lisa_confusion.ipynb
```

## 🛰️ Quest HPC

```bash
sbatch scripts/Galaxy.slurm    # 200 batches → data/batches/
```
