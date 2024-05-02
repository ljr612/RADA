import os
import argparse
from Bio.PDB import PDBParser, PDBIO
from multiprocessing import Pool

def rename_residues(chain):
    res_id = 1
    for residue in chain.get_residues():
        if residue.id[1] == res_id:
            res_id += 1
            continue
        new_id = (' ', res_id, ' ')
        while new_id in [r.id for r in chain.get_residues()]:
            res_id += 1
            new_id = (' ', res_id, ' ')
        residue.id = new_id
        res_id += 1

    num = 1
    for residue in chain.get_residues():
        residue.id = (" ", num, " ")
        num += 1

def process_pdb(input_path, output_path):
    parser = PDBParser()
    io = PDBIO()
    structure = parser.get_structure('antibody', input_path)

    heavy_chain = structure[0]['H']
    rename_residues(heavy_chain)

    light_chain = structure[0]['L']
    rename_residues(light_chain)

    io.set_structure(structure)
    io.save(output_path)

def process_folder_parallel(input_folder, output_folder):
    pool = Pool()

    for filename in os.listdir(input_folder):
        if not filename.endswith('.pdb'): 
            continue

        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        pool.apply_async(process_pdb, args=(input_path, output_path))

    pool.close()
    pool.join()

def create_arg_parser():
    parser = argparse.ArgumentParser(description="Process PDB files and rename residues.")
    parser.add_argument("-i", "--input", help="Path to the input folder containing PDB files.")
    parser.add_argument("-o", "--output", help="Path to the output folder where renamed PDB files will be saved.")
    return parser

def main():
    parser = create_arg_parser()
    args = parser.parse_args()

    process_folder_parallel(args.input, args.output)

if __name__ == "__main__":
    main()
