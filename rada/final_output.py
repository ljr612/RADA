import pandas as pd
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Filter complexes by binding affinity or ranking.")
    parser.add_argument("-f", "--file", required=True, help="CSV file with merged ZDOCK and HDOCK results")
    parser.add_argument("-n", "--number", type=int, default=None, help="Top N rankings to include")
    parser.add_argument("-g", "--binding_energy", type=float, default=None, help="Binding energy threshold (negative value)")
    parser.add_argument("-o", "--output_file", required=True, help="Output CSV file for filtered results")
    return parser.parse_args()

def filter_data(args):
    df = pd.read_csv(args.file)

    filtered_df = pd.DataFrame()

    if args.number:
        filtered_df = df[(df['zdock_ranking'] <= args.number) & (df['hdock_ranking'] <= args.number)]
    elif args.binding_energy:
        filtered_df = df[(df['zdock_binding_affinity'] <= args.binding_energy) & (df['hdock_binding_affinity'] <= args.binding_energy)]
    
    if args.number and args.binding_energy:
        filtered_df = df[(df['zdock_ranking'] <= args.number) & (df['hdock_ranking'] <= args.number) &
                         (df['zdock_binding_affinity'] <= args.binding_energy) & (df['hdock_binding_affinity'] <= args.binding_energy)]

    filtered_df.to_csv(args.output_file, index=False)
    print(f"Filtered results saved to {args.output_file}")

if __name__ == "__main__":
    args = parse_arguments()
    filter_data(args)
