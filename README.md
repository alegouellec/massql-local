# massql-local

Run MassQL queries locally on MGF files to quickly detect MS/MS spectra matching targeted fragmentation patterns.

## Overview

This repository contains a simple local workflow to run **MassQL** queries on `.mgf` files and export matching MS/MS spectra to a `.tsv` results file.

Running the query locally can be faster than using the equivalent **GNPS2 workflow**, especially when working with large preprocessed files already available on disk.

## Purpose

The goal of this workflow is to:

- load an input `.mgf` file containing MS/MS spectra,
- search for spectra matching a targeted fragmentation pattern,
- retrieve the matching scan information,
- export the results to a tab-separated `.tsv` file.

## Example query

The example provided in this repository searches for MS/MS spectra containing:

- a product ion at **m/z 172.076** with a minimum relative intensity of **2%**
- a product ion at **m/z 130.065** with a minimum relative intensity of **40%**

using a mass tolerance of **0.001 m/z** for both fragments.

## Requirements

Make sure you have the following installed:

- Python 3
- `massql`
- `pandas`
- `tqdm` *(optional in this example, but included in the original script)*

Install dependencies with:

```bash
pip install massql pandas tqdm
```

## Folder organization

Place the script in the same folder as your `.mgf` library file, or update the filename in the script to match your local setup.

Example:

```text
project_folder/
├── run_massql.py
└── ALL_GNPS_cleaned.mgf
```

In this example, the script assumes that the `.mgf` file is located in the current working directory.

## Example script

```python
from massql import msql_engine
from massql import msql_fileloading
from tqdm import tqdm
import pandas as pd

input_file = 'ALL_GNPS_cleaned.mgf'
output_file = 'results_IAA_conjugates.tsv'
query = 'QUERY scaninfo(MS2DATA) WHERE MS2PROD=172.076:TOLERANCEMZ=0.001:INTENSITYPERCENT=2 AND MS2PROD=130.065:TOLERANCEMZ=0.001:INTENSITYPERCENT=40'

print('Loading data...')
ms1_df, ms2_df = msql_fileloading.load_data(input_file)
print(f'Loaded {len(ms2_df)} MS2 spectra')

print('Running query...')
results_df = msql_engine.process_query(query, input_file, ms1_df=ms1_df, ms2_df=ms2_df)

print(f'Found {len(results_df)} matches')
results_df.to_csv(output_file, sep='\t', index=False)
print(f'Results saved to {output_file}')
```

## How to run it locally

### Option 1 — Run directly from the terminal

If your `.mgf` file is in the current folder, you can run:

```bash
python3 -c "
from massql import msql_engine
from massql import msql_fileloading
from tqdm import tqdm
import pandas as pd

input_file = 'ALL_GNPS_cleaned.mgf'
output_file = 'results_IAA_conjugates.tsv'
query = 'QUERY scaninfo(MS2DATA) WHERE MS2PROD=172.076:TOLERANCEMZ=0.001:INTENSITYPERCENT=2 AND MS2PROD=130.065:TOLERANCEMZ=0.001:INTENSITYPERCENT=40'

print('Loading data...')
ms1_df, ms2_df = msql_fileloading.load_data(input_file)
print(f'Loaded {len(ms2_df)} MS2 spectra')

print('Running query...')
results_df = msql_engine.process_query(query, input_file, ms1_df=ms1_df, ms2_df=ms2_df)

print(f'Found {len(results_df)} matches')
results_df.to_csv(output_file, sep='	', index=False)
print(f'Results saved to {output_file}')
"
```

### Option 2 — Save as a Python script

Save the code in a file called `run_massql.py`, then run:

```bash
python3 run_massql.py
```

## How it works

### 1. Load the MGF file

The script reads the input `.mgf` file and loads the spectral data into memory.

```python
ms1_df, ms2_df = msql_fileloading.load_data(input_file)
```

### 2. Define the MassQL query

The query specifies the MS/MS pattern to search for:

```text
QUERY scaninfo(MS2DATA) WHERE MS2PROD=172.076:TOLERANCEMZ=0.001:INTENSITYPERCENT=2 AND MS2PROD=130.065:TOLERANCEMZ=0.001:INTENSITYPERCENT=40
```

This means the selected spectrum must contain:

- a fragment near **172.076**
- and a fragment near **130.065**
- with the specified minimum relative intensities

### 3. Run the query

The MassQL engine processes the query on the loaded MS/MS data:

```python
results_df = msql_engine.process_query(query, input_file, ms1_df=ms1_df, ms2_df=ms2_df)
```

### 4. Export the results

Matching scans are exported to a `.tsv` file:

```python
results_df.to_csv(output_file, sep='\t', index=False)
```

## Input and output

### Input

- `.mgf` file containing MS/MS spectra in the same folder as the script, or referenced by filename/path in `input_file`

### Output

- `.tsv` file containing the scan information for spectra matching the query

## Notes

- If the `.mgf` file is not in the same folder as the script, replace `ALL_GNPS_cleaned.mgf` with the correct filename or path.
- A tolerance of **0.001 m/z** is strict and best suited for high-resolution MS data.
- The intensity thresholds can be adjusted depending on the selectivity required.

## Why run this locally?

Compared with a remote workflow, local execution can be useful for:

- rapid testing of targeted fragmentation hypotheses,
- screening large `.mgf` files,
- avoiding repeated uploads to external platforms,
- iterating quickly on MassQL query design.

## Repository description

Local MassQL workflow for searching MGF files based on targeted MS/MS fragmentation patterns.

## License

Add a license here if needed.
