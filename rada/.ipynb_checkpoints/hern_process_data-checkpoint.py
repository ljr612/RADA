import sys
import pandas as pd
import os
import json
import argparse
import prody 
import sidechainnet.utils.measure 

def tocdr(resseq):
    if 27 <= resseq <= 38:
        return '1'
    elif 56 <= resseq <= 65:
        return '2'
    elif 105 <= resseq <= 117:
        return '3'
    else:
        return '0'

def apply_antibody_data(data):

    pdb_path = os.popen(f"ls {data['path']}").readline()[:-1]
    if os.path.exists(pdb_path):
        protein_pdb = prody.parsePDB(pdb_path, model=1)
    else:
        protein_pdb = prody.parsePDB(data["pdb_id"], model=1)
    
    if data["heavy_chain"] == 0 and data["CDR_type"][-1] in list("123"):
        hseq =  "L" * 209
        hcdr_list = ["0"] * len(hseq)
        if data["CDR_type"][-1] == "1":
            hcdr_list[25:25+int(data["CDR_len"])] = [data["CDR_type"][-1]] * int(data["CDR_len"])
        elif data["CDR_type"][-1] == "2":
            hcdr_list[50:50+int(data["CDR_len"])] = [data["CDR_type"][-1]] * int(data["CDR_len"])
        elif data["CDR_type"][-1] == "3":
            hcdr_list[96:96+int(data["CDR_len"])] = [data["CDR_type"][-1]] * int(data["CDR_len"])
        hcdr = "".join(hcdr_list)
        hcoords = torch.zeros((len(hseq), 14, 3)).tolist()
    else:
        hchain = protein_pdb[data["heavy_chain"]]
        _, hcoords, hseq, _, _ = sidechainnet.utils.measure.get_seq_coords_and_angles(hchain)
        hcdr = ''.join([tocdr(res.getResnum()) for res in hchain.iterResidues()])
        hcdr = hcdr[:len(hseq)]
        hcoords = hcoords.reshape((len(hseq), 14, 3))
        hcoords = eval(np.array2string(hcoords, separator=',', threshold=np.inf, precision=3, suppress_small=True))

    achain = protein_pdb[data["antigen"][0]]
    _, acoords, aseq, _, _ = sidechainnet.utils.measure.get_seq_coords_and_angles(achain)
    acoords = acoords.reshape((len(aseq), 14, 3))
    acoords = eval(np.array2string(acoords, separator=',', threshold=np.inf, precision=3, suppress_small=True))

    res = json.dumps({
        "pdb": data["pdb_id"], 
        "antibody_seq": hseq, "antibody_cdr": hcdr, "antibody_coords": hcoords,
        "antigen_seq": aseq, "antigen_coords": acoords, 
    })

    return res

def get_argparse():
    """
    Parse command-line arguments
    """
    description = """ 
    Organize antigen-antibody complexes from the PDB database into JSONL format files for model training.
    The input file is an Excel file containing information about antigen-antibody complexes, as follows:
    pdb_id	heavy_chain	light_chain	antigen  CDR_type  CDR_len   path
    7C01	  H	         L	         B        CDR_H3      12     ./xx/xx.pdb
    """
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--input', help="Input file, must be in Excel format. Example: ./xxx.excel")
    parser.add_argument('-s', '--sheet', default="Sheet1", help="The name of the sheet where the input file is located. Example: Sheet1. Default is Sheet1.")
    parser.add_argument('-o', '--output', help="Output file, JSONL format (each line is a JSON file). Example: ./xxx.jsonl")
    return parser


def main():
    os.chdir(sys.path[0])
    args = get_argparse().parse_args()

    antibody_data = pd.read_excel(args.input, sheet_name=args.sheet).fillna(0)
    result = antibody_data.apply(apply_antibody_data, axis=1)

    with open(args.output, "w") as file:
        for i in result:
            file.write(i + "\n")

if __name__ == "__main__":
    main()
