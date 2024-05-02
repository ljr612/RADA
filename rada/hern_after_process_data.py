import argparse

def process_file(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    lines = lines[1:]

    current_length = None
    count = 1
    output_lines = []

    for line in lines:
        parts = line.strip().split()
        length = int(parts[0][2:]) 

        if current_length != length:
            current_length = length
            count = 1

        index_name = f"l{length}_{count}"

        if float(parts[3]) > 10:
            continue

        new_sequence = parts[2][2:]

        modified_line = f"{index_name} {new_sequence} {parts[3]}\n"
        output_lines.append(modified_line)

        count += 1

    with open(output_file, 'w') as file:
        file.writelines(output_lines)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process and modify PDB files.")
    parser.add_argument('-i', '--input', required=True, help="Input file path")
    parser.add_argument('-o', '--output', required=True, help="Output file path")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    process_file(args.input, args.output)
