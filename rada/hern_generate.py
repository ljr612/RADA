import os
import sys
import argparse

def get_argparse():
    description = """ 
    Script Description:
    Given the PDB information of the antigen, design CDRs using HERN. The input file is an Excel file with the following columns:
    pdb_id: The ID of the antigen-antibody complex in the PDB database
    heavy_chain: The name of the antibody heavy chain
    light_chain: The name of the antibody light chain
    antigen: The name of the antigen chain
    CDR_type: The type of CDR, set to CDR_H3
    CDR_len: The length of the CDR
    path: The local path of the PDB file
    Example: 7C01 H L B CDR_H3 12 ./xx/xx.pdb

    Script Usage:
        python process_data.py -i ./xxx.excel -o ./output.txt
        
     """
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--input', help="Input file, must be in Excel format. Example: ./xxx.excel")
    parser.add_argument('-o', '--output', help="Output file, a text file.")
    return parser


def main():
    project_dir = os.path.abspath("../hern")
    os.chdir(sys.path[0])
    args = get_argparse().parse_args()
    
    os.system(f"python hern_process_data.py -i {args.input} -o {project_dir}/tmp/abdockgen_data_tmp.jsonl ")
    print("complete")
    
    os.system(
        f"python {project_dir}/generate.py {project_dir}/ckpts/HERN_gen.ckpt \
        {project_dir}/tmp/abdockgen_data_tmp.jsonl \
        500  > {args.output} "
    )

if __name__ == "__main__":
    main()