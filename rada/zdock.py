import argparse
import os
from multiprocessing import Pool

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run zdock for multiple antibody files against a given antigen.")
    parser.add_argument("-i", "--antibody_dir", type=str, help="Directory containing antibody PDB files.")
    parser.add_argument("-a", "--antigen", type=str, help="Antigen PDB file.")
    parser.add_argument("-o", "--output_dir", type=str, help="Output directory for zdock results.")
    return parser.parse_args()

def run_zdock(args):
    antibody_file, antigen, antibody_dir, output_dir = args
    if not antibody_file.endswith('.pdb'):
        return
    input_file = os.path.join(antibody_dir, antibody_file)
    output_file = os.path.join(output_dir, f"{antibody_file.split('.')[0]}.out")
    os.system(f"../zdock/zdock -R {antigen} -L {input_file} -o {output_file}")

def main(args):
    antibody_dir = args.antibody_dir
    antigen = args.antigen
    output_dir = args.output_dir

    antibody_files = os.listdir(antibody_dir)

    with Pool() as pool:
        pool.map(run_zdock, [(file, antigen, antibody_dir, output_dir) for file in antibody_files])

if __name__ == "__main__":
    args = parse_arguments()
    main(args)
