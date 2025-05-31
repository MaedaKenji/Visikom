import json
import os
import sys

def process_ipynb(input_file):
    # Read the input .ipynb file
    with open(input_file, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    code_lines = []
    
    # Iterate through each cell
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            for line in cell['source']:
                # Remove leading whitespace to check for comment
                stripped_line = line.lstrip()
                
                # Skip full-line comments
                if stripped_line.startswith('#'):
                    continue
                
                # Remove inline comments and clean up
                code_part = line.split('#', 1)[0].rstrip()
                if code_part:
                    code_lines.append(code_part + '\n')
    
    # Generate output filename
    base = os.path.splitext(input_file)[0]
    output_file = f"{base}_uncomment.py"
    
    # Write the processed code to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(code_lines)
    
    print(f"Processed file saved as {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_ipynb_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print(f"Error: The file {input_file} does not exist.")
        sys.exit(1)
    
    if not input_file.endswith('.ipynb'):
        print("Error: Input file must be a .ipynb file.")
        sys.exit(1)
    
    process_ipynb(input_file)