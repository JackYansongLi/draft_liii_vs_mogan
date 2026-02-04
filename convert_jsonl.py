import json
import sys
import os

def create_prefix_dataset(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return

    dataset = []
    
    print(f"Processing {input_file}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    count = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        length = len(line)
        mid_point = length // 2
        scan_index = mid_point
        while scan_index < length and line[scan_index] != ' ':
            scan_index += 1
        if scan_index < length:
            mid_point = scan_index + 1
        
        prefix = line[:mid_point]
        suffix = line[mid_point:]
        
        entry = {
            "instruction": "Complete the mathematical code.",
            "input": prefix,
            "output": suffix
        }
        dataset.append(entry)
        count += 1

    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in dataset:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
            
    print(f"Success! Converted {count} lines.")
    print(f"Saved to: {output_file}")
    
    if dataset:
        print("\n--- Sample Entry ---")
        print(f"Input:  {dataset[0]['input']}")
        print(f"Output: {dataset[0]['output']}")
        print("--------------------\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_to_jsonl.py <input_raw_txt> <output_jsonl>")
        print("Example: python convert_to_jsonl.py raw_latex.txt train_latex.jsonl")
    else:
        create_prefix_dataset(sys.argv[1], sys.argv[2])
