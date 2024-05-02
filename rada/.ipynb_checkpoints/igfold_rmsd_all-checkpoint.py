import os
import pandas as pd
import numpy as np
from multiprocessing import Pool
import argparse

def calculate_rmsd(filename):
    result = os.popen(f"python igfold_rmsd.py {filename}").readlines()
    all = result[0].split()
    return all

def parse_args():
    parser = argparse.ArgumentParser(description="Calculate RMSD for PDB files")
    parser.add_argument("-i", "--input_dir", type=str, required=True, help="Input directory containing PDB files")
    parser.add_argument("-o", "--output_file", type=str, required=True, help="Output CSV file")
    return parser.parse_args()

def main():
    args = parse_args()
    pdb_dir = args.input_dir
    output_file = args.output_file
    
    file_list = [f.split(".")[0] for f in os.listdir(pdb_dir) if f.endswith(".pdb")]

    res = pd.DataFrame(
        np.zeros((len(file_list), 7)),
        columns=["rmsd", "rmsdh1", "rmsdh2", "rmsdh3", "rmsdl1", "rmsdl2", "rmsdl3"],
        index=file_list
    )

    def call_back(result):
        i = result[0]
        for j in range(7):
            res.loc[i, res.columns[j]] = float("{:.4f}".format(float(result[j+1])))

    pool = Pool()
    for i in res.index:
        pool.apply_async(calculate_rmsd, args=(f"{pdb_dir}/{i}.pdb",), callback=call_back)

    pool.close()
    pool.join()

    res.to_csv(output_file)

if __name__ == "__main__":
    main()
