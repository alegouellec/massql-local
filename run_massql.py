from massql import msql_engine
from massql import msql_fileloading

# Input MGF file located in the same folder as this script
input_file = "ALL_GNPS_cleaned.mgf"

# Output results file
output_file = "results_IAA_conjugates.tsv"

# MassQL query
query = (
    "QUERY scaninfo(MS2DATA) WHERE "
    "MS2PROD=172.076:TOLERANCEMZ=0.001:INTENSITYPERCENT=2 "
    "AND MS2PROD=130.065:TOLERANCEMZ=0.001:INTENSITYPERCENT=40"
)

print("Loading data...")
ms1_df, ms2_df = msql_fileloading.load_data(input_file)
print(f"Loaded {len(ms2_df)} MS2 spectra")

print("Running query...")
results_df = msql_engine.process_query(
    query,
    input_file,
    ms1_df=ms1_df,
    ms2_df=ms2_df,
)

print(f"Found {len(results_df)} matches")
results_df.to_csv(output_file, sep="\t", index=False)
print(f"Results saved to {output_file}")
