import os
import pandas as pd
import numpy as np
from multiprocessing import Pool
import argparse
import subprocess

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process PDB files to extract docking metrics.")
    parser.add_argument('-i', '--input_dir', type=str, required=True, help="Input directory containing PDB files")
    parser.add_argument('-o', '--output_file', type=str, required=True, help="Output CSV file to store results")
    return parser.parse_args()

def process(file_info):
    i, pdb_dir = file_info
    command = f"~/.local/bin/prodigy {pdb_dir}/{i}.pdb --selection A H"
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        lines = result.stdout.splitlines()
        metrics = [i]
        for line in lines[-11:]:
            metrics.append(line.strip().split(" ")[-1])
        return metrics
    except subprocess.CalledProcessError as e:
        print(f"Error processing {i}: {e.stderr}")
        return None  # Return None to indicate an error occurred

def call_back(res, result_df):
    if res:  # Ensure that there is data (not None)
        idx = res[0]
        for j in range(1, 12):
            result_df.loc[idx, result_df.columns[j - 1]] = res[j]

def main():
    args = parse_arguments()
    pdb_dir = args.input_dir
    output_file = args.output_file

    file_list = [f.split(".")[0] for f in os.listdir(pdb_dir) if f.endswith(".pdb")]

    res_df = pd.DataFrame(
        np.zeros((len(file_list), 11)),
        columns=[
            "No. of intermolecular contacts",
            "No. of charged-charged contacts",
            "No. of charged-polar contacts",
            "No. of charged-apolar contacts",
            "No. of polar-polar contacts",
            "No. of apolar-polar contacts",
            "No. of apolar-apolar contacts",
            "Percentage of apolar NIS residues",
            "Percentage of charged NIS residues",
            "Predicted binding affinity (kcal.mol-1)",
            "Predicted dissociation constant (M) at 25.0°C"],
        index=file_list
    )

    with Pool() as pool:
        results = pool.map(process, [(i, pdb_dir) for i in file_list])
        for res in results:
            if res:  # Process only if the result is not None
                call_back(res, res_df)

    res_df.to_csv(output_file)

if __name__ == "__main__":
    main()
