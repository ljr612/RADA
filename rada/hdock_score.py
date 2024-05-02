import os
import argparse
import pandas as pd
import numpy as np
from multiprocessing import Pool

def process_file(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        line_six = lines[5].strip()
        return line_six.split()[-3]

def run_docking_score(input_dir, output_csv):
    file_list = [f.split(".")[-2] for f in os.listdir(input_dir) if f.endswith(".out")]
    
    with Pool() as pool:
        docking_scores = pool.map(process_file, [os.path.join(input_dir, f"{file}.out") for file in file_list])

    res1 = pd.DataFrame(docking_scores, columns=["docking score"], index=file_list)
    res1.to_csv(output_csv)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process docking output files and extract docking scores.")
    parser.add_argument('-i', '--input_dir', required=True, help="Input directory containing docking output files.")
    parser.add_argument('-o', '--output_csv', required=True, help="Output CSV file to save docking scores.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    input_dir = args.input_dir
    output_csv = args.output_csv
    run_docking_score(input_dir, output_csv)
