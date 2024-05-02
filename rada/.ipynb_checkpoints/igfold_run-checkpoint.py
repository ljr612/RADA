import argparse
import csv
import subprocess

def run_igfold_for_file(input_csv):
    # 打开CSV文件并读取
    with open(input_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            # 准备参数
            filename = row['filename']
            H_sequence = row['H']
            L_sequence = row['L']
            protein_name = filename  # 假设文件名即蛋白名

            # 构建命令
            command = ['python', 'igfold_use.py', H_sequence, L_sequence, protein_name]
            
            # 运行命令并等待完成
            try:
                subprocess.run(command, check=True)
                print(f"Processed {protein_name}.pdb successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to process {protein_name}.pdb with error: {e}")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Batch process antibody structures using IgFold.")
    parser.add_argument('-i', '--input', type=str, required=True, help="Input CSV file containing filenames, H sequences, and L sequences.")
    args = parser.parse_args()
    return args.input

if __name__ == "__main__":
    input_csv = parse_arguments()
    run_igfold_for_file(input_csv)
