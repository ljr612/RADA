import argparse

def calculate_rmsd(filename):
    with open(filename, "r") as f:
        name = filename.split('/')[-1].split('.')[0]
        lh = int(name[1:3])-2
        
        sum_total = 0.0
        num_total = 0
        
        sum_h1 = 0.0
        num_h1 = 0
        
        sum_h2 = 0.0
        num_h2 = 0
        
        sum_h3 = 0.0
        num_h3 = 0
        
        sum_l1 = 0.0
        num_l1 = 0
        
        sum_l2 = 0.0
        num_l2 = 0
        
        sum_l3 = 0.0
        num_l3 = 0
        
        for line in f:
            l = line.split()
            if len(l) == 12:
                rmsd = float(l[10])
                residue_num = int(l[5])
                
                sum_total += rmsd
                num_total += 1
                
                chain = l[4]
                if chain == 'H':
                    if 31 <= residue_num <= 36:
                        sum_h1 += rmsd
                        num_h1 += 1
                    elif 50 <= residue_num <= 65:
                        sum_h2 += rmsd
                        num_h2 += 1
                    elif 98 <= residue_num <= 98 + lh:
                        sum_h3 += rmsd
                        num_h3 += 1
                elif chain == 'L':
                    if 24 <= residue_num <= 35:
                        sum_l1 += rmsd
                        num_l1 += 1
                    elif 51 <= residue_num <= 57:
                        sum_l2 += rmsd
                        num_l2 += 1
                    elif 90 <= residue_num <= 98:
                        sum_l3 += rmsd
                        num_l3 += 1
        
        rmsd_total = sum_total / num_total
        rmsd_h1 = sum_h1 / num_h1 
        rmsd_h2 = sum_h2 / num_h2 
        rmsd_h3 = sum_h3 / num_h3 
        rmsd_l1 = sum_l1 / num_l1 
        rmsd_l2 = sum_l2 / num_l2 
        rmsd_l3 = sum_l3 / num_l3 
        
        print(name,rmsd_total,rmsd_h1,rmsd_h2,rmsd_h3,rmsd_l1,rmsd_l2,rmsd_l3)

def parse_args():
    parser = argparse.ArgumentParser(description="Calculate RMSD from a PDB file")
    parser.add_argument("file", metavar="FILE", type=str, help="Input PDB file")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    filename = args.file
    result = calculate_rmsd(filename)

