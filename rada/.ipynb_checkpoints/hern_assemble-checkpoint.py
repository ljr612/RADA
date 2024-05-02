import argparse
import os
import pandas as pd

def sequence(seq):
    H1 = "QVQLVESGGEVVKPGGSLRLSCAASGFTFSSYYMSWVRQAPGKGLEWVGWIYSSGNTNYAQSFKGRVTISRDTSKNTLYLEMNSLRSEDTAVYYCAR"
    H2 = "WGQGTLVTVSS"
    H = H1 + seq + H2
    L = "DIVLTQSPSLSASPGDRVTISCRASQSGISNYLAWYQQKPGKAPKLLIYGASSRPSGVPDRFSGSGSGTDFTLTISGLQPEDEADYYCQQYDSSPWTFGGGTKLEIK"
    return H, L

def read_input(input_file):
    data = []
    with open(input_file, "r") as f:
        for line in f:
            filename, seq, ppl = line.strip().split(" ")
            H, L = sequence(seq)
            data.append([filename, H, L])
    df = pd.DataFrame(data, columns=["filename", "H", "L"])
    return df

def save_output(output_file, df):
    df.to_csv(output_file, index=False)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Combine CDR H3 and antibody framework and save as CSV file.")
    parser.add_argument("-i", "--input", required=True, help="Input file containing filenames and sequences.")
    parser.add_argument("-o", "--output", required=True, help="Output CSV file path.")
    return parser.parse_args()

def main():
    args = parse_arguments()
    df = read_input(args.input)
    save_output(args.output, df)

if __name__ == "__main__":
    main()

