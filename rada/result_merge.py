import pandas as pd
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Merge ZDOCK and HDOCK results with antibody sequences into a single file.")
    parser.add_argument("-z", "--zdock_file", required=True, help="CSV file with ZDOCK results")
    parser.add_argument("-d", "--hdock_file", required=True, help="CSV file with HDOCK results")
    parser.add_argument("-i", "--input_file", required=True, help="CSV file with antibody sequences")
    parser.add_argument("-o", "--output_file", required=True, help="Output CSV file for merged results")
    return parser.parse_args()

def merge_data(args):
    zdock_df = pd.read_csv(args.zdock_file, index_col=0)
    hdock_df = pd.read_csv(args.hdock_file, index_col=0)
    input_df = pd.read_csv(args.input_file)
    
    if input_df.columns[0] == 'filename':
        input_df.set_index('filename', inplace=True)
    else:
        input_df.set_index(input_df.columns[0], inplace=True)
    
    zdock_df = zdock_df[['Predicted binding affinity (kcal.mol-1)']].rename(columns={'Predicted binding affinity (kcal.mol-1)': 'zdock_binding_affinity'})
    hdock_df = hdock_df[['Predicted binding affinity (kcal.mol-1)']].rename(columns={'Predicted binding affinity (kcal.mol-1)': 'hdock_binding_affinity'})
    
    zdock_df['zdock_ranking'] = zdock_df['zdock_binding_affinity'].rank(ascending=True, method='dense').astype(int)
    hdock_df['hdock_ranking'] = hdock_df['hdock_binding_affinity'].rank(ascending=True, method='dense').astype(int)
    
    result_df = pd.concat([input_df, zdock_df, hdock_df], axis=1, join='inner')
    
    result_df.to_csv(args.output_file, index_label='name')

if __name__ == "__main__":
    args = parse_arguments()
    merge_data(args)
